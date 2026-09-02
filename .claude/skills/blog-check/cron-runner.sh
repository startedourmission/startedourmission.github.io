#!/bin/bash
# launchd가 매일 04:00 KST에 호출하는 진입점.
# 볼트 루트의 blog-check-cron.md 에 실행 로그를 마크다운으로 누적 기록한다.

set -u

VAULT="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/AutoVault"
LOG="$HOME/Library/Logs/blog-daily-routine/blog-check-cron.md"
CLAUDE="$HOME/.local/bin/claude"

cd "$VAULT" || exit 1

# 최신 항목이 맨 위에 오도록 새 블록을 기존 로그 앞에 prepend 한다.
# 임시 파일은 로그와 같은 디렉터리(iCloud)에 만들어 mv 가 같은 파일시스템 내 rename 이 되게 한다.
TMP="$LOG.tmp.$$"
{
  echo ""
  echo "## $(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo ""
  echo '```'
  "$CLAUDE" -p "/blog-check" --dangerously-skip-permissions 2>&1
  echo '```'
  echo ""
  echo "---"
} > "$TMP"

[ -f "$LOG" ] && cat "$LOG" >> "$TMP"
mv "$TMP" "$LOG"
