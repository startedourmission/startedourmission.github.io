---
type: company
description: "OpenAI 전 CTO Mira Murati가 2025년 설립한 AI 연구소, LLM 추론 비결정성 규명으로 알려짐"
tags:
  - LLM
aliases:
  - Thinking Machines Lab
  - Thinking Machines
---

Thinking Machines Lab은 [[OpenAI]] 전 CTO Mira Murati가 2025년 설립한 미국 AI 연구소입니다. OpenAI 출신을 비롯한 연구진이 합류했으며, 출범 직후 대규모 투자를 유치해 주목받았습니다.

대중적으로 알려진 계기는 2025년 9월 공개한 연구 "Defeating Nondeterminism in LLM Inference"입니다. 같은 모델을 `temperature=0`으로 1000번 돌려도 출력이 일치하지 않는 현상의 근본 원인을, 종래 가설(동시성과 부동소수점 atomic add)이 아니라 서버 부하에 따른 배치 크기 변동과 비배치불변(non-batch-invariant) 커널로 규명했습니다.

함께 공개한 배치불변 커널 구현(batch_invariant_ops)은 RMSNorm·행렬곱·attention의 reduction 순서를 배치 크기와 무관하게 고정해 비트 단위로 동일한 출력을 재현합니다. 이 작업은 vLLM·SGLang 등 추론 엔진의 결정적(deterministic) 모드 확산에 영향을 주었습니다.
