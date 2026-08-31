#!/usr/bin/env python3
"""stub_buzz.py — paper-stubs/ 폴더 stub 노트의 buzz를 채운다.

blog-check의 buzz-update.py 공식·API를 그대로 재사용한다(동일 buzz 척도).
단, stub은 블로그 repo 밖이므로 Headliner 로직은 일절 건드리지 않는다.

각 stub은 frontmatter `arxiv:` 또는 본문 `arXiv:XXXX.XXXXX`로 arXiv ID를 갖는다.
ID로 HF upvotes + Semantic Scholar 인용수를 긁어 buzz를 frontmatter에 기록한다.

Usage:
    python3 tools/stub_buzz.py                # buzz 없는 stub만
    python3 tools/stub_buzz.py --all          # 전체 재계산
    python3 tools/stub_buzz.py <file.md>      # 단일
"""
import sys, re, time, importlib.util
from pathlib import Path

sys.dont_write_bytecode = True
VAULT = Path(__file__).resolve().parent.parent
STUBS = VAULT / "paper-stubs"

# buzz-update.py 모듈 로드 (하이픈 파일명이라 import 불가 → spec 로드)
_bu_path = VAULT / ".claude/skills/blog-check/buzz-update.py"
_spec = importlib.util.spec_from_file_location("buzz_update", _bu_path)
bu = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bu)

FRONT_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def extract_arxiv(text: str) -> str | None:
    m = FRONT_RE.match(text)
    if m:
        am = re.search(r'^arxiv:\s*"?([0-9]{4}\.[0-9]{4,5})"?', m.group(1), re.M)
        if am:
            return am.group(1)
    return bu.extract_arxiv_id(text)


def get_buzz(text: str) -> int | None:
    return bu.get_buzz_value(text)


def set_buzz_fm(text: str, value: int) -> str:
    """frontmatter에 buzz: 줄을 추가/갱신 (올바른 YAML, 깨진 패턴 안 씀)."""
    m = FRONT_RE.match(text)
    if not m:
        return text
    fm = m.group(1)
    if re.search(r"^buzz:\s*\d+", fm, re.M):
        fm2 = re.sub(r"^buzz:\s*\d+", f"buzz: {value}", fm, flags=re.M)
    else:
        fm2 = fm.rstrip() + f"\nbuzz: {value}"
    return text[:m.start(1)] + fm2 + text[m.end(1):]


def set_partial(text: str, partial: bool) -> str:
    """citation 누락 상태 표시. partial=True면 buzz_partial: true 추가, 아니면 제거."""
    m = FRONT_RE.match(text)
    if not m:
        return text
    fm = m.group(1)
    fm = re.sub(r"\n?buzz_partial:\s*\w+", "", fm)  # 기존 제거
    if partial:
        fm = fm.rstrip() + "\nbuzz_partial: true"
    return text[:m.start(1)] + fm + text[m.end(1):]


def process(path: Path, force: bool, hf_only: bool) -> tuple[str, int | None, int | None]:
    text = path.read_text(encoding="utf-8")
    old = get_buzz(text)
    was_partial = bool(re.search(r"^buzz_partial:\s*true", FRONT_RE.match(text).group(1), re.M)) if FRONT_RE.match(text) else False
    # 완전한 buzz가 이미 있으면 skip. partial이면 citation 재시도 위해 통과.
    if old is not None and not force and not was_partial:
        return ("skip", old, old)
    aid = extract_arxiv(text)
    if not aid:
        return ("no-arxiv", old, None)
    hf = bu.get_hf_upvotes(aid)
    time.sleep(0.1)
    cite = bu.get_citations(aid)
    time.sleep(1.5)   # Semantic Scholar 비인증 레이트 리밋(429) 회피
    if cite is None:
        if not hf_only or hf <= 0:
            # citation 못 받았고 hf-only도 아니거나 HF도 0이면 손대지 않는다.
            # (HF 0인 고전 논문을 0으로 덮는 사고 방지)
            return ("api-fail", old, None)
        # HF만으로 산출 (citation=0 가정), partial 표시
        new = bu.calc_buzz(hf, 0)
        out = set_partial(set_buzz_fm(text, new), True)
        path.write_text(out, encoding="utf-8")
        return ("hf-only", old, new)
    new = bu.calc_buzz(hf, cite)
    out = set_partial(set_buzz_fm(text, new), False)  # citation 확보 → partial 해제
    path.write_text(out, encoding="utf-8")
    return ("ok", old, new)


def main():
    args = [a for a in sys.argv[1:]]
    force = "--all" in args
    hf_only = "--hf-only" in args
    args = [a for a in args if a not in ("--all", "--hf-only")]

    if args:
        files = [Path(args[0])]
    else:
        files = sorted(STUBS.glob("*.md"))

    counts = {}
    for p in files:
        status, old, new = process(p, force, hf_only)
        counts[status] = counts.get(status, 0) + 1
        print(f"  [{status:8}] buzz {old}→{new}  {p.stem[:60]}")
    print("\n요약:", "  ".join(f"{k}={v}" for k, v in sorted(counts.items())))


if __name__ == "__main__":
    main()
