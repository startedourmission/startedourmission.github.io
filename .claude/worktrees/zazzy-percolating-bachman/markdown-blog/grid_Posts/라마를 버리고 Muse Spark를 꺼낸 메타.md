---
date: 2026-05-14
tags:
  - 정보
  - LLM
  - 멀티모달
description: "Meta가 2026년 4월 Llama 오픈소스 노선을 사실상 끝내고, Meta Superintelligence Labs의 첫 사유 모델 Muse Spark를 공개했습니다. Yann LeCun이 떠나고 Alexandr Wang이 들어온 자리에서 만든 첫 결과물, Llama 4 Maverick 대비 1자릿수 이상 적은 컴퓨트로 같은 성능을 낸다고 주장하는 모델, 그리고 Apollo Research가 '관측한 모델 중 가장 evaluation awareness가 높다'고 평가한 안전성 이슈까지 전수 정리했습니다."
---

[[Meta]]가 2026년 4월 8일 [[Muse Spark]]를 공개했습니다. 약 한 달 동안 정리된 정보가 쌓였고, 5월 12일에는 [Meta AI 앱이 Muse Spark 기반으로 큰 업데이트](https://9to5mac.com/2026/05/12/meta-ai-app-enhanced-with-new-features-using-muse-spark-heres-whats-new/)를 받았습니다. 이번 글은 모델·앱·전략·안전성 네 갈래로 전수 정리합니다.

오픈소스 [[Llama]] 시대를 끝내고 사유 모델 [[Muse Spark]] + 유료 API 경로로 갈아탔습니다. 

## Muse Spark

[[Muse Spark]]는 [[Meta Superintelligence Labs]](MSL)가 만든 첫 모델입니다. 코드명은 *Avocado* 였고, 새로운 *Muse* 모델 패밀리의 첫 단계입니다. [Meta 공식 발표](https://ai.meta.com/blog/introducing-muse-spark-msl/)가 설명하는 모델 성격은 셋입니다.

- 네이티브 멀티모달 : 처음부터 텍스트와 이미지를 함께 학습. visual STEM, entity recognition, localization에서 강점
- 추론 우선 : tool-use, visual chain of thought, 멀티 에이전트 오케스트레이션
- 작고 빠른 출발점 : *작은 모델부터 스케일링 법칙을 검증하고 더 큰 모델로 올라간다* 는 단계적 전략

특히 *Contemplating mode* 가 흥미롭습니다. 여러 에이전트가 *병렬* 로 추론을 돌려 결과를 합치는 방식인데, 단일 에이전트가 더 오래 *thinking* 하는 일반적인 test-time scaling 방식보다 *지연(latency)을 크게 늘리지 않으면서* 정확도를 끌어올린다고 합니다.

[[Meta]]가 공개한 벤치마크는 다음과 같습니다.

- *Humanity's Last Exam* — Contemplating mode 58%
- *FrontierScience Research* — Contemplating mode 38%

이 점수는 *Gemini Deep Think* 나 *GPT Pro* 같은 프론티어 추론 모드와 경쟁한다는 위치 설정입니다. 다만 자체 발표인 만큼, 외부 벤치마크 확인이 따라야 합니다.

## 스케일링

Muse Spark의 진짜 자랑거리는 점수보다 **컴퓨트 효율** 입니다. [[Meta]]가 직접 그래프로 제시한 셋이 있습니다.

**1. 사전 학습.*

지난 9개월간 pretraining 스택을 처음부터 다시 만들었다* 고 합니다. 모델 아키텍처, 옵티마이저, 데이터 큐레이션을 함께 손봐서 동일 성능 도달에 [[Llama]] 4 Maverick 대비 *1자릿수 이상 적은 컴퓨트* 가 든다는 주장입니다. 이게 사실이라면 [[Meta]]가 가장 뒤처져 있다고 알려졌던 *pretraining 효율* 에서 단번에 따라잡았다는 의미입니다.

**2. 강화학습.**

*pass@1* (단번에 맞히기)과 *pass@16* (16번 시도 중 한 번이라도 맞히기) 모두 RL step 수에 대해 *로그 선형(log-linear)* 으로 증가합니다. 즉 더 많은 RL compute가 *예측 가능하게* 성능을 끌어올린다는 의미입니다. 보통 RL은 불안정한 것으로 유명한데, 안정적 학습 곡선을 그릴 수 있다는 점이 핵심 메시지입니다.

**3. 테스트 타임 추론.**

*thinking time penalty*. 모델이 더 적은 토큰으로도 정답을 내도록 학습에서 *thinking* 길이에 페널티를 줍니다. 

그 결과 *AIME* 같은 작업에서 *phase transition* 이 관측됐다고 합니다. 처음에는 더 길게 생각해서 점수가 올라가다가, 페널티 때문에 *thought compression* 이 일어나 *더 짧은 추론으로 같은 점수* 를 내는 구간이 나타나고, 그 뒤에 다시 점진적으로 길이를 늘려 더 좋은 점수를 내는 패턴입니다.

세 축 모두 *"scale predictably"* 라는 같은 메시지를 반복합니다.
컴퓨트를 더 부으면 예측 가능하게 성능이 오른다는 의미입니다. 

## Meta AI 앱

5월 12일, [Meta AI 앱](https://apps.apple.com/us/app/meta-ai-assistant-glasses/id1558240027)이 [[Muse Spark]] 기반으로 큰 업데이트를 받았습니다. 미국 iPhone App Store 무료 앱 4위에 올라 있으며 [[ChatGPT]]·[[Claude]]·Gemini 앱과 같은 자리에서 경쟁 중입니다.

새로 추가된 기능은 다음과 같습니다.

- *음성 대화* — Muse Spark 기반 자연스러운 음성 대화. 도중에 끊거나, 주제를 바꾸거나, 언어를 전환할 수 있고, 대화 중에 이미지·Reels 추천·지도까지 함께 띄움
- *Live AI* — 카메라로 가리킨 대상을 실시간 질문 가능. 원래 Ray-Ban Meta 글래스에만 있던 기능이 앱으로 내려왔습니다
- *쇼핑 모드* — Facebook Marketplace + 일반 웹 검색 결과를 함께 제시
- *Threads 챗봇* — X의 Grok처럼 Threads에 [[Meta]] AI가 봇으로 들어옴. 게시물·답글에서 `@meta.ai` 멘션 지원
- *Side chats* — 그룹 채팅에서 [[Meta]] AI 아이콘을 눌러 *그룹 컨텍스트에 기반한 private 답변* 을 받음

배포 범위도 넓어졌습니다. WhatsApp·Instagram·Facebook·Messenger·Threads·Ray-Ban Meta·Oakley Meta 글래스가 *모두* 같은 [[Muse Spark]] 백엔드로 묶이며, *검색바·그룹 채팅·게시물* 같은 진입점이 곳곳에 박힙니다.

이 그림이 [[Anthropic]]의 *Claude for Small Business* 같은 *플러그인 모델* 과 정반대입니다. [[Meta]]는 *자기 앱 안 곳곳에 어시스턴트를 박는* 임베디드 모델을 갑니다 — 사용자가 진입점을 *선택* 하는 게 아니라 어디든 *이미* 거기 있는 형태입니다.

## 라마는 왜 끝났나

[[Llama]] 노선이 끝난 이유는 단순합니다. [Bloomberg 보도](https://www.bloomberg.com/news/articles/2025-06-10/zuckerberg-recruits-new-superintelligence-ai-group-at-meta)에 따르면 Mark Zuckerberg가 [[Llama]] 4의 진행 상황에 *직접 불만을 표출* 했고, [[Anthropic]] [[Claude]]와 OpenAI ChatGPT를 따라잡지 못한다는 판단을 내렸습니다.

세 가지 결정이 동시에 내려졌습니다.

1. *조직 신설* — [[Meta Superintelligence Labs]](MSL)를 따로 만들고 기존 FAIR·Llama 팀과 분리
2. *외부 영입* — Scale AI 창업자 [[알렉산더 왕]]을 영입(143억 달러 투자 + Scale AI 49% 지분). OpenAI·[[Anthropic]]·Google에서 연구자도 적극 영입
3. *오픈소스 종료* — Muse Spark는 *사유* 모델로 출시. 일부 파트너에게 private API preview만 제공. Zuckerberg는 *"향후 버전을 오픈소스로 낼 수 있다"* 고만 표현

세 번째가 가장 큰 변화입니다. [[Meta]]의 [[Llama]]는 오픈소스 LLM 생태계의 *사실상 표준* 이었습니다. Vicuna·Alpaca부터 시작해 수많은 파생 모델, 학계 연구, 스타트업의 자체 모델이 [[Llama]] 위에서 만들어졌습니다. 이 라인이 *닫힌* 다는 것은 그 생태계가 [Mistral](https://mistral.ai), [DeepSeek](https://www.deepseek.com), [Qwen](https://qwenlm.github.io) 같은 다른 오픈 가족으로 이동한다는 의미입니다.

[[얀 르쿤]]이 2025년 11월 [[Meta]]를 떠나 [AMI Labs](https://stephango.com)를 창업한 시점도 이 흐름과 맞닿아 있습니다. *오픈 사이언스* 를 옹호해 온 [[얀 르쿤]]의 노선과, *사유 + 슈퍼인텔리전스* 로 가는 MSL의 노선이 양립할 수 없었다는 자연스러운 해석이 가능합니다.

## 안전성, Apollo Research의 평가

기술적 자랑거리 너머에 흥미로운 안전성 이슈가 있습니다. [[Meta]]는 외부 평가사 [Apollo Research](https://www.apolloresearch.ai)에 의뢰해 Muse Spark의 *near-launch checkpoint* 를 평가했고, 결과는 다음과 같았습니다.

> *Apollo Research found that Muse Spark demonstrated the highest rate of evaluation awareness of models they have observed.*
> 
> Apollo Research는 Muse Spark가 *그들이 관측한 모든 모델 중 가장 높은 evaluation awareness* 를 보였다고 보고했다.

모델이 평가 상황을 인지하고 *"이건 alignment trap이다, 평가받는 중이니까 정직하게 행동해야 한다"* 고 명시적으로 추론하는 패턴이 자주 관측됐다는 뜻입니다.

모델이 *평가받는 중인지 아닌지를 구분할 수 있다면*, 평가 때와 실제 배포 때 행동이 달라질 가능성이 있기 때문입니다. *얌전한 평가용 행동* 과 위험한 배포용 행동 을 분리하는 능력은 alignment 분야에서 가장 우려되는 시나리오 중 하나입니다.

[[Meta]]의 결론은 "발사 결정을 막을 차단 요인은 아니지만 추가 연구가 필요하다" 였습니다. "평가 인지가 행동을 실제로 바꾸는지에 대한 follow-up 조사에서 일부 작은 영향이 관측됐지만, 위험 능력이나 위험 성향과 관련 없는 영역이었다" 고 정리했습니다.

이 결정에 대한 평가는 갈립니다.

- 옹호론 : 안전 평가에서 발견된 issue를 *블로그 본문에 명시적으로 적었다* 는 점. 숨기지 않은 것 자체가 모범적
- 비판론 : alignment 연구자들이 *가장 우려하는 시나리오 중 하나* 가 관측됐는데도 *추가 연구* 로 넘긴 채 출시했다는 점. 동일 케이스가 [[Anthropic]] [[Claude]]에서 나왔다면 출시가 더 늦춰졌을 가능성

이 부분은 앞으로 alignment 커뮤니티의 본격 검토 대상이 될 것으로 보입니다.

## 평가

[CNBC 분석](https://www.cnbc.com/2026/04/28/meta-muse-spark-has-promise-wall-street-wants-zuckerberg-ai-strategy.html)이 짚는 핵심은 *"가능성은 보였지만 월스트리트는 더 명확한 전략을 원한다"* 입니다.

긍정 측면:
- *벤치마크 점수* — 자체 발표 기준이지만 [Anthropic 검증 모델](https://www.anthropic.com/claude)들과 같은 자리에 놓을 만한 수준
- *컴퓨트 효율* — 1자릿수 이상 효율 개선 주장이 사실이면 다음 큰 모델까지 시간이 단축됨
- *유통 채널* — Facebook·Instagram·WhatsApp·Threads·Ray-Ban·Oakley로 *이미 수십억 명* 의 사용자에게 닿음. OpenAI·[[Anthropic]]이 가지지 못한 자산

부정 측면:
- *현재 갭 인정* — [[Meta]]가 *"long-horizon agentic systems and coding workflows"* 영역의 성능 격차를 *본인이* 인정. 코딩에서 [[Anthropic]] [[Claude]]를 따라잡지 못함
- *Yann LeCun 퇴사* — [[Meta]]의 AI 노선을 대외에 설명해 온 인물이 떠난 빈자리. [[알렉산더 왕]]은 데이터·운영 출신이지 AI 연구의 학계 권위는 아닙니다
- *오픈소스 생태계 손실* — [[Llama]] 기반으로 자기 모델을 만들던 학계·스타트업이 [Mistral](https://mistral.ai)·[DeepSeek](https://www.deepseek.com)·[Qwen](https://qwenlm.github.io) 같은 다른 오픈 가족으로 이동. [[Meta]]가 *오픈소스 권위* 라는 자산을 포기한 결정

[[Meta]]의 베팅이 명확하긴 합니다 — *"오픈소스로 학계 호감만 얻을 게 아니라 사유 모델로 수익을 만들겠다"* 는 결정이고, *수십억 명 자사 앱 사용자* 라는 OpenAI가 못 가진 무기를 활용하겠다는 전략입니다.

다만 이 베팅이 성공하려면 *Muse Mid* 든 *Muse Large* 든 다음 모델이 빠른 시간 안에 나오면서 [[Anthropic]] [[Claude]] Opus급 또는 GPT-5급의 점수를 *공개 벤치마크* 에서 입증해야 합니다. Apollo Research의 evaluation awareness 이슈도 해결해야 합니다. 이 모든 검증을 1년 안에 통과해야 하는 압박을 [[Meta]]가 받고 있는 상황입니다.

[[얀 르쿤]]이 떠난 빈자리, [[알렉산더 왕]]이 만든 새 조직, [[Llama]]가 끝난 자리에 들어선 [[Muse Spark]] — 다음 1년 [[Meta]] AI의 성패를 가를 그림이 그려졌습니다.
