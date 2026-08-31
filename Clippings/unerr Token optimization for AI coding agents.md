---
title: "Token optimization for AI coding agents"
source: "https://unerr.dev/blog/token-optimization-coding-agents"
author: "unerr"
clipped: 2026-08-12
tags: [AI, coding-agents, cost]
---

# Token optimization for AI coding agents

원문: https://unerr.dev/blog/token-optimization-coding-agents (수치 인용 기준 ~2026-06)

## 핵심
- 에이전트는 채팅이 아니라 **루프**. 토큰 ≈ roundtrip × 커지는 컨텍스트 (stateless API가 히스토리 재전송).
- 측정 분할: 토큰의 **~76%**가 코드 읽기/탐색; ~12% 실행/테스트; ~12% 편집. 통상 60–80% read.
- 제곱 체감: 20 steps @1K/step ≈ 누적 입력 **210K** (20K 아님). 50 step이면 배수 30× 초과 가능.
- 캐시는 안정적 head(system/tools)에 도움. 파일 수정·툴 목록 churn이 있는 moving tail에서는 깨짐.
- 모델 라우팅: 가격차 5–25×. 최적화 단위는 $/token이 아니라 **성공한 작업당 비용**.
- 지출 범위 인용: Claude Code 평균 ~$6/dev/day; 엔터프라이즈 $150–250/mo; heavy $400–1500; 극단 >$4000.
- 순위: (1) 네비게이션/구조 (2) 짧은 루프·새 세션 (3) 안정 prefix 캐시 (4) 품질 게이트 라우팅 (5) 작업당 측정.
