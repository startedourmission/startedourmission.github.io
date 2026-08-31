#!/usr/bin/env python3
"""끊어진 위키 링크 점검 (결정론적). 코드블록 제외.

`[[이름]]` 링크 중 대상 노트(`이름.md`)가 markdown-blog 어디에도 없는 것을 보고한다.
blog-check.sh 의 grep 기반 점검이 grid_Posts/grid_Papers 만 보던 것을,
Dictionary 까지 포함해 점검한다.

grep 방식의 두 함정을 피한다.
  1. 코드블록 오탐 — ```...``` 펜스와 인라인 `code` 안의 [[...]] (bash `[[ ]]`,
     파이썬 리스트 `[['a','b']]` 등)를 위키링크로 오인하지 않는다.
  2. 노이즈 폭주 — Dictionary 내부 링크는 수백 개라 전부 나열하면 일일 점검이
     묻힌다. 폴더별로 나눠, 본문(Posts/Papers)은 전부, Dictionary 는
     개수 요약 + 상위 N개만 보고한다.

대상 노트 존재 판정은 NFC 정규화 후 파일명 매칭 (macOS NFD 파일명 대응).

사용법:
  python3 tools/check_broken_links.py                # 요약 출력
  python3 tools/check_broken_links.py --dict-limit 30
  python3 tools/check_broken_links.py --json

종료 코드: 본문(Posts/Papers)에 깨진 링크가 있으면 1, 없으면 0.
  (Dictionary 깨진 링크는 양이 많아 종료 코드에 반영하지 않음 — 보고만.)
"""
import argparse
import glob
import json
import os
import re
import sys
import unicodedata

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(VAULT, "블로그", "markdown-blog")

# 점검 대상 폴더 (본문은 종료코드에 반영, Dictionary 는 보고만)
BODY_DIRS = ["grid_Posts", "grid_Papers"]
DICT_DIR = "Dictionary"


def nfc(s):
    return unicodedata.normalize("NFC", s)


def strip_code(text):
    """펜스 코드블록(```)과 인라인 코드(`)를 제거해 그 안의 [[...]] 오탐을 막는다."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", "", text)
    return text


def build_note_index():
    """markdown-blog 전체 .md 파일명(확장자 제거, NFC) 집합."""
    names = set()
    for dirpath, dirnames, filenames in os.walk(BLOG):
        if "_assets" in dirpath:
            continue
        for fn in filenames:
            if fn.endswith(".md"):
                names.add(nfc(fn[:-3]))
    return names


# [[타깃]] 또는 [[타깃|표시]] / [[타깃\|표시]] (표 안에서는 pipe를 \| 로 이스케이프)
LINK_RE = re.compile(r"\[\[([^\]\|\n]+?)(?:\\?\|[^\]\n]*)?\]\]")


def extract_links(text):
    out = []
    for m in LINK_RE.finditer(strip_code(text)):
        target = m.group(1).strip()
        # 표 셀의 escaped pipe 잔재(\) 제거
        target = target.rstrip("\\").strip()
        # 이미지·경로·임베드·헤딩앵커·숫자시작·... 제외
        if not target or target.startswith((".", "#", "/")):
            continue
        if "/" in target or target.startswith("..."):
            continue
        if re.search(r"\.(png|jpg|jpeg|gif|webp|svg|pdf)$", target, re.I):
            continue
        if target[0].isdigit():
            continue
        out.append(nfc(target))
    return out


def scan(folder, notes):
    """folder 안 .md 에서 깨진 링크 -> {target: [src files]}"""
    broken = {}
    root = os.path.join(BLOG, folder)
    for f in glob.glob(os.path.join(root, "**", "*.md"), recursive=True):
        if "_assets" in f:
            continue
        text = open(f, encoding="utf-8").read()
        src = os.path.basename(f)
        for tgt in set(extract_links(text)):
            if tgt not in notes:
                broken.setdefault(tgt, []).append(src)
    return broken


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dict-limit", type=int, default=25,
                    help="Dictionary 깨진 링크 표시 상한 (기본 25)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    notes = build_note_index()
    body_broken = {}
    for d in BODY_DIRS:
        for tgt, srcs in scan(d, notes).items():
            body_broken.setdefault(tgt, []).extend(srcs)
    dict_broken = scan(DICT_DIR, notes)

    if args.json:
        print(json.dumps({
            "body_broken": {k: sorted(set(v)) for k, v in sorted(body_broken.items())},
            "dict_broken_count": len(dict_broken),
            "dict_broken": {k: sorted(set(v)) for k, v in sorted(dict_broken.items())},
        }, ensure_ascii=False, indent=2))
    else:
        if not body_broken:
            print("본문(Posts/Papers) 끊어진 링크: 없음 ✓")
        else:
            print(f"본문(Posts/Papers) 끊어진 링크 {len(body_broken)}건:")
            for tgt in sorted(body_broken):
                srcs = ", ".join(sorted(set(body_broken[tgt]))[:2])
                print(f"    [[{tgt}]]  ← {srcs}")
        print()
        if not dict_broken:
            print("Dictionary 끊어진 링크: 없음 ✓")
        else:
            print(f"Dictionary 끊어진 링크 {len(dict_broken)}건 (상위 {args.dict_limit}, 참조 많은 순):")
            ranked = sorted(dict_broken.items(), key=lambda kv: -len(set(kv[1])))
            for tgt, srcs in ranked[:args.dict_limit]:
                print(f"    [[{tgt}]]  ({len(set(srcs))}곳)")
            if len(dict_broken) > args.dict_limit:
                print(f"    ... 외 {len(dict_broken) - args.dict_limit}건")

    sys.exit(1 if body_broken else 0)


if __name__ == "__main__":
    main()
