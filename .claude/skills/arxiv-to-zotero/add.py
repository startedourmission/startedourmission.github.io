#!/usr/bin/env python3
"""Add arXiv papers to Zotero via the Web API.

Reads ZOTERO_USERID and ZOTERO_PRIVATE_KEY from env.
Caches the Inbox collection key next to this file.

Usage:
    add.py [--no-pdf] <arxiv-url-or-id> [<arxiv-url-or-id> ...]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    import certifi
    SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CTX = ssl.create_default_context()

SCRIPT_DIR = Path(__file__).resolve().parent
COLLECTION_CACHE = SCRIPT_DIR / ".collection_key"
COLLECTION_NAME = "Inbox"

ATOM_NS = "http://www.w3.org/2005/Atom"
ARXIV_NS = "http://arxiv.org/schemas/atom"


def die(msg: str, code: int = 1) -> None:
    print(f"❌ {msg}", file=sys.stderr)
    sys.exit(code)


def http(
    method: str,
    url: str,
    *,
    headers: dict | None = None,
    body: bytes | None = None,
    timeout: int = 60,
) -> tuple[int, dict, bytes]:
    req = urllib.request.Request(url, data=body, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as resp:
            return resp.status, dict(resp.headers), resp.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), e.read()


def zotero_headers(api_key: str, extra: dict | None = None) -> dict:
    h = {"Zotero-API-Key": api_key}
    if extra:
        h.update(extra)
    return h


def extract_arxiv_id(raw: str) -> str | None:
    raw = raw.strip()
    # Strip query/hash
    raw = raw.split("?", 1)[0].split("#", 1)[0]
    # PDF URL → abs ID
    m = re.search(r"arxiv\.org/(?:abs|pdf)/([a-z\-]+(?:\.[A-Z]{2})?/\d{7}|\d{4}\.\d{4,5})(v\d+)?", raw, re.I)
    if m:
        return m.group(1)
    m = re.match(r"^(\d{4}\.\d{4,5})(v\d+)?$", raw)
    if m:
        return m.group(1)
    m = re.match(r"^([a-z\-]+(?:\.[A-Z]{2})?/\d{7})(v\d+)?$", raw, re.I)
    if m:
        return m.group(1)
    return None


def fetch_arxiv_metadata(arxiv_id: str) -> dict:
    url = f"http://export.arxiv.org/api/query?id_list={urllib.parse.quote(arxiv_id)}"
    status, _, body = http("GET", url)
    if status != 200:
        raise RuntimeError(f"arXiv API status {status}")
    root = ET.fromstring(body)
    entry = root.find(f"{{{ATOM_NS}}}entry")
    if entry is None:
        raise RuntimeError("no entry in arXiv response")
    title_el = entry.find(f"{{{ATOM_NS}}}title")
    if title_el is None or not (title_el.text or "").strip():
        raise RuntimeError("missing title — bad ID?")
    title = re.sub(r"\s+", " ", title_el.text).strip()
    summary_el = entry.find(f"{{{ATOM_NS}}}summary")
    summary = re.sub(r"\s+", " ", (summary_el.text or "")).strip() if summary_el is not None else ""
    published_el = entry.find(f"{{{ATOM_NS}}}published")
    date = (published_el.text or "")[:10] if published_el is not None else ""
    authors = []
    for a in entry.findall(f"{{{ATOM_NS}}}author"):
        name_el = a.find(f"{{{ATOM_NS}}}name")
        if name_el is not None and name_el.text:
            authors.append(name_el.text.strip())
    doi_el = entry.find(f"{{{ARXIV_NS}}}doi")
    doi = (doi_el.text or "").strip() if doi_el is not None else ""
    cat_el = entry.find(f"{{{ARXIV_NS}}}primary_category")
    category = cat_el.get("term") if cat_el is not None else ""
    pdf_url = ""
    for link in entry.findall(f"{{{ATOM_NS}}}link"):
        if link.get("title") == "pdf":
            pdf_url = link.get("href", "")
            break
    if not pdf_url:
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    return {
        "id": arxiv_id,
        "title": title,
        "abstract": summary,
        "date": date,
        "authors": authors,
        "doi": doi,
        "category": category,
        "pdf_url": pdf_url,
    }


def split_name(full: str) -> dict:
    tokens = full.split()
    if len(tokens) == 1:
        return {"creatorType": "author", "name": tokens[0]}
    return {
        "creatorType": "author",
        "firstName": " ".join(tokens[:-1]),
        "lastName": tokens[-1],
    }


def ensure_collection_key(user_id: str, api_key: str) -> str:
    if COLLECTION_CACHE.exists():
        cached = COLLECTION_CACHE.read_text().strip()
        if cached:
            return cached
    status, _, body = http(
        "GET",
        f"https://api.zotero.org/users/{user_id}/collections?format=json&limit=100",
        headers=zotero_headers(api_key),
    )
    if status != 200:
        die(f"failed to list collections (status {status})")
    for c in json.loads(body):
        if c.get("data", {}).get("name") == COLLECTION_NAME:
            key = c["key"]
            COLLECTION_CACHE.write_text(key)
            return key
    # create it
    payload = json.dumps([{"name": COLLECTION_NAME, "parentCollection": False}]).encode()
    status, _, body = http(
        "POST",
        f"https://api.zotero.org/users/{user_id}/collections",
        headers=zotero_headers(api_key, {"Content-Type": "application/json"}),
        body=payload,
    )
    if status not in (200, 201):
        die(f"failed to create collection (status {status}): {body!r}")
    resp = json.loads(body)
    key = resp.get("successful", {}).get("0", {}).get("key")
    if not key:
        die(f"collection create response missing key: {resp}")
    COLLECTION_CACHE.write_text(key)
    return key


def create_item(user_id: str, api_key: str, meta: dict, collection_key: str) -> str:
    item = {
        "itemType": "preprint",
        "title": meta["title"],
        "creators": [split_name(n) for n in meta["authors"]] or [],
        "abstractNote": meta["abstract"],
        "repository": "arXiv",
        "archiveID": f"arXiv:{meta['id']}",
        "date": meta["date"],
        "DOI": meta["doi"],
        "url": f"https://arxiv.org/abs/{meta['id']}",
        "libraryCatalog": "arXiv.org",
        "collections": [collection_key],
        "tags": [{"tag": meta["category"]}] if meta["category"] else [],
    }
    status, _, body = http(
        "POST",
        f"https://api.zotero.org/users/{user_id}/items",
        headers=zotero_headers(api_key, {"Content-Type": "application/json"}),
        body=json.dumps([item]).encode(),
    )
    if status not in (200, 201):
        die(f"item POST failed ({status}): {body!r}")
    resp = json.loads(body)
    succ = resp.get("successful", {}).get("0", {})
    if not succ:
        die(f"item create failed: {resp}")
    return succ["key"]


def download_pdf(url: str, dest: Path) -> int:
    # arXiv likes a UA
    req = urllib.request.Request(url, headers={"User-Agent": "arxiv-to-zotero/1.0"})
    with urllib.request.urlopen(req, timeout=120, context=SSL_CTX) as r, dest.open("wb") as f:
        size = 0
        while True:
            chunk = r.read(65536)
            if not chunk:
                break
            f.write(chunk)
            size += len(chunk)
    return size


def attach_pdf(
    user_id: str, api_key: str, parent_key: str, pdf_path: Path, arxiv_id: str
) -> tuple[str, bool]:
    """Return (attachment_key, uploaded_now). uploaded_now=False means dedup hit."""
    filename = f"{arxiv_id.replace('/', '_')}.pdf"
    filesize = pdf_path.stat().st_size
    md5 = hashlib.md5(pdf_path.read_bytes()).hexdigest()
    mtime = int(time.time() * 1000)

    # 1. create attachment item
    attach = [{
        "itemType": "attachment",
        "parentItem": parent_key,
        "linkMode": "imported_file",
        "title": "arXiv Fulltext PDF",
        "filename": filename,
        "contentType": "application/pdf",
        "charset": "",
        "tags": [],
        "relations": {},
    }]
    status, _, body = http(
        "POST",
        f"https://api.zotero.org/users/{user_id}/items",
        headers=zotero_headers(api_key, {"Content-Type": "application/json"}),
        body=json.dumps(attach).encode(),
    )
    if status not in (200, 201):
        raise RuntimeError(f"attachment item POST failed ({status}): {body!r}")
    resp = json.loads(body)
    succ = resp.get("successful", {}).get("0", {})
    if not succ:
        raise RuntimeError(f"attachment create failed: {resp}")
    attach_key = succ["key"]

    # 2. request upload auth
    form = urllib.parse.urlencode({
        "md5": md5,
        "filename": filename,
        "filesize": str(filesize),
        "mtime": str(mtime),
    }).encode()
    status, _, body = http(
        "POST",
        f"https://api.zotero.org/users/{user_id}/items/{attach_key}/file",
        headers=zotero_headers(api_key, {
            "Content-Type": "application/x-www-form-urlencoded",
            "If-None-Match": "*",
        }),
        body=form,
    )
    if status != 200:
        raise RuntimeError(f"upload auth failed ({status}): {body!r}")
    auth = json.loads(body)
    if auth.get("exists") == 1:
        return attach_key, False

    upload_url = auth["url"]
    upload_ct = auth["contentType"]
    prefix = auth["prefix"].encode() if isinstance(auth["prefix"], str) else auth["prefix"]
    suffix = auth["suffix"].encode() if isinstance(auth["suffix"], str) else auth["suffix"]
    upload_key = auth["uploadKey"]

    # 3. upload to storage
    body_bytes = prefix + pdf_path.read_bytes() + suffix
    status, _, resp_body = http(
        "POST",
        upload_url,
        headers={"Content-Type": upload_ct},
        body=body_bytes,
        timeout=300,
    )
    if status not in (200, 201, 204):
        raise RuntimeError(f"storage upload failed ({status}): {resp_body!r}")

    # 4. register upload
    reg = urllib.parse.urlencode({"upload": upload_key}).encode()
    status, _, body = http(
        "POST",
        f"https://api.zotero.org/users/{user_id}/items/{attach_key}/file",
        headers=zotero_headers(api_key, {
            "Content-Type": "application/x-www-form-urlencoded",
            "If-None-Match": "*",
        }),
        body=reg,
    )
    if status not in (200, 204):
        raise RuntimeError(f"register upload failed ({status}): {body!r}")
    return attach_key, True


def process_one(user_id: str, api_key: str, raw: str, collection_key: str, attach_pdf_flag: bool) -> None:
    arxiv_id = extract_arxiv_id(raw)
    if not arxiv_id:
        print(f"⚠️  '{raw}' — arXiv ID 인식 실패, 건너뜀")
        return
    try:
        meta = fetch_arxiv_metadata(arxiv_id)
    except Exception as e:
        print(f"⚠️  {arxiv_id} — 메타데이터 실패: {e}")
        return
    item_key = create_item(user_id, api_key, meta, collection_key)

    pdf_note = ""
    if attach_pdf_flag:
        tmp = Path(f"/tmp/arxiv_{arxiv_id.replace('/', '_')}.pdf")
        try:
            download_pdf(meta["pdf_url"], tmp)
            _, uploaded = attach_pdf(user_id, api_key, item_key, tmp, arxiv_id)
            pdf_note = " · PDF 첨부됨" if uploaded else " · PDF 중복(dedup)"
        except Exception as e:
            pdf_note = f" · PDF 실패({e})"
        finally:
            if tmp.exists():
                tmp.unlink(missing_ok=True)

    print(f"✅ {meta['title'][:80]}")
    print(f"   arXiv:{arxiv_id} → Zotero {item_key}{pdf_note}")
    print(f"   zotero://select/library/items/{item_key}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-pdf", action="store_true", help="skip PDF attachment")
    ap.add_argument("inputs", nargs="+")
    args = ap.parse_args()

    user_id = os.environ.get("ZOTERO_USERID")
    api_key = os.environ.get("ZOTERO_PRIVATE_KEY")
    if not user_id or not api_key:
        die("ZOTERO_USERID/ZOTERO_PRIVATE_KEY env not set. `source .env` first.")

    collection_key = ensure_collection_key(user_id, api_key)

    for raw in args.inputs:
        process_one(user_id, api_key, raw, collection_key, attach_pdf_flag=not args.no_pdf)


if __name__ == "__main__":
    main()
