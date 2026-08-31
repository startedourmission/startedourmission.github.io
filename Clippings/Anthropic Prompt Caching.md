---
title: "Prompt caching — Anthropic"
source: "https://platform.claude.com/docs/en/build-with-claude/prompt-caching"
author: "Anthropic"
clipped: 2026-08-12
tags: [AI, Claude, cost]
---

# Anthropic Prompt Caching

원문: https://platform.claude.com/docs/en/build-with-claude/prompt-caching

## 핵심
- automatic `cache_control` 또는 explicit breakpoint (tools → system → messages 순서).
- 가격 배수: cache **read = 0.1×** (90% off); 5분 write **1.25×**; 1시간 write **2×**.
- 예: Sonnet 4.6 base $3/MTok → cache hit $0.30/MTok.
- 기본 TTL 5분(hit 시 갱신). 에이전트가 5분 이상 쉬면 1시간 TTL 검토.
- footgun: 타임스탬프/유저 메시지에 breakpoint → 매 턴 write, hit 없음.
- 코딩 어시스턴트가 주요 use case. `cache_read_input_tokens` / `cache_creation_input_tokens`로 측정.
