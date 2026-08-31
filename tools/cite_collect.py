#!/usr/bin/env python3
"""cite_collect.py — stub/grid_Papers 논문에 citations(인용수) 필드를 채운다.

star 점수가 인용수 기반(pow)으로 바뀌면서, buzz(blog Headliner용 화제도)와 별개로
논문의 역사적 임팩트=인용수를 frontmatter `citations:`에 저장한다.

arXiv ID 있는 논문은 Semantic Scholar API로 인용수 조회(S2 API 키 사용).
arXiv 없는 고전은 본문 note의 인용수나 수동 입력값을 유지(건드리지 않음).

Usage:
    python3 tools/cite_collect.py            # citations 없는 것만
    python3 tools/cite_collect.py --all      # 전체 재조회
"""
import sys, re, time, importlib.util
from pathlib import Path

sys.dont_write_bytecode = True
VAULT = Path(__file__).resolve().parent.parent
SRCS = [VAULT / "paper-stubs", VAULT / "markdown-blog/grid_Papers"]

_bu = VAULT / ".claude/skills/blog-check/buzz-update.py"
_spec = importlib.util.spec_from_file_location("buzz_update", _bu)
bu = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bu)

FRONT = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def get_arxiv(text):
    m = FRONT.match(text)
    if m:
        am = re.search(r'^arxiv:\s*"?([0-9]{4}\.[0-9]{4,5})"?', m.group(1), re.M)
        if am:
            return am.group(1)
    return bu.extract_arxiv_id(text)


def get_cite_field(text):
    m = FRONT.match(text)
    if not m:
        return None
    cm = re.search(r"^citations:\s*(\d+)", m.group(1), re.M)
    return int(cm.group(1)) if cm else None


def set_cite(text, value):
    m = FRONT.match(text)
    fm = m.group(1)
    if re.search(r"^citations:\s*\d+", fm, re.M):
        fm2 = re.sub(r"^citations:\s*\d+", f"citations: {value}", fm, flags=re.M)
    else:
        fm2 = fm.rstrip() + f"\ncitations: {value}"
    return text[:m.start(1)] + fm2 + text[m.end(1):]


def main():
    force = "--all" in sys.argv
    counts = {"ok": 0, "skip": 0, "no-arxiv": 0, "fail": 0}
    for src in SRCS:
        if not src.is_dir():
            continue
        for p in sorted(src.glob("*.md")):
            text = p.read_text(encoding="utf-8")
            if get_cite_field(text) is not None and not force:
                counts["skip"] += 1
                continue
            aid = get_arxiv(text)
            if not aid:
                counts["no-arxiv"] += 1
                continue
            c = bu.get_citations(aid)
            time.sleep(0.4)
            if c is None:
                counts["fail"] += 1
                print(f"  [fail] {p.stem[:55]}")
                continue
            p.write_text(set_cite(text, c), encoding="utf-8")
            counts["ok"] += 1
            print(f"  [ok] cite={c:>7}  {p.stem[:55]}")
    print("\n요약:", "  ".join(f"{k}={v}" for k, v in counts.items()))


if __name__ == "__main__":
    main()
