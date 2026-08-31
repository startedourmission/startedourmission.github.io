#!/usr/bin/env python3
"""RSS feed validator for the startedourmission blog (stdlib only).

메모리 교훈(feedback_rss_verify_generated):
    RSS 오류는 소스를 눈으로 추측하지 말고, 실제 생성된 rss.xml을 파서로
    검증해서 정확한 line:col을 잡는다. 이 스크립트가 게시 전 그 게이트다.

왜 제어문자만 보는가:
    빌드(SkunkHtml.fs)가 <title>/<description>/<content:encoded>를 전부 CDATA로
    감싼다. CDATA 안에서는 `<` `>` `&`, LaTeX 백슬래시, 코드스팬이 XML을 깨지
    않는다(과거 이것들을 원인으로 지목한 게 전부 오답이었던 이유). `]]>`는 빌드의
    cdata()가 안전하게 쪼갠다. 남는 유일한 killer는 XML 1.0이 문서 어디에도 금지하는
    C0 제어문자(U+0000-001F 중 tab/LF/CR 제외)와 U+FFFE/U+FFFF다. CDATA 안이라도
    이건 파서가 문서 전체를 거부한다 — 실제 사고(제목 heading 속 U+0008)가 이거였다.

두 가지 모드:
    1) 생성물 검증 (authoritative, 로컬 빌드 후):
         python3 tools/rss_check.py 블로그/skunk-html-output
       디렉토리 안의 rss*.xml을 strict XML 파싱 + 불법 제어문자 스캔.
       파일들을 직접 지정해도 됨:  rss_check.py a.xml b.xml

    2) 소스 사전검사 (빌드 없이 빠르게):
         python3 tools/rss_check.py --source "markdown-blog/<목적지>/글제목.md"
       파일명(=RSS <title> 소스)과 본문에서 불법 XML 제어문자를 스캔.
       validate.py가 이미 본문을 보지만, 파일명까지 함께 보고 RSS 관점으로 보고한다.

출력: JSON. status = valid | invalid | error. exit code 0 | 1 | 2.
"""
import sys
sys.dont_write_bytecode = True

import json
import xml.etree.ElementTree as ET
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent

# 빌드 출력에서 검증할 피드 파일들
FEED_GLOB = "rss*.xml"

# XML 1.0에서 문서 어디에도(=CDATA 안에서도) 금지되는 문자.
#   허용 제어문자: U+0009(tab) U+000A(LF) U+000D(CR)
#   그 외 C0(U+0000-001F) 전부 불법 + U+FFFE, U+FFFF 불법.
def scan_illegal_chars(text: str) -> list[dict]:
    hits: list[dict] = []
    for i, ch in enumerate(text):
        o = ord(ch)
        illegal = (o < 0x20 and o not in (0x09, 0x0A, 0x0D)) or o in (0xFFFE, 0xFFFF)
        if not illegal:
            continue
        line_no = text.count("\n", 0, i) + 1
        col = i - text.rfind("\n", 0, i)
        ctx = text[max(0, i - 25):i + 10].replace("\n", "\\n")
        hits.append({
            "codepoint": f"U+{o:04X}",
            "line": line_no,
            "col": col,
            "context": f"...{ctx}...",
        })
    return hits


def validate_feed(path: Path) -> list[str]:
    """실제 생성된 피드 하나를 strict 파싱 + 불법문자 스캔."""
    errors: list[str] = []
    text = path.read_text(encoding="utf-8", errors="replace")

    # 1) 불법 제어문자 먼저 스캔 (파서 에러 위치보다 정확하고, 근본 원인을 짚어줌)
    for hit in scan_illegal_chars(text):
        errors.append(
            f"불법 XML 문자 {hit['codepoint']} (피드 전체가 깨짐): "
            f"line {hit['line']} col {hit['col']}: {hit['context']}"
        )

    # 2) strict XML 파싱 (expat) — 위 스캔이 놓친 구조 오류까지 잡는다
    try:
        ET.parse(str(path))
    except ET.ParseError as e:
        line, col = getattr(e, "position", (0, 0))
        # 이미 제어문자로 설명된 경우 중복 보고 피함
        if not errors:
            errors.append(f"XML 파싱 실패: line {line} col {col}: {e}")
        else:
            errors.append(f"(파서도 거부: line {line} col {col}: {e})")

    return errors


def run_built(targets: list[Path]) -> dict:
    feeds: list[Path] = []
    for t in targets:
        if t.is_dir():
            feeds.extend(sorted(t.glob(FEED_GLOB)))
        elif t.exists():
            feeds.append(t)

    if not feeds:
        hint = targets[0] if targets else "?"
        return {
            "status": "error",
            "message": (
                f"검증할 피드 파일 없음: {hint} — 먼저 로컬 빌드로 rss*.xml을 생성하세요 "
                "(export PATH=\"$HOME/.dotnet:$PATH\"; cd 블로그 && dotnet run --project skunk-html.fsproj)"
            ),
        }

    all_errors: dict[str, list[str]] = {}
    for feed in feeds:
        errs = validate_feed(feed)
        if errs:
            try:
                key = str(feed.resolve().relative_to(VAULT))
            except ValueError:
                key = str(feed)
            all_errors[key] = errs

    if all_errors:
        return {"status": "invalid", "checked": len(feeds), "errors": all_errors}
    return {
        "status": "valid",
        "checked": len(feeds),
        "feeds": [f.name for f in feeds],
    }


def run_source(path: Path) -> dict:
    if not path.exists():
        return {"status": "error", "message": f"파일 없음: {path}"}

    errors: list[str] = []
    # 파일명 = RSS <title> 소스. 여기에 제어문자가 박히면 피드가 깨진다.
    for hit in scan_illegal_chars(path.name):
        errors.append(
            f"파일명(RSS 제목)에 불법 XML 문자 {hit['codepoint']}: "
            f"col {hit['col']}: {hit['context']}"
        )
    # 본문 + 프론트매터(description 포함) 전체
    text = path.read_text(encoding="utf-8", errors="replace")
    for hit in scan_illegal_chars(text):
        errors.append(
            f"본문/프론트매터에 불법 XML 문자 {hit['codepoint']} (RSS 깨짐): "
            f"line {hit['line']} col {hit['col']}: {hit['context']}"
        )

    try:
        rel = path.resolve().relative_to(VAULT)
    except ValueError:
        rel = path

    if errors:
        return {"status": "invalid", "path": str(rel), "errors": errors}
    return {"status": "valid", "path": str(rel)}


def main():
    args = sys.argv[1:]
    if not args:
        print(
            "usage:\n"
            "  rss_check.py <output-dir-or-xml-files...>   # 생성물 검증\n"
            "  rss_check.py --source <draft.md>            # 소스 사전검사",
            file=sys.stderr,
        )
        sys.exit(2)

    if args[0] == "--source":
        if len(args) < 2:
            print("usage: rss_check.py --source <draft.md>", file=sys.stderr)
            sys.exit(2)
        p = Path(args[1])
        if not p.is_absolute():
            p = (Path.cwd() / p).resolve()
        result = run_source(p)
    else:
        targets = []
        for a in args:
            p = Path(a)
            if not p.is_absolute():
                p = (Path.cwd() / p).resolve()
            targets.append(p)
        result = run_built(targets)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["status"] == "valid":
        sys.exit(0)
    elif result["status"] == "invalid":
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
