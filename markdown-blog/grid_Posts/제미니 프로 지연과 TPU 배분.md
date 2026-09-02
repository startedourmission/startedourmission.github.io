---
date: 2026-08-22
ready: true
tags:
  - 정보
  - LLM
description: 구글이 5월부터 석 달째 Flash만 연달아 내놓고 3.5 Pro는 계속 미루고 있습니다. 코딩 목표 미달이라는 표면적 이유 뒤에는 TPU를 프런티어 모델(지금은 Gemini 4)에 우선 배분하는 내부 줄서기가 있습니다.
image: "![[제미니 프로 지연과 TPU 배분-thumb.png]]"
---
8월 13일 [[Gemini]] 3.7 Flash가 나왔습니다. 코딩과 에이전트용 워크호스이고, 3.6 Flash 이후 약 3주 만입니다. [발표문](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/)에는 프로 모델 일정이 없습니다. 이게 우연이 아니라는 정황이 5월부터 쌓여 있습니다.

## 3주마다 나오는 Flash

5월 19일 I/O에서 구글은 3.5 Flash를 먼저 풀면서, 3.5 Pro는 내부 사용 중이고 [다음 달에 내놓겠다](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/)고 적었습니다. 6월은 그냥 지나갔습니다. 7월 21일 발표는 3.6 Flash, 3.5 Flash-Lite, 3.5 Flash Cyber 세 개였습니다. 이번에도 프로는 "파트너와 테스트 중이며 준비되면 넓히겠다"는 말만 나왔고, 같은 글에서 [Gemini 4의 사전학습을 이미 시작했다](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/)고 밝혔습니다. "프로를 건너뛰기로 했다"고 명시한 문장은 어디에도 없습니다. 다만 석 달 연속으로 실제 일정에 오른 것은 Flash뿐입니다.

