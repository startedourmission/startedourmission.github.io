#!/usr/bin/env python3
"""중복 노트 탐지 (결정론적, LLM 판단 없음).

같은 대상이 두 개 이상의 노트로 갈라진 경우를 빠르게 찾는다.
대표 사례: 영문명/한글 음역으로 나뉜 인물·개념 노트
  (예: "Dahua Lin.md" vs "린 다후아.md", "Yejin Choi.md" vs "최예진.md").

세 가지 신호를 본다. 모두 파싱 기반이라 수 초 내에 끝난다.

  1. 이름 충돌 (name collision)
     각 노트의 파일명(title) + frontmatter aliases 를 정규화
     (소문자화, 공백·구두점 제거)한 키로 모은다.
     한 키에 서로 다른 파일이 둘 이상 매달리면 중복 후보.
     한 노트의 alias가 다른 노트의 제목과 같으면 여기서 잡힌다.

  2. 제목 토큰 동일 (title token match)
     제목을 토큰화해 (영문 소문자 + 한글) 정렬한 뒤,
     서로 다른 파일이 같은 토큰 멀티셋을 가지면 후보.
     "GPT 5.5" vs "GPT-5.5" 같은 구분자 차이를 잡는다.

  3. 본문 첫 문단 유사도 (옵션, --body)
     첫 비어있지 않은 문단을 토큰 집합으로 만들고
     자카드 유사도가 임계치(기본 0.6) 이상이면 후보.
     alias 없이 갈린 경우의 안전망. 느려서 기본 비활성.

사용법:
  python3 tools/find_dupes.py                      # Dictionary 스캔 (기본)
  python3 tools/find_dupes.py --dir bl로그/markdown-blog   # 다른 폴더
  python3 tools/find_dupes.py --all                # 볼트 전체 .md
  python3 tools/find_dupes.py --body               # 본문 유사도까지
  python3 tools/find_dupes.py --json               # 기계가 읽을 JSON 출력

종료 코드: 중복 후보가 있으면 1, 없으면 0 (CI/cron 게이트용).
"""
import argparse
import glob
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DIR = os.path.join("markdown-blog", "Dictionary")

SKIP_DIRS = {".git", "node_modules", ".obsidian", "_assets", "Archive"}


def iter_md(root, recursive):
    if recursive:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in filenames:
                if fn.endswith(".md"):
                    yield os.path.join(dirpath, fn)
    else:
        for p in glob.glob(os.path.join(root, "*.md")):
            yield p


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    return m.group(1) if m else ""


def get_aliases(fm):
    out = []
    in_block = False
    for line in fm.splitlines():
        if re.match(r"^\s*aliases:", line):
            in_block = True
            # inline form: aliases: [a, b]
            inline = re.match(r"^\s*aliases:\s*\[(.+)\]\s*$", line)
            if inline:
                out += [x.strip().strip("\"'") for x in inline.group(1).split(",")]
                in_block = False
            continue
        if in_block:
            ma = re.match(r"^\s*-\s*(.+?)\s*$", line)
            if ma:
                out.append(ma.group(1).strip().strip("\"'"))
            elif re.match(r"^\S", line):
                in_block = False
    return [a for a in out if a]


def nfc(s):
    """macOS 파일시스템은 한글 파일명을 NFD(자모 분리)로 준다.
    완성형 정규식이 먹히도록 NFC로 합성한다."""
    return unicodedata.normalize("NFC", s)


def norm_name(s):
    """소문자화 + 모든 공백·구두점 제거. 'Lin Dahua' == 'lindahua'."""
    s = nfc(s).strip().lower()
    s = re.sub(r"[\s\-_.·:/,'\"()]+", "", s)
    return s


def title_tokens(title):
    """영문 단어(소문자) + 한글 음절 토큰의 정렬 튜플."""
    toks = re.findall(r"[a-z0-9]+|[가-힣]+", nfc(title).lower())
    return tuple(sorted(toks))


def first_paragraph(text):
    body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
    for para in re.split(r"\n\s*\n", body):
        p = para.strip()
        if p and not p.startswith("#") and not p.startswith(">"):
            return p
    return ""


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=DEFAULT_DIR, help="스캔할 폴더 (볼트 기준 상대경로)")
    ap.add_argument("--all", action="store_true", help="볼트 전체 .md 재귀 스캔")
    ap.add_argument("--body", action="store_true", help="본문 첫 문단 유사도까지 검사 (느림)")
    ap.add_argument("--threshold", type=float, default=0.6, help="본문 자카드 임계치")
    ap.add_argument("--json", action="store_true", help="JSON 출력")
    args = ap.parse_args()

    root = VAULT if args.all else os.path.join(VAULT, args.dir)
    recursive = args.all
    files = sorted(iter_md(root, recursive))

    name_idx = defaultdict(set)   # norm name -> {file}
    title_idx = defaultdict(set)  # token tuple -> {file}
    bodies = {}                   # file -> token set (first paragraph)

    for f in files:
        rel = os.path.relpath(f, VAULT)
        text = open(f, encoding="utf-8").read()
        fm = parse_frontmatter(text)
        title = os.path.basename(f)[:-3]

        names = {title, *get_aliases(fm)}
        for n in names:
            name_idx[norm_name(n)].add(rel)

        title_idx[title_tokens(title)].add(rel)

        if args.body:
            toks = set(re.findall(r"[a-z0-9]+|[가-힣]+", nfc(first_paragraph(text)).lower()))
            bodies[rel] = toks

    findings = []

    for key, fs in sorted(name_idx.items()):
        if len(fs) > 1:
            findings.append({"signal": "name", "key": key, "files": sorted(fs)})

    for toks, fs in sorted(title_idx.items()):
        if toks and len(fs) > 1:
            # name 신호와 완전히 같은 묶음이면 중복 보고 생략
            sf = sorted(fs)
            if not any(d["signal"] == "name" and d["files"] == sf for d in findings):
                findings.append({"signal": "title", "key": " ".join(toks), "files": sf})

    if args.body:
        items = list(bodies.items())
        seen_pairs = set()
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                fa, ta = items[i]
                fb, tb = items[j]
                sim = jaccard(ta, tb)
                if sim >= args.threshold:
                    pair = tuple(sorted((fa, fb)))
                    if pair in seen_pairs:
                        continue
                    seen_pairs.add(pair)
                    findings.append({
                        "signal": "body",
                        "key": f"jaccard={sim:.2f}",
                        "files": list(pair),
                    })

    if args.json:
        print(json.dumps({"scanned": len(files), "findings": findings},
                         ensure_ascii=False, indent=2))
    else:
        scope = "볼트 전체" if args.all else args.dir
        print(f"스캔: {len(files)}개 ({scope})")
        if not findings:
            print("중복 후보 없음 ✓")
        else:
            label = {"name": "이름 충돌", "title": "제목 토큰 동일", "body": "본문 유사"}
            print(f"중복 후보 {len(findings)}건:\n")
            for d in findings:
                print(f"[{label[d['signal']]}] {d['key']}")
                for f in d["files"]:
                    print(f"    {f}")
                print()

    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
