---
date: 2026-07-03
tags:
  - 정보
  - LLM
  - 오픈소스
description: "Aramco·NVIDIA·Vista·General Catalyst 주도 $8억 시리즈C로 Together AI가 $8.3B 밸류에이션에 도달했습니다. 연간 예약 $11.5억, 500MW 컴퓨트 약정 확보. 오픈웨이트 모델 기반 AI 추론 인프라가 클로즈드 API를 대체하는 구도입니다."
image: "![[Together AI $800M 시리즈C - $8.3B 밸류, 오픈소스 AI 추론 인프라 역대 최대 라운드-thumb.png]]"
---

> 이 글은 [Together AI 공식 블로그](https://www.together.ai/blog/announcing-our-series-c) 및 [TechCrunch 보도](https://techcrunch.com/2026/07/01/neocloud-together-ai-raises-800m-leaps-to-8-3b-valuation/)를 참고하여 작성했습니다.

Together AI가 7월 1일 $8억 규모의 시리즈C 투자를 유치했습니다. 기업가치는 $8.3B(약 11조 원)으로 16개월 전 시리즈B 대비 2.5배 상승입니다. 오픈소스 AI 인프라 스타트업 단일 라운드로는 역대 최대 규모입니다.

## Together AI 포지셔닝

Together AI는 클라우드에서 오픈웨이트 모델을 서빙하는 neocloud입니다. AWS, Azure, Google Cloud 같은 범용 클라우드와 다른 점은 AI 추론에 특화된 커스텀 인프라를 자체 구축한다는 것입니다.

회사의 핵심 주장은 간단합니다. 프로토타입 단계에서는 OpenAI나 Anthropic의 API 비용이 감당 가능해 보이지만, 실제 프로덕션에 올라가면 비용 구조가 달라진다는 것입니다. 그 시점에서 [[DeepSeek]], MiniMax, Kimi, Nemotron, GLM 같은 오픈웨이트 모델을 Together AI 인프라에 올리면 클로즈드 API 대비 6배에서 20배 저렴하게 동등한 성능을 낼 수 있다고 합니다. 고객사 Decagon의 사례가 구체적으로 인용됩니다. AI 고객 서비스 플랫폼인 Decagon은 Together AI로 전환한 뒤 추론 비용이 6분의 1로 줄었습니다.

현재 고객사로는 Cursor, Cognition, Eleven Labs, Suno, Decagon이 있습니다. 마지막 분기 연간 예약금은 $11.5억입니다.

## 오픈웨이트 모델의 부상

Together AI의 시리즈C 타이밍은 시장 변화와 맞물립니다. 회사가 인용한 수치에 따르면 업계 전반에서 오픈소스 모델 사용이 최근 12개월 사이 3배로 늘었습니다.

이 변화의 배경은 모델 품질의 수렴입니다. 2024년까지만 해도 GPT-4급 작업은 OpenAI나 Anthropic의 API 없이는 불가능하다는 인식이 지배적이었습니다. 2026년 현재 [[DeepSeek]], Kimi, [[Qwen]], MiniMax 같은 오픈웨이트 모델들이 특정 벤치마크에서 클로즈드 프런티어 모델에 근접하거나 넘어서는 사례가 나오고 있습니다.

오픈웨이트 모델에는 또 다른 이점이 있습니다. 파인튜닝이 가능하고, 특정 도메인에 맞게 후처리할 수 있습니다. 클로즈드 API는 프롬프트 엔지니어링 범위 밖의 커스터마이징을 허용하지 않습니다. 기업 입장에서 고객 데이터를 학습에 반영하거나, 특정 산업 용어를 모델에 깊이 박아 넣으려면 오픈웨이트가 유일한 선택지입니다.

## 인프라 기술 스택

Together AI가 단순 GPU 렌탈 회사와 다른 이유는 자체 추론 최적화 스택을 개발한다는 점입니다.

공개된 기술 컴포넌트는 세 가지입니다. FlashAttention-4는 [[NVIDIA]] Blackwell 아키텍처에 맞게 최적화한 어텐션 커널입니다. Together Megakernel은 자체 개발한 추론 커널 라이브러리입니다. `together.compile`은 모델을 Together 인프라에 최적화된 형태로 컴파일하는 도구입니다.

성능 주장으로는 코딩 에이전트 워크로드에서 경쟁 오픈소스 엔진 대비 처리량이 31% 높다는 수치가 있습니다. 현재 87개 클러스터를 운영하며, 하루 10억 건의 추론 호출을 처리합니다.

## 투자 라운드 세부

라운드 리드는 아람코 벤처스(Aramco Ventures, 사우디아라비아 국영 석유기업 아람코의 VC 부문)입니다. 참여 투자자는 [[NVIDIA]], Vista Equity Partners, General Catalyst, Emergence Capital, Salesforce Ventures, Schneider Electric, Pegatron, March Capital, Lux Capital, PSP Partners 등입니다.

에쿼티 $8억 외에 투자자들이 별도로 500MW 이상의 컴퓨트 용량을 독립 법인으로 확보하는 약정도 함께 이루어졌습니다. 즉 이번 라운드는 현금 투자와 인프라 실물 확보가 동시에 이루어진 구조입니다. 500MW는 대형 데이터센터 캠퍼스 수준의 전력량으로, 향후 5년간 50배 용량 확장 목표에 대응하는 규모입니다.

## 경쟁 구도

neocloud 섹터에 자본이 몰리는 현상이 가속되고 있습니다. 비슷한 시기의 경쟁사 라운드로 Upscale AI $5억 시리즈A 연장, AMD GPU 클러스터 전문 TensorWave의 $3.5억 시리즈B가 있습니다.

이 섹터가 성장하는 근본 이유는 두 가지 구조적 요인입니다. 하나는 오픈웨이트 모델의 품질 격차 축소입니다. 클로즈드 API 없이도 많은 프로덕션 태스크를 처리할 수 있게 되면서, 기업들이 비용 효율적인 대안을 찾기 시작했습니다. 다른 하나는 데이터 주권 수요입니다. 의료, 법률, 금융 규제 영역에서는 고객 데이터를 외부 API로 라우팅하는 것 자체가 컴플라이언스 문제가 됩니다. 자체 인프라에 오픈웨이트 모델을 올리는 방식이 유일한 규정 준수 선택지인 경우가 많습니다.

Together AI의 다음 과제는 기술 스택의 실질적 우위를 유지하는 것입니다. GPU 렌탈 자체는 차별화가 어렵기 때문에, 추론 최적화 커널의 성능 격차가 커스터머 리텐션의 핵심입니다.

---

이 글은 [Together AI 공식 블로그](https://www.together.ai/blog/announcing-our-series-c)의 관점에서 작성되었습니다.
