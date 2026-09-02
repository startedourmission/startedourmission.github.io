#!/bin/bash
# 최근 N일(기본 7) 이내 frontmatter date 를 가진 블로그 게시글을 찾는다.
# markdown-blog 전체를 훑되, 구조용 파일(moc/index/links 등)과 _assets 는 제외.
#
# 출력 (탭 구분, 날짜 내림차순):
#   YYYY-MM-DD <TAB> 요일(1=월 .. 7=일) <TAB> 상대경로(markdown-blog 기준)
#
# 사용:  bash collect_week_posts.sh [DAYS]
#   DAYS 생략 시 7. 롤링 윈도(오늘 ~ 오늘-(DAYS-1)) — 7일이면 각 요일이 정확히 한 번씩.
#
# 메모: macOS 기본 bash 는 3.2 라서 `read -d ''`(NUL) 가 grep -Z 파이프와 불안정.
#       블로그 파일명에 개행은 없으므로 개행 구분 + `IFS= read -r` 로 처리(공백·콤마 안전).
set -u

VAULT="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/AutoVault"
BLOG="$VAULT/markdown-blog"
DAYS="${1:-7}"

cd "$BLOG" || { echo "ERROR: markdown-blog 폴더를 찾을 수 없음: $BLOG" >&2; exit 1; }

# 7일 창에 해당하는 날짜 집합을 공백으로 둘러싸 만든다 (BSD/macOS date).
win=""
i=0
while [ "$i" -lt "$DAYS" ]; do
  win="$win $(date -v-"${i}"d +%Y-%m-%d)"
  i=$((i + 1))
done

# frontmatter 에 date: 가 있는 .md 후보를 순회.
grep -rlE '^date:' --include='*.md' . 2>/dev/null | while IFS= read -r f; do
  base=$(basename "$f")
  # 구조용·시스템 파일 제외 (실제 게시글 아님).
  case "$base" in
    moc.md|MOC.md|index.md|links.md|node-pretext.md|"HOW THIS BLOG WORKS.md") continue ;;
  esac
  d=$(grep -m1 -E '^date:' "$f" | sed -E 's/^date:[[:space:]]*"?([0-9]{4}-[0-9]{2}-[0-9]{2}).*/\1/')
  case " $win " in
    *" $d "*)
      wd=$(date -j -f "%Y-%m-%d" "$d" +%u 2>/dev/null)
      printf '%s\t%s\t%s\n' "$d" "$wd" "${f#./}"
      ;;
  esac
done | sort -r
