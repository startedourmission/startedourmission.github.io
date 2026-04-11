---
date: 2026-04-10
tags:
  - 정보
  - LLM
aliases: Reinforcement Learning from Human Feedback
image: "![[]]"
description: "인간의 선호도 피드백으로 훈련된 보상 모델을 사용해 LLM을 정렬하는 기법"
---

# RLHF

RLHF(Reinforcement Learning from Human Feedback, 인간 피드백으로부터의 강화 학습)는 인간 평가자의 선호도 비교 데이터로 보상 모델을 훈련하고, 이를 강화 학습 신호로 삼아 LLM을 인간의 의도와 가치에 맞게 조정하는 기법이다.

## 핵심

- 세 단계: (1) 지도 미세 조정(SFT), (2) 보상 모델 훈련, (3) PPO로 정책 최적화
- Bradley-Terry 모델로 쌍별(pairwise) 비교를 확률로 변환하여 보상 모델을 훈련한다
- KL 발산 제약으로 SFT 모델에서 너무 멀어지지 않게 정규화한다 (보상 해킹 방지)
- ChatGPT, Claude, Gemini 등 현대 LLM 정렬의 핵심 기법이다
- 인간 피드백 수집 비용과 보상 해킹이 주요 과제이다
