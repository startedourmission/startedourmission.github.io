---
date: 2026-06-10
tags:
  - LLM
  - Anthropic
description: "[[Claude]] 4.X 시리즈의 이전 버전. Fable 5와의 성능 비교 대상"
---

[[Anthropic]]의 Claude 4.X 시리즈 모델로, [[Claude Fable 5|Fable 5]] 등장 이전의 고성능 모델. 루프 구조와 메모리 활용에서 Fable 5에 비해 제한적이다.

## Fable 5와의 차이

[[Parameter Golf]] 벤치마크:
- Opus 4.7: 첫 성공 후 동일 패턴(스칼라 조정) 반복 → 약 1배 개선
- Fable 5: 구조적 변화 시도, 실패 극복 → 약 6배 개선

[[Continual Learning Bench 1.0]]:
- Opus 4.7: 검증 커버리지 약 17%
- Fable 5: 검증 커버리지 최고 73%
