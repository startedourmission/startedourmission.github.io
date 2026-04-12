#!/bin/bash
# Update statistics in HOW THIS BLOG WORKS.md
# Called by Claude Code hook after git push

BLOG="/Users/chajinwoo/Library/Mobile Documents/iCloud~md~obsidian/Documents/AutoVault/블로그/markdown-blog"
FILE="$BLOG/HOW THIS BLOG WORKS.md"

if [ ! -f "$FILE" ]; then
  exit 0
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
