#!/usr/bin/env python3
"""Blog frontmatter validator (stdlib only).

Trading Vault의 validate.py 패턴을 블로그 규칙에 맞게 적용.
LLM이 직접 검증하는 대신 결정론적 Python이 게이트를 지킨다.

Usage:
    python3 tools/validate.py markdown-blog/<목적지>/some-post.md
    python3 tools/validate.py markdown-blog/grid_Posts/some-post.md
    python3 tools/validate.py --check-h1 markdown-blog/<목적지>/some-post.md
"""
import sys
sys.dont_write_bytecode = True

import json
import re
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent

# 허용된 분류 태그 (필수 1개 이상)
CLASSIFICATION_TAGS = {"논문", "정보", "잡담"}

# 허용된 주제 태그 (CLAUDE.md 기준 — 참조용, 강제 아님)
SUBJECT_TAGS = {
    "LLM", "멀티모달", "컴퓨터비전", "영상처리", "음성", "NLP",
    "강화학습", "추론", "에이전트", "확산모델", "트랜스포머",
    "머신러닝", "딥러닝", "데이터분석", "파이썬", "오픈소스", "도구",
    "GPU", "TPU", "반도체", "벤치마크", "AI평가", "SaaS",
}

# 시리즈 태그 (CLAUDE.md 기준)
SERIES_TAGS = {"제프리힌턴", "얀르쿤", "cs229", "cs230", "cme295", "book", "KMS"}

# 특수 태그 (사용자 전용이지만 검증에서 허용)
SPECIAL_TAGS = {"Headliner", "headliner", "베스트논문", "MOC", "인물"}

ALL_KNOWN_TAGS = CLASSIFICATION_TAGS | SUBJECT_TAGS | SERIES_TAGS | SPECIAL_TAGS

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Dictionary/ 경로에 있는 파일은 분류 태그 필수 아님
DICT_PATH_FRAGMENT = "Dictionary"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """YAML frontmatter를 간단한 key-value로 파싱. body도 반환."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    fm_lines = []
    end_idx = None
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            end_idx = i
            break
        fm_lines.append(line)

    if end_idx is None:
        return {}, text

    body = "\n".join(lines[end_idx + 1:])
    fm: dict = {}
    current_key = None
    current_list = None

    for line in fm_lines:
        # list item
        if line.startswith("  - "):
            val = line[4:].strip()
            # 따옴표 제거
            if (val.startswith('"') and val.endswith('"')) or \
               (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            if current_list is not None:
                current_list.append(val)
            continue
        # key: value
        if ":" in line and not line.startswith(" "):
            current_list = None
            key, _, rest = line.partition(":")
            key = key.strip()
            val = rest.strip()
            if val == "" or val == "|" or val == ">":
                # 다음 줄이 리스트 또는 멀티라인
                current_key = key
                current_list = []
                fm[key] = current_list
            else:
                if (val.startswith('"') and val.endswith('"')) or \
                   (val.startswith("'") and val.endswith("'")):
                    val = val[1:-1]
                fm[key] = val
                current_key = key

    return fm, body


def is_dictionary_path(path: Path) -> bool:
    return DICT_PATH_FRAGMENT in str(path)


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)

    if not fm:
        errors.append("프론트매터 없음 (--- 블록이 없거나 파싱 실패)")
        return errors

    # 1. date 검증
    date = fm.get("date")
    if not date:
        errors.append("date 필드 없음")
    else:
        date_str = str(date).strip()
        if not DATE_RE.match(date_str):
            errors.append(f"date 형식 오류: '{date_str}' (YYYY-MM-DD 필요)")

    # 2. description 검증
    desc = fm.get("description")
    if not desc or (isinstance(desc, str) and not desc.strip()):
        errors.append("description 필드 없음 또는 비어 있음")

    # 3. tags 검증
    tags = fm.get("tags")
    if tags is None:
        errors.append("tags 필드 없음")
    elif not isinstance(tags, list):
        errors.append(f"tags가 리스트 형식이 아님: {tags!r}")
    else:
        if len(tags) > 5:
            errors.append(f"태그가 5개 초과: {len(tags)}개")

        for t in tags:
            t = str(t)
            if t.startswith("#"):
                errors.append(f"태그에 # 금지: '{t}'")
            if t.startswith('"') or t.startswith("'"):
                errors.append(f"태그에 따옴표 금지: '{t}'")

        # 분류 태그 필수 (Dictionary 제외)
        if not is_dictionary_path(path):
            has_classification = any(t in CLASSIFICATION_TAGS for t in tags)
            if not has_classification:
                errors.append(
                    f"분류 태그 없음 — 논문/정보/잡담 중 1개 필수 (현재: {tags})"
                )

    # 4. 본문 H1 금지 (코드 펜스 내부는 건너뜀)
    in_fence = False
    for i, line in enumerate(body.splitlines(), 1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("# "):
            errors.append(f"본문에 H1 금지 (빌드가 자동 생성): line {i}: {line[:60]!r}")
            break  # 첫 번째만 보고

    # 5. 불법 XML 제어문자 (RSS 피드 깨짐 방지)
    # XML 1.0이 문서 어디에도(CDATA 안에서도) 금지하는 문자:
    #   U+0000-0008, U+000B, U+000C, U+000E-001F (tab/LF/CR만 허용) + U+FFFE, U+FFFF.
    # 빌드가 제목·description·본문을 전부 CDATA로 감싸므로 이게 유일한 피드 killer다.
    # 보이지 않는 문자라 눈으로 못 잡는다 (과거 U+0008 사고). 파일명(=RSS 제목)도 함께 본다.
    def is_illegal_xml(o: int) -> bool:
        return (o < 0x20 and o not in (0x09, 0x0A, 0x0D)) or o in (0xFFFE, 0xFFFF)

    for i, ch in enumerate(text):
        o = ord(ch)
        if is_illegal_xml(o):
            line_no = text.count("\n", 0, i) + 1
            col = i - text.rfind("\n", 0, i)
            ctx = text[max(0, i - 20):i + 10].replace("\n", "\\n")
            errors.append(
                f"불법 XML 제어문자 U+{o:04X} (RSS 피드 깨짐): "
                f"line {line_no} col {col}: ...{ctx}..."
            )

    for i, ch in enumerate(path.name):
        o = ord(ch)
        if is_illegal_xml(o):
            errors.append(
                f"파일명(RSS 제목)에 불법 XML 제어문자 U+{o:04X}: col {i + 1}: {path.name!r}"
            )

    return errors


def main():
    if len(sys.argv) < 2:
        print("usage: validate.py <path-to-draft>", file=sys.stderr)
        sys.exit(2)

    path = Path(sys.argv[1])
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    if not path.exists():
        print(json.dumps({"status": "error", "message": f"파일 없음: {path}"}))
        sys.exit(2)

    errors = validate(path)

    try:
        rel = path.resolve().relative_to(VAULT)
    except ValueError:
        rel = path

    if errors:
        print(json.dumps({
            "status": "invalid",
            "path": str(rel),
            "errors": errors,
        }, indent=2, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps({"status": "valid", "path": str(rel)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
