---
type: concept
description: Group Relative Policy Optimization. 가치 함수 없이 그룹 내 상대 보상으로 정책을 갱신하는 강화학습 기법
tags:
  - 강화학습
  - LLM
aliases:
  - GRPO
  - Group Relative Policy Optimization
---

GRPO(Group Relative Policy Optimization)는 별도의 가치 함수(critic) 없이, 같은 프롬프트에 대해 여러 응답을 샘플링한 뒤 그 그룹 안에서의 상대적 우열로 이점(advantage)을 추정하는 강화학습 기법입니다. PPO가 요구하는 가치 네트워크를 없애 메모리와 연산을 줄이면서도 안정적인 정책 갱신을 노립니다.

DeepSeek가 추론 모델 학습에서 널리 알리면서 LLM의 후처리 학습에 자주 쓰입니다. 정답 여부 같은 검증 가능한 보상과 결합해 추론·코딩 능력을 끌어올리는 데 효과적이었습니다.

최근에는 단일 응답 보상을 넘어 멀티턴 에이전트 학습으로 확장됩니다. [[MetaForge - A Self-Evolving Multimodal Agent that Retrieves, Adapts, and Forges Tools On Demand]]는 멀티턴 GRPO에 정답·도구 검색·파라미터 적응·호출 필요성·스킬 생성·형식 등을 묶은 복합 보상을 설계해, 에이전트가 도구를 적응적으로 쓰도록 학습시킵니다.
