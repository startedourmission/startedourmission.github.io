#!/usr/bin/env python3
"""인물 노트 type/태그 정합성 점검 (결정론적, LLM 판단 없음).

블로그 빌드는 `type: person` 으로 인물을 식별하지만, 옵시디언 뷰·베이스는
`인물` 태그로 필터링하는 경우가 많다. 둘이 어긋나면 한쪽에서 노트가
누락된다 (예: type:person 인데 인물 태그가 없으면 옵시디언 인물 뷰에서 안 보임).

두 불일치를 보고한다.
  A. type:person 인데 '인물' 태그 없음   -> 옵시디언 인물 뷰에서 누락
  B. '인물' 태그 있는데 type:person 아님  -> 오분류 (예: 회사인데 인물 태그)

자동 수정은 하지 않는다. 후보만 보고하고 사람이 판단한다
(B는 태그를 빼야 할지 type을 바꿔야 할지 맥락이 필요하므로).

사용법:
  python3 tools/check_person_tags.py            # Dictionary 스캔
  python3 tools/check_person_tags.py --json      # JSON 출력

종료 코드: 불일치가 있으면 1, 없으면 0 (cron 게이트용).
"""
import argparse
import glob
import json
import os
import re
import sys
import unicodedata

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT = os.path.join(VAULT, "블로그", "markdown-blog", "Dictionary")


def parse_fm(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    return m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    missing_tag = []   # type:person 인데 인물 태그 없음
    misclassified = []  # 인물 태그 있는데 type:person 아님

    files = sorted(glob.glob(os.path.join(DICT, "*.md")))
    for f in files:
        name = os.path.basename(f)
        if name == "CLAUDE.md":
            continue
        fm = parse_fm(open(f, encoding="utf-8").read())
        if fm is None:
            continue
        is_person = bool(re.search(r"^type:\s*person\s*$", fm, re.M))
        has_inmul = bool(re.search(r"^\s*-\s*인물\s*$", fm, re.M)) or \
            bool(re.search(r"^tags:\s*\[[^\]]*인물[^\]]*\]\s*$", fm, re.M))
        rel = os.path.relpath(f, VAULT)
        if is_person and not has_inmul:
            missing_tag.append(rel)
        elif has_inmul and not is_person:
            other = re.search(r"^type:\s*(\S+)", fm, re.M)
            misclassified.append({"file": rel, "type": other.group(1) if other else None})

    if args.json:
        print(json.dumps({
            "scanned": len(files),
            "missing_inmul_tag": missing_tag,
            "misclassified": misclassified,
        }, ensure_ascii=False, indent=2))
    else:
        print(f"스캔: {len(files)}개 (Dictionary)")
        if not missing_tag and not misclassified:
            print("type/태그 불일치 없음 ✓")
        else:
            if missing_tag:
                print(f"\ntype:person 인데 '인물' 태그 없음 (옵시디언 뷰 누락) — {len(missing_tag)}개:")
                for x in missing_tag:
                    print(f"    {x}")
            if misclassified:
                print(f"\n'인물' 태그 있는데 type:person 아님 (오분류) — {len(misclassified)}개:")
                for x in misclassified:
                    print(f"    {x['file']}  (type: {x['type']})")

    sys.exit(1 if (missing_tag or misclassified) else 0)


if __name__ == "__main__":
    main()
