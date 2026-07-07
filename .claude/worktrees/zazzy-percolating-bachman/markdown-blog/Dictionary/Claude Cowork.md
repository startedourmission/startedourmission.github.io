---
type: tool
description: "Anthropic의 팀 협업·자동화 워크스페이스, Claude 모델을 위키·문서·플러그인 워크플로우와 묶는 진입점"
tags:
  - 도구
  - LLM
  - 에이전트
aliases:
  - "Claude Cowork"
  - "Cowork"
---

Claude Cowork는 [[Anthropic]]이 운영하는 팀 협업·자동화 워크스페이스로, [[Claude]] 모델을 *팀의 위키·문서·자동화 워크플로우* 와 묶는 진입점입니다. [[Claude Code]](개발자 CLI), [[Claude Agent SDK]](빌더용 라이브러리)와 함께 [[Anthropic]]의 페르소나별 제품 라인업 중 하나를 이룹니다.

Cowork는 [[MCP]] 기반 커넥터와 *플러그인* 시스템을 핵심 확장 메커니즘으로 갖습니다. 플러그인은 슬래시 명령, 스킬, 사전 정의된 워크플로우의 묶음으로, *Claude for Small Business* 같은 버티컬 솔루션이 모두 Cowork 플러그인 형태로 배포됩니다.

플러그인 설치 경로는 *Customize → Plugins → + → 원하는 플러그인 → Install* 의 세 단계이고, 설치 즉시 슬래시 명령과 스킬이 활성화됩니다. Cowork 채팅창에서 `/` 를 치면 설치된 플러그인의 모든 명령이 자동완성으로 뜹니다.

2026년 6월 15일 이후로는 [[Claude Agent SDK]]·`claude -p` 사용량이 구독 한도에서 별도 SDK 크레딧으로 분리되지만, Cowork와 그 위의 플러그인 사용은 **여전히 구독 한도** 안에서 처리됩니다.
