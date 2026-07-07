---
type: tool
description: Anthropic의 공식 에이전트 SDK, Python·TypeScript로 Claude 기반 자동화·에이전트를 만들 때 쓰는 라이브러리
tags:
  - 도구
  - LLM
  - 에이전트
aliases:
  - "Claude Agent SDK"
  - "Anthropic Agent SDK"
---

Claude Agent SDK는 [[Anthropic]]이 공개한 공식 에이전트 개발 라이브러리로, [[Claude]] 모델을 외부 앱·자동화에 통합할 때 쓰는 Python·TypeScript SDK입니다. [[Claude Code]]의 비대화형 모드(`claude -p`)와 같은 결제·실행 인프라를 공유합니다.

SDK는 사용자가 자신의 Claude 구독으로 인증하거나, [Claude Developer Platform](https://console.anthropic.com)의 API 키로 인증하는 두 가지 경로를 제공합니다. 전자는 일반 사용자가 만든 자동화·외부 앱이 개인 구독을 활용하게 하는 데 쓰이고, 후자는 팀의 공유 프로덕션 파이프라인에서 pay-as-you-go로 청구되는 운영 형태에 쓰입니다.

2026년 6월 15일부터 SDK 사용량은 Claude 구독 플랜의 대화형 한도에서 빠지고, 별도 월간 크레딧으로 분리됩니다. Pro는 월 20달러, Max 5x는 100달러, Max 20x는 200달러, Team Premium은 100달러, seat-based Enterprise Premium은 200달러 크레딧이 자동 충전됩니다. 크레딧이 소진된 뒤에는 extra usage가 켜져 있다면 표준 API 요율로 추가 청구가 되고, 꺼져 있다면 호출이 일시 중지됩니다.

크레딧 액수는 *개인의 실험·자동화* 규모로 설계되어 있어, 팀의 공유 운영 자동화는 API 키 기반 pay-as-you-go로 운영하는 것이 안내됩니다. SDK는 [GitHub Actions](https://github.com/anthropics/claude-code-action) 연동에도 동일하게 적용됩니다.
