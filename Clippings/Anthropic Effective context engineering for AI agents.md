---
title: "Effective context engineering for AI agents"
source: "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents"
author: "Anthropic Applied AI"
clipped: 2026-08-12
tags: [AI, agents, context-engineering]
---

# Effective context engineering for AI agents

원문: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents (2025-09-29)

## 핵심
- 컨텍스트 엔지니어링 = 추론 시점의 **모든** 토큰(툴·MCP·히스토리·검색) 큐레이션. 프롬프트 문구만이 아님.
- 원칙: 원하는 결과를 최대화하는 **가장 작은 high-signal 토큰 집합** (유한 attention budget).
- **Context rot:** 윈도우가 찰수록 회상/정밀도 저하.
- just-in-time 검색(경로, grep, 쿼리) 선호 vs 코퍼스 때려넣기. Claude Code: CLAUDE.md 선탑재 + glob/grep on demand.
- 장기 레버: compaction, structured note-taking/memory, sub-agents(수만 토큰 소모 후 1–2K 요약만 반환).
- 가장 가벼운 compaction: 소비된 tool-result 제거.
