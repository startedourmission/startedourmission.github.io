---
type: tool
description: Anthropic의 공식 터미널·IDE 기반 코딩 에이전트, Claude 모델을 셸과 코드 컨텍스트에 연결하는 CLI
tags:
  - 도구
  - LLM
  - 에이전트
aliases:
  - "Claude Code"
  - "claude-code"
---

Claude Code는 [[Anthropic]]이 만든 공식 코딩 에이전트로, 터미널이나 IDE에서 [[Claude]] 모델을 직접 호출해 코드를 읽고 쓰고 실행하는 CLI 도구입니다. macOS·Windows 데스크톱 앱, claude.ai/code 웹, VS Code·JetBrains IDE 확장 등 여러 형태로 제공됩니다.

기본 사용 방식은 두 가지로 갈립니다. 대화형(interactive) 모드는 셸이나 IDE에서 사용자와 주고받으며 작업하는 형태이고, 비대화형(non-interactive) 모드는 `claude -p "<prompt>"` 형식으로 한 번에 응답을 받는 스크립트 친화적 형태입니다. cron job, CI/CD 파이프라인, GitHub Actions 같은 자동화에는 후자가 쓰입니다.

Claude Code의 핵심 기능으로는 슬래시 명령(`/`), 사용자 정의 스킬(skill), MCP 서버 연동, hook 시스템, 사용자 정의 키바인딩 등이 있습니다. [[MCP]]를 통해 외부 도구·데이터 소스를 에이전트에게 연결할 수 있고, 스킬은 특정 작업 패턴을 재사용 가능한 워크플로우로 묶어 둘 수 있습니다.

2026년 5월 발표에 따라, 2026년 6월 15일부터는 `claude -p` 비대화형 모드와 [[Claude Agent SDK]]를 통한 호출이 Claude 구독 한도가 아닌 별도의 월간 SDK 크레딧에서 차감됩니다. 대화형 Claude Code 사용은 기존 구독 한도를 그대로 따릅니다.
