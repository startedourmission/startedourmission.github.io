#!/usr/bin/env python3
"""게시 큐 — `ready` 체크박스로 게시 여부를 정한다 (stdlib only).

2026-08-31 구조 변경. 초안은 더 이상 별도 폴더(`raw/drafts/`)에 살지 않는다.
**모든 글은 처음부터 최종 목적지(`markdown-blog/…`)에 쓰이고**, 프론트매터의
`ready` 체크박스가 블로그 노출을 결정한다.

    ready: false   → 초안. F# 빌드(`Obsidian.isUnpublished`)가 통째로 건너뛴다.
                     HTML·인덱스·RSS·사이트맵·llms.txt 어디에도 안 나온다.
    ready 없음     → 게시. 기존 글 1,400여 편이 여기 해당한다.
    ready: true    → 게시. 사용자가 옵시디언에서 체크박스를 켠 것.

이 설계의 실패 방향은 의도적이다. 필드를 빠뜨리면 "조용히 사라짐"이 아니라
"그냥 올라감"이 된다. 이 볼트에서 두 번 크게 당한 게 전부 조용한 실패였다.

`ready`는 [[Headliner]]처럼 **사용자만 켠다.** Claude 는 새 글을 항상
`ready: false` 로 만들고 이 값을 true 로 바꾸지 않는다.

Usage:
    python3 tools/ready_queue.py            # 게시 대기(ready:true 인데 아직 push 안 됨)
    python3 tools/ready_queue.py --drafts   # ready:false 인 초안 전부
    python3 tools/ready_queue.py --all      # 초안 + 게시대기 한꺼번에
    python3 tools/ready_queue.py --dest TAG…  # 태그로 목적지 폴더 조회 (blog-draft 용)
"""
import sys
sys.dont_write_bytecode = True

import json
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate import parse_frontmatter  # noqa: E402

VAULT = Path(__file__).resolve().parent.parent
POSTS = VAULT / "markdown-blog"

TRUTHY = {"true", "yes", "on", "1"}
FALSY = {"false", "no", "off", "0"}

# 빌드가 개별 글로 취급하지 않는 특수 파일 (Program.fs 와 같은 목록)
SPECIAL = {"index.md", "links.md", "moc.md", "sub_index.md", "CLAUDE.md"}

# 시리즈·코스 태그가 분류 태그보다 우선한다.
SERIES_DEST = [
    ("KMS", "markdown-blog/Knowledge Management System/"),
    ("제프리힌턴", "markdown-blog/Mastermind/Geoffrey Hinton/"),
    ("얀르쿤", "markdown-blog/Mastermind/Yann LeCun/"),
    ("cs229", "markdown-blog/Lectures Translate/CS229 Lectures/"),
    ("cs230", "markdown-blog/Lectures Translate/CS230 Lectures/"),
    ("cme295", "markdown-blog/Lectures Translate/CME295 Lectures/"),
]

CLASSIFICATION_DEST = {
    "논문": "markdown-blog/grid_Papers/",
    "정보": "markdown-blog/grid_Posts/",
    "잡담": "markdown-blog/grid_Posts/",
}


def ready_state(fm: dict) -> str:
    """'true' | 'false' | 'absent'"""
    val = fm.get("ready")
    if val is None or isinstance(val, list):
        return "absent" if val is None else "false"
    s = str(val).strip().strip('"').strip("'").lower()
    if s in TRUTHY:
        return "true"
    if s in FALSY:
        return "false"
    return "absent"


def destination(tags: list) -> str | None:
    """태그로 목적지 폴더를 정한다. 확정 못 하면 None — 부르는 쪽이 사용자에게 묻는다."""
    tags = [str(t) for t in tags] if isinstance(tags, list) else []
    for series, dest in SERIES_DEST:
        if series in tags:
            return dest
    for tag in tags:
        if tag in CLASSIFICATION_DEST:
            return CLASSIFICATION_DEST[tag]
    return None


def classification(tags: list) -> str | None:
    tags = [str(t) for t in tags] if isinstance(tags, list) else []
    for tag in tags:
        if tag in CLASSIFICATION_DEST:
            return tag
    return None


def dirty_files() -> set:
    """git 이 아직 커밋하지 않은 파일 (수정 + 미추적). 게시 대기 판정에 쓴다."""
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain", "--", "markdown-blog"],
            cwd=VAULT, capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return set()
    paths = set()
    for line in out.splitlines():
        if len(line) < 4:
            continue
        p = line[3:].strip().strip('"')
        if " -> " in p:            # 이름 변경
            p = p.split(" -> ", 1)[1]
        paths.add(str((VAULT / p).resolve()))
    return paths


def row(path: Path, fm: dict, state: str) -> dict:
    tags = fm.get("tags") if isinstance(fm.get("tags"), list) else []
    image = str(fm.get("image", "")).strip().strip('"')
    return {
        "path": str(path.relative_to(VAULT)),
        "title": path.stem,
        "ready": state,
        "date": str(fm.get("date", "")).strip(),
        "tags": [str(t) for t in tags],
        "classification": classification(tags),
        "has_image": image not in ("", "![[]]"),
    }


def scan(want: str) -> list[dict]:
    """want: 'queue'(게시대기) | 'drafts'(초안) | 'all'"""
    if not POSTS.is_dir():
        return []
    dirty = dirty_files() if want in ("queue", "all") else set()
    rows = []
    for path in sorted(POSTS.rglob("*.md")):
        if path.name in SPECIAL or "_assets" in path.parts:
            continue
        try:
            fm, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        except OSError as exc:
            rows.append({"path": str(path.relative_to(VAULT)), "title": path.stem,
                         "ready": "?", "error": f"읽기 실패: {exc}"})
            continue

        state = ready_state(fm)
        if state == "false" and want in ("drafts", "all"):
            rows.append(row(path, fm, state))
        elif state == "true" and want in ("queue", "all"):
            # 이미 커밋·푸시된 ready:true 는 이미 라이브다. 대기 큐가 아니다.
            if str(path.resolve()) in dirty:
                rows.append(row(path, fm, state))

    rows.sort(key=lambda r: (r.get("date") or "9999-99-99", r["title"]))
    return rows


def main():
    args = sys.argv[1:]

    if args and args[0] == "--dest":
        dest = destination(args[1:])
        print(json.dumps({"status": "ok", "tags": args[1:], "dest": dest},
                         ensure_ascii=False))
        return

    want = "queue"
    if args and args[0] == "--drafts":
        want = "drafts"
    elif args and args[0] == "--all":
        want = "all"

    rows = scan(want)
    print(json.dumps({
        "status": "ok",
        "mode": want,
        "posts_dir": str(POSTS.relative_to(VAULT)),
        "count": len(rows),
        "queue": rows,
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
