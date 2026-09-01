---
ready: true
type: concept
description: Reinforcement Learning with Verifiable Rewards. 정답을 결정론적으로 확인할 수 있는 영역에서 검증자 신호로 정책을 최적화하는 학습 패러다임
tags:
  - LLM
  - 강화학습
  - 추론
aliases:
  - Reinforcement Learning with Verifiable Rewards
---

Reinforcement Learning with Verifiable Rewards의 약자입니다. 답 확인기나 유닛 테스트 실행기 같은 결정론적 검증자 $V(x,y) \in \{0,1\}$를 보상으로 써서 정책을 최적화합니다.

$$\max_\theta \; \mathbb{E}_{x \sim \mathcal{D}, \, y \sim \pi_\theta(\cdot \mid x, \tau)} \left[V(x, y)\right]$$

확장이 되는 이유는 $V$가 편향 없고 무제한이며 사실상 공짜인 지도 신호를 주기 때문입니다. OpenAI o1과 DeepSeek-R1 같은 추론 모델 학습이 이 패러다임 위에 서 있습니다.

한계는 적용 범위입니다. 정답을 기계적으로 확인할 수 있는 수학과 코딩 밖으로 나가면 검증자가 없습니다. 요약이나 창작 글쓰기에서는 진짜 목표가 잠재 품질 함수인데 여기에 대응하는 $V$가 존재하지 않습니다.

기존 우회책은 $V$를 근사 평가자로 갈아 끼우는 것이었습니다. 학습된 보상 모델, LLM 심판, 루브릭 채점이 여기 속하는데 평가 편향이 들어오고 정책이 평가자 능력에 묶이며 롤아웃마다 추론 비용이 붙습니다. [[From RLVR to RLSVR - Task Transformation Induces Self-Verifiable Rewards for Open-Ended LLM Self-Improvement]]는 목표를 근사하는 대신 과제 자체를 검증 가능한 프록시 환경으로 변환하는 방향을 제안합니다.
