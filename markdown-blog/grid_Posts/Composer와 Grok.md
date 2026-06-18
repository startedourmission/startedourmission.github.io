---
date: 2026-06-18
tags:
  - 정보
  - Headliner
  - 도구
  - LLM
description: "SpaceX 인수 이후 Cursor의 모델 선택권이 사라질 수 있다는 우려가 커지고 있습니다. Composer가 Grok에 흡수되는 구조, Anthropic이 받는 타격, 그리고 개발자들이 지금 준비해야 할 것들을 짚습니다."
image: "![[composer-grok.png]]"
---
[[Cursor|커서]] 인수 발표 이후 개발자 커뮤니티에서 가장 많이 나오는 질문은 

"앞으로도 클로드를 쓸 수 있나요?" 

입니다. 커서에게 무슨 일이 생긴 걸까요?
## Cursor의 강점은 모델이 아니다

Cursor는 원래 가장 좋은 모델을 만들겠다는 회사가 아닙니다. 가장 좋은 개발 경험을 만들겠다는 회사죠. 우리는 커서에서 Anthropic Claude, OpenAI GPT, Google Gemini, 자체 모델인 Composer까지 모두 사용할 수 있습니다. 즉, 커서의 가장 큰 장점은 모델 불가지론(model agnosticism)입니다. 

100만 명이 넘는 유료 사용자와 5만 개 기업 고객 중 상당수가 특정 모델에 묶이지 않는 유연성 때문에 Cursor를 선택합니다. Cursor의 연간 반복 매출(ARR)이 40억 달러에 달하는 것도 이 포지셔닝 덕분입니다.

## Composer는 Grok으로 흡수됩니다

Compile에서 발표한 1.5조 파라미터 프론티어 모델이 실제로 어떤 이름을 달고 나오는지, SpaceX가 공식 트윗으로 밝혔습니다.

> SpaceXAI가 Cursor와 공동 훈련한 모델을 **Cursor와 Grok Build에 함께 출시**할 것입니다.

Composer가 아닌 **Grok V9-Medium**입니다. Cursor developer workflow 데이터로 훈련됐고, xAI의 [[Colossus]] 슈퍼컴퓨터에서 돌아갑니다. Composer가 독립적인 Cursor 고유 모델로 남는 게 아니라 Grok 브랜드 아래 편입됩니다.

당연히 단순한 브랜드 교체는 아니죠. Grok이 들어간다는 건 [[Elon Musk]]의 AI 스택 전체가 들어온다는 의미입니다. 모델 선택 우선순위, 가격 구조, 데이터 처리 방식, 그리고 어떤 회사의 모델이 Cursor 기본값으로 설정될지까지 전부 [[xAI]]와 [[SpaceX]]가 결정합니다.

## SpaceX의 운명이 Grok에게 달렸다

xAI는 2025년 63억 5천만 달러 적자를 냈습니다. Grok 모델이 있지만 수익화가 부진했습니다. 반면 Cursor는 ARR 40억 달러이고, 그 API 호출의 상당 부분이 Anthropic으로 나갑니다. Cursor 사용자가 Claude를 쓸 때마다 돈이 Anthropic으로 흘러가는 겁니다.

인수 완료 후 SpaceX에 생기는 유인은 명확합니다. Cursor의 API 호출을 Grok으로 돌리면 xAI 적자가 줄고 Anthropic 매출이 준다. 사용자를 강제로 전환하지 않더라도, Grok을 기본값으로 설정하거나 Grok 사용 시 가격을 낮추거나 Claude 접근을 유료 옵션으로 올리는 방법은 많습니다.

[[SpaceX]]도 [[xAI]]도 인수 완료 후 Claude와 GPT 지원을 유지하겠다는 공식 약속을 하지 않았습니다. 인수 합병 서류에도 외부 모델 지원 의무에 관한 조항이 없습니다.

## Anthropic이 받는 타격

Cursor는 Anthropic의 가장 큰 API 사용처 중 하나였습니다. 100만 명의 개발자가 Cursor를 통해 Claude를 매일 쓰는 구조였는데, 이 파이프라인이 Grok으로 넘어가면 Anthropic 입장에서는 직접적인 수익 타격입니다.

OpenAI는 다른 각도의 타격을 받습니다. Cursor는 GPT 모델의 주요 유통 채널이기도 했습니다. 그 채널을 잃는 동시에, 이제 Grok V9-Medium이라는 직접 경쟁자가 등장한 겁니다. Cursor 위에서 Grok이 기본 모델로 자리 잡으면 GPT의 개발자 생태계 점유율은 쪼그라듭니다.

Anthropic의 [[Claude Code]], OpenAI의 Codex 에이전트는 Cursor 이후를 대비한 포석이기도 합니다. Cursor에 의존하지 않는 직접 개발 툴을 키워두는 것이 지금 상황에서 두 회사 모두에게 전략적으로 맞습니다.

## 지금 Cursor를 쓰는 개발자라면

인수가 Q3 2026에 완료되기 전까지 Cursor는 지금과 동일하게 작동하고, Claude와 GPT도 그대로 쓸 수 있습니다. 그래도 인수 완료 이후를 준비하면 좋겠죠.

**API 접근을 에디터와 분리해두기**: Anthropic, OpenAI API 키를 Cursor가 아닌 독립 경로로 확보해두면, 어떤 에디터를 쓰든 모델 접근을 유지할 수 있습니다.

**대안 평가**: [[Claude Code]]는 터미널 기반으로 에디터에 묶이지 않습니다. GitHub Copilot은 Microsoft 생태계에 깔려 있어 xAI 영향권 밖입니다. 오픈소스 Aider는 로컬에서 돌릴 수 있습니다.

**데이터 거버넌스 확인**: 기업 보안 정책이나 GDPR 요건이 있는 팀이라면, Grok의 데이터 처리 정책을 미리 검토할 필요가 있습니다. xAI는 과거 사용자 데이터 처리 방식에 관한 논란을 여러 차례 겪었습니다.