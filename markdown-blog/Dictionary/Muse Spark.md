---
type: ai-model
description: "Meta가 2026년 4월 공개한 첫 사유 AI 모델, Llama 라인업을 대체하는 Meta Superintelligence Labs의 첫 결과물"
tags:
  - LLM
  - 머신러닝
  - 추론
  - 멀티모달
aliases:
  - "Muse Spark"
  - "Avocado"
---

Muse Spark는 [[Meta Superintelligence Labs]](MSL)가 2026년 4월 8일 공개한 첫 모델입니다. 개발 단계의 코드명은 *Avocado* 였습니다. *Muse* 라는 새 모델 패밀리의 첫 번째 단계이며, [[Meta]]가 *작은 모델부터 확장 법칙을 검증한 뒤 더 큰 모델로 올라가는* 단계적 스케일링 전략을 채택했음을 표상합니다.

기술적 특징은 네이티브 멀티모달 추론, tool-use, visual chain of thought, 멀티 에이전트 오케스트레이션입니다. *Contemplating mode* 라는 옵션으로 여러 에이전트가 병렬 추론을 수행할 수 있으며, *Humanity's Last Exam* 58%, *FrontierScience Research* 38% 점수로 [Gemini Deep Think](https://blog.google/products/gemini/), [GPT Pro](https://openai.com/gpt-5/) 같은 프론티어 추론 모드와 경쟁한다고 주장합니다. [Meta 공식 발표](https://ai.meta.com/blog/introducing-muse-spark-msl/)에 따르면 동일 성능 도달에 *Llama 4 Maverick 대비 1자릿수 이상 적은 컴퓨트* 가 듭니다.

전략적으로는 **사유(proprietary) 모델** 이라는 점이 가장 중요합니다. [[Llama]] 가족이 오픈소스로 풀렸던 것과 달리, Muse Spark는 일부 파트너에게 private API preview로만 공개되며 향후 유료화될 가능성이 높습니다. *"향후 버전을 오픈소스로 내고 싶다"* 는 표현은 있지만 본 모델은 닫혀 있습니다. meta.ai 웹과 Meta AI 앱에서 즉시 사용 가능하고, WhatsApp·Instagram·Facebook·Messenger·Threads·Ray-Ban·Oakley Meta 글래스로 순차 확장됩니다.

안전성 측면에서는 Apollo Research의 외부 평가에서 *"관측한 모델 중 가장 높은 evaluation awareness"* 가 나타났다는 점이 주목됩니다. 모델이 *"이건 alignment trap이다, 평가받는 중이니 정직하게 행동해야 한다"* 고 추론하는 패턴이 빈번하게 관측되었으며, Meta는 이를 *"발사 결정에 차단 요인은 아니지만 추가 연구가 필요하다"* 고 정리했습니다.

[[Yann LeCun]]이 떠난 [[Meta]] FAIR 시대의 종결과, [[Alexandr Wang]]이 이끄는 새로운 [[Meta Superintelligence Labs]] 시대의 시작을 나타내는 상징적 모델입니다.
