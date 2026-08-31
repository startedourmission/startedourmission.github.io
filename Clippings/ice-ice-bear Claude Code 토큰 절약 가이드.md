---
title: "Claude Code 토큰 절약 가이드"
source: "https://ice-ice-bear.github.io/ko/posts/2026-03-03-claude-code-token-optimization/"
author: "ice-ice-bear"
clipped: 2026-08-12
tags: [AI, Claude-Code, cost, Korea]
---

# Claude Code 토큰 절약 가이드 — 비용을 80% 줄이는 실전 전략

원문: https://ice-ice-bear.github.io/ko/posts/2026-03-03-claude-code-token-optimization/ (2026-03-03)
보완: https://aisparkup.com/posts/14700 (캐시 footgun, 2026-07-24)

## 핵심
- Claude Code 평균 ~$6/dev/day, $100–200/mo 인용. 습관+라우팅으로 50–80% 절감 주장.
- `/clear` 작업 전환 시, `/compact` 10–15턴마다, `/cost` 모니터링.
- CLAUDE.md ≤~500줄, 워크플로는 Skills로 on-demand 로드.
- 라우팅: Opus(아키텍처) / Sonnet(기본) / Haiku(탐색·테스트, ~80% 저렴).
- Extended thinking은 output 토큰 소모 — 단순 작업은 낮추거나 끔.
- 안 쓰는 MCP 끄기(매 턴 툴 정의 팽창). 가능하면 CLI(`gh` 등).
- 서브에이전트: 로그/테스트는 자식 컨텍스트, 요약만 반환.