3.7 Flash의 [모델카드](https://deepmind.google/models/model-cards/gemini-3-7-flash/)를 보면 이 모델이 새 사전학습 런이 아니라는 점도 드러납니다. 3.6 Flash와 같은 학습 데이터, 같은 하드웨어를 쓰고, 추론 알고리즘만 개선한 버전입니다. 즉 구글이 지금 반복해서 내놓는 것은 매번 새로 학습한 모델이 아니라, 기존 베이스를 다듬어 재출시하는 쪽입니다.

## 왜 Pro만 밀리나?

7월 16일 블룸버그(Love, Alba)는 3.5 Pro가 내부 목표, 특히 코딩 성능에서 미달해 출시가 수개월 밀렸다고 보도했습니다. 구글은 6월에 코딩용 학습 데이터를 바꿔봤지만 결과가 기대에 못 미쳤습니다. 현직·전직 직원 10명은 Anthropic과 OpenAI가 코딩에서 앞서 있다는 내부 우려를 전했습니다.

구글 대변인의 반박은 두 갈래입니다. 다양한 모델을 빠르게 내놓고 있다는 것, 그리고 파트너들과 3.5 Pro와 업그레이드된 Flash를 함께 테스트하고 있다는 것입니다. 같은 기사는 구글의 사내 코딩 도구 자체가 클라우드, 딥마인드, 안드로이드 세 조직으로 갈라져 있다는 점도 지적합니다. 조율해야 할 팀이 많다는 뜻입니다.

정리하면 이렇습니다. 공식 설명은 "더 좋게 만들려고" 지연됐다는 쪽이고, 내부 취재는 "코딩 목표를 못 맞췄다"는 쪽입니다. 이 둘은 서로 다른 이야기가 아니라 같은 상황을 발표 전과 발표 후에서 각각 본 것에 가깝습니다.

## TPU는 어디에?

지연의 배경에는 컴퓨트 배분 문제가 있습니다. 5월에 [[순다르 피차이]]는 "당분간 우리는 컴퓨트 제약을 받는다"고 말하며, 딥마인드에 프런티어 모델용 리소스를 최우선으로 두는 이유를 "모든 일의 기반이기 때문"[이라고 설명했습니다](https://www.thestar.com.my/tech/tech-news/2026/05/19/googles-own-ai-researchers-jockey-for-access-to-itscomputing). 7월 2분기 실적 콜에서도 같은 순서를 재확인했습니다. [[Google TPU v7 Ironwood|TPU]] 배분 1순위는 프런티어 AGI 모델이고, 그다음이 검색·유튜브 같은 핵심 제품, 그다음이 클라우드(Vertex, Gemini Enterprise)와 데이터 분석·보안입니다. 고객이 칩 자체를 원하면 자체 데이터센터나 블랙스톤 프로젝트처럼 구글 밖에 TPU를 두는 쪽으로 유도합니다.

같은 콜에서 피차이는 Gemini 4를 학습 중이며 더 큰 베이스 모델이 필요하다고 말했고, 컴퓨트와 인력을 그쪽에 집중하고 있다고 덧붙였습니다. "3.5 Pro에서 칩을 빼서 Gemini 4로 돌렸다"는 문장은 어디에도 없습니다. 다만 우선순위가 다음 베팅에 가 있다는 것은 명확합니다. 3.5 Pro가 코딩 목표를 못 맞춘 채 재작업 중인 동안, 정작 최우선 컴퓨트는 그 재작업이 아니라 Gemini 4 학습에 배정되고 있다는 뜻입니다.

## 떠나가는 사용자

이 배분 순서 때문에 실제로 조직을 떠난 사례도 나옵니다. 앤드루 다이는 어느 회의에서 벤치마크 결과를 보다가 Gemini가 경쟁 모델에 막히는 장면을 봤고, 자신이 파고들고 싶은 시각 이해 연구에 쓸 컴퓨트를 사내에서 확보하기 어렵다고 판단해 퇴사했습니다. 이오아니스 안토노글루는 알파고를 만들 때는 컴퓨트가 충분했는데, Gemini 단계의 법률·코드 포스트트레이닝 작업에서는 부족을 느꼈다고 밝혔습니다. 다이는 2024년 대형 학습이 진행되는 동안 자신이 속한 일부 연구가 약 한 분기 동안 멈췄었다고도 말했습니다.

구글의 공식 입장은 우선순위에 따라 배분하며 고객·사용자·장기 연구 사이 균형을 맞춘다는 것입니다. 다만 순서가 있다는 사실 자체는 구글도 부인하지 않고, 그 순서의 맨 앞이 프런티어 모델이라는 것도 이번 실적 콜에서 직접 확인된 내용입니다.

컴퓨트가 부족하다는 서술만 보면 회사 사정이 안 좋은 것처럼 들리지만, 실적은 정반대입니다. 2분기 클라우드 매출은 247억 5천만 달러로 전년 대비 82% 늘었고, 수주 잔고는 5,140억 달러입니다. 검색 매출은 17%, 유튜브 광고는 13% 늘었습니다.

그런데 같은 분기 자유현금흐름은 마이너스 59억 달러를 기록했습니다. 2004년 기업공개 이후 첫 분기 적자입니다. 최고재무책임자 애슈케나지는 연간 설비투자 가이던스를 기존 1,800억~1,900억 달러에서 1,950억~2,050억 달러로 올렸고, 3분기에는 자체 데이터센터 공급이 모자라 제3자 용량을 빌려 임시로 메우겠다고 밝혔습니다. 매출은 늘고 있는데 그보다 빠르게 컴퓨트에 돈을 쏟아붓고 있다는 뜻이고, 이게 "컴퓨트 제약"이라는 말의 실체에 가깝습니다.

8월 5일 피차이가 사내에 보낸 메모는 이 우선순위를 그대로 반영합니다. 제미니 앱 월간 사용자 9억 5천만 명, 검색과 클라우드 실적을 앞세우고, 개발자가 에이전트 기본 모델로 무엇을 고를지는 뒤로 밀려 있습니다.

같은 8월 5일, [[데미스 하사비스]]는 딥마인드 일상 운영에서 물러나 알파벳 의장 겸 수석과학자가 됐습니다. 코라이 카부쿠오글루가 수석부사장으로 Gemini 모델, 프런티어 연구, 앱·개발자 팀을 넘겨받았습니다. 제프 딘은 회사를 떠났습니다.

피차이의 메모는 Flash 수요, 사이버보안 특화 모델, Gemma 다운로드 수를 언급하며 "프런티어에서 고쳐야 할 곳에 집중하겠다"고 적었습니다. 하사비스는 Gemini 4를 포함한 새 모델의 진전을 언급했습니다. 이 리더십 재배치가 3.5 Pro의 출시일을 앞당긴다는 근거는 없습니다. 바뀌는 것은 누가 출하 책임을 지느냐일 뿐, 우선순위 자체는 그대로입니다.

## 그래서 3.7 Flash를 쓸 이유

3.7 Flash 도입가는 입력 100만 토큰당 0.75달러, 출력 3.75달러입니다. 이 가격은 2026년 12월 31일까지만 유지되고, 2027년 1월 1일부터 1.50/7.50달러로 오릅니다.

[Artificial Analysis](https://artificialanalysis.ai/articles/gemini-3-7-time-frontier)는 이 모델을 석 달 사이 나온 세 번째 Flash로 집계하면서, 자체 지능 지수를 3.6 Flash의 52에서 3.7 Flash(high)의 56으로 평가했습니다. 작업당 평균 처리 시간은 1.7분으로, 지능 대 시간 파레토 전선 위쪽에 위치한다고 밝혔습니다.

호출량이 많은 에이전트 작업에 3.7 Flash를 써볼 이유는 이 가격과 속도 조합에 있지, 이 모델이 Pro를 대체해서가 아닙니다. Pro가 영영 안 나온다고 단정할 근거도 없습니다. 지금 구글이 개발자 앞에 내놓고 있는 것은 밀린 빈자리를 메우는 워크호스이고, 실제 컴퓨트와 노력의 우선순위는 그 빈자리가 아니라 다음 세대 모델 쪽에 가 있습니다.

---

참고: [Introducing Gemini 3.7 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/) · [Gemini 3.7 Flash model card](https://deepmind.google/models/model-cards/gemini-3-7-flash/) · [Gemini 3.5](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/) · [Gemini 3.6 Flash, 3.5 Flash-Lite, 3.5 Flash Cyber](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/) · [The next chapter of our AI momentum](https://blog.google/company-news/inside-google/message-ceo/next-chapter-ai-momentum/) · [The Star / Bloomberg 7월 16일](https://www.thestar.com.my/tech/tech-news/2026/07/17/google-gemini-launch-delayed-as-tech-falls-short-of-internal-goals) · [The Star / Bloomberg 5월 18일](https://www.thestar.com.my/tech/tech-news/2026/05/19/googles-own-ai-researchers-jockey-for-access-to-itscomputing) · [The Register Q2](https://www.theregister.com/ai-and-ml/2026/07/23/google-is-hoarding-tpus-to-develop-artificial-general-intelligence/5276755) · [CRN / Pichai TPU](https://www.crn.com/news/cloud/2026/google-ceo-on-gemini-4-allocating-tpus-ai-models-and-gemini-enterprise) · [Artificial Analysis Gemini 3.7 Flash](https://artificialanalysis.ai/articles/gemini-3-7-time-frontier)
