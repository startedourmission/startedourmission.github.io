---
date: 2026-07-15
tags:
  - 정보
  - 오픈소스
  - LLM
  - 추론
description: "Mistral이 Lean 4 정리증명과 코드 검증에 특화된 모델 Leanstral 1.5를 Apache-2.0으로 공개했습니다. PutnamBench 672문제 중 587개를 풀고 miniF2F를 포화시켰다고 주장합니다. AI가 코드의 정확성을 형식적으로 증명하는 영역이 오픈소스로 열렸습니다."
image: "![[leanstral-1-5-thumb.png]]"
---

> 이 글은 [Mistral의 Leanstral 1.5 발표](https://mistral.ai/news/leanstral-1-5/)를 참고했습니다.

Mistral이 Leanstral 1.5를 오픈소스로 공개했습니다. Lean 4 기반의 정리증명과 코드 검증에 특화된 모델이고, 라이선스는 Apache-2.0입니다. Hugging Face와 무료 API로 받을 수 있습니다.

## 형식 증명이라는 과제

Lean 4는 수학 정리와 프로그램의 정확성을 기계가 검증할 수 있게 형식적으로 기술하는 언어입니다. 사람이 증명을 짜는 데 품이 많이 들어서, 여기에 AI를 붙이려는 시도가 이어져 왔습니다. Leanstral 1.5는 그 특화 모델입니다. 아키텍처는 전문가 혼합(MoE)으로, 128개 전문가 중 토큰당 4개만 활성화해 활성 파라미터는 약 60억 규모입니다. 총량은 크지만 실제 추론 비용은 낮게 유지하는 구성입니다.

## 성적

Mistral은 형식 검증 벤치마크에서 최상위 성능을 주장합니다. PutnamBench 672문제 중 587개를 풀었고, miniF2F는 포화시켰다고 밝혔습니다. FATE 계열에서는 FATE-H 87%, 더 어려운 FATE-X 34%를 기록했습니다.

수치보다 눈에 띄는 것은 실제 적용 사례입니다. 57개 저장소를 대상으로 돌린 테스트에서 그동안 알려지지 않았던 버그 5건을 찾아냈다고 합니다. 이 부분은 Mistral 발표를 인용한 보도를 통해 전해진 내용입니다.

## 왜 중요한가

코드가 맞다는 것을 테스트로 확인하는 것과 형식적으로 증명하는 것은 신뢰 수준이 다릅니다. 앞은 확인한 경우만 보장하고, 뒤는 조건 안에서 항상 성립함을 보입니다. Leanstral 1.5는 그 형식 증명 쪽을 AI로 밀어붙이는 시도이고, 그것을 오픈 가중치와 무료 API로 풀었습니다. 신뢰성이 중요한 소프트웨어나 형식 수학에 관심 있는 쪽에는 바로 만져볼 수 있는 오픈소스 선택지가 하나 생긴 셈입니다.

---

출처: [Leanstral 1.5 - Proof Abundance for All (Mistral)](https://mistral.ai/news/leanstral-1-5/) / [MarkTechPost](https://www.marktechpost.com/2026/07/03/mistral-ai-releases-leanstral-1-5-an-apache-2-0-lean-4-code-agent-model-solving-587-of-672-putnambench-problems/)
