---
type: ai-model
description: "양방향 트랜스포머 인코더로 NLP 전반을 끌어올린 구글의 사전학습 언어 모델"
tags:
  - LLM
  - NLP
aliases:
  - Bidirectional Encoder Representations from Transformers
---

BERT(Bidirectional Encoder Representations from Transformers)는 2018년 [[Google]]이 발표한 [[트랜스포머]] 인코더 기반 사전학습 언어 모델입니다.

마스킹된 토큰을 양방향 문맥으로 예측하는 방식(Masked Language Modeling)으로 사전학습한 뒤 다운스트림 과제에 미세조정하는 패러다임을 정립했습니다. 공개 직후 다수의 NLP 벤치마크 기록을 갈아치우며, [[GPT]]와 함께 사전학습 시대를 연 양대 모델로 꼽힙니다.
