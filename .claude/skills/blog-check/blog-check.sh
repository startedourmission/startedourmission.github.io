#!/usr/bin/env bash
# blog-check.sh — 블로그 파일 기반 점검 (끊긴 위키 링크 + 링크 추천 + 방치 초안)

VAULT="$HOME/Vaults/AutoVault"
POSTS="$VAULT/markdown-blog/grid_Posts"
PAPERS="$VAULT/markdown-blog/grid_Papers"
DICT="$VAULT/markdown-blog/Dictionary"
BLOG="$VAULT/markdown-blog"
DRAFTS="$VAULT/raw/drafts"

echo "====== 끊어진 위키 링크 ======"

# 본문(grid_Posts/grid_Papers) + Dictionary 의 [[링크]] 중 대상 노트가 없는 것.
# 코드블록 제외, escaped pipe(\|) 처리, 폴더별 요약 — 전용 스크립트로 점검.
# 본문 깨진 링크는 전부, Dictionary 는 양이 많아 개수+상위 25개만 보고한다.
python3 "$VAULT/tools/check_broken_links.py" 2>/dev/null || true

echo ""
echo "====== 링크 추천 (최근 30일 게시글) ======"
# Dictionary 항목명이 본문에 평문으로 등장하지만 [[...]] 링크가 없는 경우 신고

python3 - <<'PYEOF'
import os, re, time
from pathlib import Path

VAULT = os.path.expanduser("~/Vaults/AutoVault")
BLOG  = f"{VAULT}/markdown-blog"
DICT  = f"{BLOG}/Dictionary"
POSTS = f"{BLOG}/grid_Posts"
PAPERS= f"{BLOG}/grid_Papers"

# Dictionary 항목명 수집 (CLAUDE.md 제외)
dict_entries = sorted(
    [f.stem for f in Path(DICT).glob("*.md") if f.name != "CLAUDE.md"],
    key=lambda x: -len(x)  # 긴 이름 우선 → 부분일치 오탐 줄임
)

cutoff = time.time() - 30 * 86400
results = []

for folder in [POSTS, PAPERS]:
    for f in Path(folder).glob("*.md"):
        if f.stat().st_mtime < cutoff:
            continue
        raw = f.read_text(errors="ignore")
        # 프론트매터 제거
        body = raw
        if raw.startswith("---"):
            end = raw.find("---", 3)
            if end != -1:
                body = raw[end+3:]

        fname = f.name
        for entity in dict_entries:
            if entity not in body:
                continue
            # 이미 [[entity 형태로 링크된 경우 건너뜀
            if f"[[{entity}" in body:
                continue
            results.append(f"  [[{entity}]] ← {fname}")

if results:
    for r in sorted(set(results)):
        print(r)
else:
    print("  없음")
PYEOF

echo ""
echo "====== 방치된 초안 (7일 이상) ======"

find "$DRAFTS" -name "*.md" -mtime +7 2>/dev/null \
  | while IFS= read -r f; do
      age=$(( ( $(date +%s) - $(stat -f %m "$f" 2>/dev/null || stat -c %Y "$f" 2>/dev/null) ) / 86400 ))
      echo "${age}일 경과  —  $(basename "$f")"
    done \
  | sort -rn

echo ""
echo "====== 중복 노트 후보 ======"
# Dictionary 노트 중 같은 대상이 영문/한글 등으로 갈라진 경우 탐지 (결정론적)
# exit code 1(후보 있음)이어도 blog-check 전체는 계속 진행
python3 "$VAULT/tools/find_dupes.py" --body 2>/dev/null || true

echo ""
echo "====== 인물 노트 type/태그 불일치 ======"
# type:person ↔ '인물' 태그가 어긋나면 옵시디언 인물 뷰에서 누락된다
python3 "$VAULT/tools/check_person_tags.py" 2>/dev/null || true

echo ""
echo "====== buzz 업데이트 ======"

python3 "$VAULT/.claude/skills/blog-check/buzz-update.py" 2>/dev/null || echo "(buzz-update.py 실행 실패 — python3 확인 필요)"

echo ""
echo "====== 트렌드 데이터 갱신 (HN Trends) ======"
# 블로그 Trends 페이지용 assets/trends-data.json 재생성. 로컬 갱신만 — 자동 커밋/푸시 없음.
# buzz 업데이트와 동일하게 working tree에만 남고, 다음 블로그 push 때 라이브에 반영된다.
# launchd PATH엔 homebrew bin이 없으므로 node 절대경로를 우선 사용한다.
TRENDS_NODE="/opt/homebrew/bin/node"; [ -x "$TRENDS_NODE" ] || TRENDS_NODE="$(command -v node 2>/dev/null)"
TRENDS_GEN="$VAULT/scripts/gen-trends-data.js"
TRENDS_LOG="$VAULT/.claude/skills/blog-check/.gen-trends.log"
if [ -n "$TRENDS_NODE" ] && [ -x "$TRENDS_NODE" ] && [ -f "$TRENDS_GEN" ]; then
  if "$TRENDS_NODE" "$TRENDS_GEN" >/dev/null 2>"$TRENDS_LOG"; then
    echo "  갱신 완료 — assets/trends-data.json (다음 push 때 라이브 반영)"
  else
    echo "  갱신 실패/스킵 — $(tail -1 "$TRENDS_LOG" 2>/dev/null)"
  fi
else
  echo "  건너뜀 — node 또는 생성기 스크립트를 찾지 못함 ($TRENDS_NODE)"
fi

echo "====== 완료 ======"
