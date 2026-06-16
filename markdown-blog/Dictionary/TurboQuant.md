---
type: ai-model
description: "Google Research의 KV cache 6× 압축 알고리즘, ICLR 2026 발표, 학습 없이 3-bit 양자화에 정확도 손실 zero"
tags:
  - LLM
  - 머신러닝
  - 오픈소스
aliases:
  - "TurboQuant"
  - "PolarQuant"
---

TurboQuant는 [Google Research](https://research.google)의 *Amir Zandieh* (Research Scientist)와 [[Vahab Mirrokni]] (Google Fellow, VP)가 개발한 LLM KV cache 압축 알고리즘입니다. ICLR 2026에서 발표되며, arXiv ID는 2504.19874입니다. [공식 발표](https://research.google/blog/turboquant-redefining-ai-efficiency-with-extreme-compression/)에 따르면 KV cache 메모리를 6배 이상 압축하면서 정확도 손실이 *거의 zero* — needle-in-a-haystack 검색에서 unquantized와 동일한 점수를 받습니다.

핵심 기법은 *random rotation* + *PolarQuant* 두 단계입니다. 데이터 벡터를 무작위 회전시켜 기하 구조를 단순화한 뒤, 표준 좌표가 아닌 *극좌표(polar coordinates)* 로 변환해 *반지름(magnitude)* 과 *각도(direction)* 를 분리합니다. 각도 분포가 예측 가능하고 집중돼 있어, 기존 양자화기가 필요로 하는 비싼 per-block 정규화 단계를 건너뛸 수 있습니다.

성능 측면에서는 Nvidia H100 GPU에서 unquantized keys 대비 *최대 8배* 처리 속도를 냅니다. 학습이나 fine-tuning이 필요 없고 추론 런타임 오버헤드도 무시할 수 있어, 프로덕션 inference와 대규모 벡터 검색 시스템에 그대로 적용할 수 있습니다.

이 알고리즘이 공개되자 메모리 칩 주가가 흔들렸다는 보도가 나왔습니다 — *"같은 GPU에서 6배 큰 모델을 굴릴 수 있다"* 는 메시지가 메모리 수요 전망에 직접 충격을 줬기 때문입니다. [[llama.cpp]] 같은 추론 엔진에서도 빠르게 통합 논의가 진행됐습니다.

TurboQuant는 KV cache 압축뿐 아니라 벡터 검색(near-neighbor search)에도 동일하게 적용되며, *vector DB* 운영자에게도 직접 이득을 줍니다.
