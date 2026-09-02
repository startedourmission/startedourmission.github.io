#!/bin/bash
# Update statistics in HOW THIS BLOG WORKS.md
# Called by Claude Code hook after git push

# 레포 루트를 스크립트 위치에서 유도한다 — 볼트를 옮겨도 따라온다.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BLOG="$ROOT/markdown-blog"
FILE="$BLOG/HOW THIS BLOG WORKS.md"

if [ ! -f "$FILE" ]; then
  echo "update-how-it-works: 대상 파일 없음 — $FILE" >&2
  exit 1
fi

posts=$(find "$BLOG" -name "*.md" -not -path "*/Dictionary/*" -not -name "HOW THIS*" -not -name "index.md" | wc -l | tr -d ' ')
dict=$(find "$BLOG/Dictionary" -name "*.md" | wc -l | tr -d ' ')
diagrams=$(find "$BLOG" -name "*.png" | wc -l | tr -d ' ')
links=$(grep -roh '\[\[' "$BLOG" --include="*.md" | wc -l | tr -d ' ')
today=$(date +%Y-%m-%d)

sed -i '' "s/^- 총 게시글: .*/- 총 게시글: $posts/" "$FILE"
sed -i '' "s/^- Dictionary 항목: .*/- Dictionary 항목: $dict/" "$FILE"
sed -i '' "s/^- 도해 이미지: .*/- 도해 이미지: $diagrams/" "$FILE"
sed -i '' "s/^- 위키 링크: .*/- 위키 링크: $links/" "$FILE"
sed -i '' "s/^- 마지막 업데이트: .*/- 마지막 업데이트: $today/" "$FILE"

echo "update-how-it-works: 게시글 $posts · Dictionary $dict · 도해 $diagrams · 링크 $links"
