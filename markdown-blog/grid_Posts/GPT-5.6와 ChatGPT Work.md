---
date: 2026-07-13
tags:
  - 정보
  - LLM
description: "OpenAI가 GPT-5.6 3종과 업무 에이전트 ChatGPT Work를 같은 날 냈습니다. 경쟁축이 모델 성능에서 업무 실행으로 옮겨간 발표입니다."
image: "![[gpt-56-chatgpt-work.png]]"
---

[[OpenAI]]가 2026년 7월 9일 GPT-5.6 제품군과 ChatGPT Work를 함께 공개했습니다. 새 모델도 모델이지만, 무게는 업무를 대신 수행하는 에이전트 쪽에 실려 있습니다.

## 세 갈래 모델

GPT-5.6은 세 갈래로 나옵니다. 가장 강력한 Sol, 속도를 노린 Luna, 그 사이에서 일상 업무의 균형을 잡은 Terra입니다. Sol에는 ultra 모드가 붙습니다. 시스템이 한 과제에 더 오래 매달리고 작업을 하위 모델에 나눠 맡기는 방식입니다.

가격은 100만 토큰 기준으로 갈립니다. Sol이 입력 5달러 출력 30달러, Terra가 2.5달러와 15달러, Luna가 1달러와 6달러입니다. 최상위와 최하위의 차이가 다섯 배입니다. 이 구조에서는 단일 모델을 고정해 쓰는 습관이 비용을 결정합니다. 반복적이고 판단이 적은 작업까지 Sol로 돌리면 요금이 다섯 배로 붙습니다.

## ChatGPT Work

발표의 실제 무게중심은 ChatGPT Work입니다. GPT-5.6과 코덱스 기술을 기반으로 하는 이 에이전트는, 연결된 앱과 파일에서 맥락을 모아 문서와 스프레드시트, 프레젠테이션 같은 업무 산출물을 만듭니다.

[[ChatGPT]]가 질문에 답을 돌려주는 단계에서, 사내 데이터에 접근해 결과물을 조립하는 단계로 넘어간 것입니다. 챗봇 경쟁이 아니라 업무 실행 경쟁으로 축이 옮겨갔다는 신호입니다. 다만 어디까지 접근시킬지는 여전히 조직이 통제해야 할 변수이고, 실제 업무 정확도는 도입 사례가 쌓여야 검증됩니다.

## 실무에서 지금 할 것

세 가지로 정리됩니다. 첫째, 작업을 난이도로 나눠 반복 작업은 Luna, 판단이 필요한 작업은 Sol로 보내고 토큰 비용을 미리 시뮬레이션합니다. 둘째, ChatGPT Work에 붙일 데이터 범위를 최소 권한으로 좁혀 시작합니다. 셋째, 산출물을 그대로 쓰지 말고 사람 검수 단계를 파이프라인에 넣습니다.

발표 시점 기준 롤아웃은 24시간에 걸쳐 점진 적용된다고 보도됐습니다. 지역과 요금제에 따라 실제 사용 가능 시점과 조건은 달라질 수 있습니다.

## 출처

- [OpenAI launches its new family of models with GPT-5.6 (TechCrunch, 2026-07-09)](https://techcrunch.com/2026/07/09/openai-launches-its-new-family-of-models-with-gpt-5-6/)
- [OpenAI releases GPT-5.6 and ChatGPT Work tool (Axios, 2026-07-09)](https://www.axios.com/2026/07/09/ai-openai-gpt-release)
- [OpenAI to publicly release GPT-5.6 (CNBC, 2026-07-08)](https://www.cnbc.com/2026/07/08/openai-expanding-gpt-5point6-ai-model-release-ending-government-limits.html)
