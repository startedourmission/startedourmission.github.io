---
type: person
name: Sen-Xu
description: Sina Weibo AI 연구원. VibeThinker 시리즈(1.5B, 3B) 1저자. 소형 언어 모델의 검증 가능한 추론 한계를 탐구하는 Spectrum-to-Signal Principle 설계자.
tags:
  - 인물
  - LLM
  - 추론
  - 오픈소스
aliases:
  - Sen Xu
  - 徐森
papers:
  - VibeThinker-3B - Exploring the Frontier of Verifiable Reasoning in Small Language Models
star: 10
---

Sina Weibo Inc. 소속 AI 연구원. 이메일 주소(`xusen1@staff.weibo.com`)를 통해 co-correspondence author로 등재되어 있습니다.

소형 모델이 대형 모델의 추론 능력을 갖출 수 있는지를 핵심 질문으로 삼아 연구를 이어오고 있습니다. 2025년 11월 발표한 [[VibeThinker-1.5B]] (arXiv:2511.06221)에서 다양성 기반 최적화(Diversity-Driven Optimization)로 DeepSeek R1(400배 큰 모델)을 AIME 벤치마크 세 개에서 초과하는 결과를 냈고, 단 7,800달러 규모의 포스트트레이닝 예산으로 달성한 비용 효율성으로 주목받았습니다.

2026년 6월 후속작 [[VibeThinker-3B - Exploring the Frontier of Verifiable Reasoning in Small Language Models]]에서 파라미터 수를 3B로 키워 Spectrum-to-Signal Principle(SSP)을 전면 확장합니다. 5단계 파이프라인(2단계 SFT, 다도메인 RL, Long2Short Math RL, Offline Self-Distillation, Instruct RL)을 통해 AIME26 94.3, LiveCodeBench v6 80.2, LeetCode OOD 96.1%라는 플래그십 급 수치를 3B 규모에서 실현했습니다.

[[Junlin Zhang]]과 함께 WeiboAI 팀을 이끌며, 두 논문 모두 MIT 라이선스로 오픈소스 공개했습니다. Parametric Compression-Coverage Hypothesis라는 새로운 이론적 관점도 이 작업에서 제안했습니다.
