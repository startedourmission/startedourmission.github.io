---
date: 2026-08-31
ready: false
tags:
  - 정보
  - LLM
  - 도구
description: "SpaceX의 Cursor 인수가 8월에 완결된 뒤 OpenAI가 모델 공급 계약을 종료하겠다고 통보했습니다. 차단 예정일은 11월 12일이고, 같은 상황에서 Anthropic은 반대로 갔습니다."
image: "![[openai-cursor-cutoff-thumb.png]]"
---

8월 29일, [[OpenAI]]가 [[Cursor]]에 모델을 공급하는 계약을 종료하겠다고 [[SpaceX]]에 통보했습니다. 제안된 차단일은 2026년 11월 12일입니다.

6월의 인수 발표 때 나왔던 이야기가 아닙니다. 그 거래는 8월 중순에 완결됐고, 이건 완결 2주 뒤에 나온 후속 조치입니다.

## 사유

OpenAI가 든 이유는 성능도 단가도 아닙니다. 신뢰입니다. 머스크 계열사와의 과거 경험상 SpaceX가 이용약관 범위 안에서 자사 기술을 쓸 것이라고 확신할 수 없다는 것입니다.

계약 종료가 아니라 계약을 감아 내리는(wind down) 형태입니다. 즉시 차단이 아니라 11월 12일까지 유예를 두고, 그 사이 Cursor가 협상 중이라고 알려져 있습니다.

이 판단의 형식 자체는 이상하지 않습니다. 경쟁사가 자사 모델의 유통 채널을 통째로 소유하게 됐으니까요. 이상한 건 옆에서 정반대 판단이 나왔다는 점입니다.

## 갈린 판단

[[Anthropic]]은 같은 상황에서 공급을 유지하기로 했습니다. 공동창업자 톰 브라운이 Claude 모델을 Cursor에 계속 공급하고 뒤에 컴퓨트를 더 붙이겠다고 밝혔습니다.

보도들은 대체로 이 대비를 "OpenAI는 머스크와 사이가 나쁘고 Anthropic은 아니다"로 정리합니다. 인물 구도로 보면 그렇게 읽힙니다. 그런데 한 가지를 같이 놓으면 다른 게 보입니다.

Anthropic은 SpaceX로부터 컴퓨트를 빌려 씁니다. 5월 6일에 맺은 계약으로 Colossus 1 데이터센터의 용량 전체를 쓰고 있고, 규모는 300MW 이상, GPU 22만 장 이상입니다. Claude의 사용 한도를 올릴 수 있었던 것도 이 계약 덕분입니다.

그러니까 Anthropic은 SpaceX에 모델을 팔면서 동시에 SpaceX로부터 연산을 삽니다. 여기서 공급을 끊는다는 건 자기 인프라 공급자와 척지는 일입니다. OpenAI에는 그런 연결이 없습니다.

판단이 갈린 자리는 이념이 아니라 의존 구조입니다. 두 회사가 머스크를 다르게 봐서가 아니라, 머스크 쪽에 걸려 있는 것이 다릅니다.

## 5퍼센트

여기서 이 사건의 실제 무게가 나옵니다.

Cursor CEO 마이클 트루엘이 밝힌 수치로, OpenAI 모델은 Cursor 사용자 트래픽의 약 5퍼센트입니다.

이 숫자가 맞다면 11월 12일 차단이 Cursor에 주는 타격은 거의 없습니다. 나머지 95퍼센트는 이미 Claude와 Gemini, 그리고 Cursor 자체 모델 쪽으로 가 있다는 뜻이니까요.

수치의 출처는 CEO의 소셜 발언이고 자사 집계입니다. "사용자 트래픽"이 요청 수인지 토큰 수인지 매출 기준인지도 밝혀지지 않았습니다. 그래도 방향은 다른 사실들과 어긋나지 않습니다. Cursor는 2026년 내내 자체 모델 쪽으로 무게를 옮겨 왔습니다. Composer 2.5가 있고, 인수 이후 Grok 4.5와 4.6이 자체 모델 풀에 들어왔고, 6월 Compile에서는 Colossus에서 처음부터 학습시킨 1.5조 파라미터 프론티어 모델을 공개했습니다.

그래서 이 사건을 시점으로 놓고 보면 순서가 뒤집힙니다. OpenAI가 11월 12일에 유통 채널을 잃는 것이 아닙니다. 이미 잃은 상태였고, 11월 12일은 그 사실을 계약서에 반영하는 날입니다.

## 사용자 쪽

보도 대부분이 빠뜨리는 부분입니다. 5퍼센트라도 그 5퍼센트를 쓰던 사람은 있습니다.

주의할 점 하나가 있습니다. 개인 API 키를 꽂는 방식(BYOK)으로는 접근이 유지되지 않습니다. 차단 대상이 개별 사용량이 아니라 "고객사 Cursor"이기 때문입니다. 키를 따로 준비해 두면 된다고 생각하고 있었다면 그 계획은 성립하지 않습니다.

지금 할 수 있는 것은 이 정도입니다.

| 할 일 | 이유 |
| --- | --- |
| 기본 모델을 Claude나 Gemini로 명시 지정 | Auto나 Router에 두면 차단일까지 OpenAI 모델로 라우팅될 수 있습니다 |
| BYOK를 대안으로 두지 않기 | 차단이 계정이 아니라 고객사 단위입니다 |
| 대체 하네스를 11월 전에 실제로 돌려보기 | [[Claude Code]], OpenCode, Codex CLI를 이론이 아니라 검증된 폴백으로 만들어 둡니다 |
| 모델 이름을 설정 파일로 빼기 | 코드베이스에 하드코딩돼 있으면 다음번 공급 변경 때 같은 일을 반복합니다 |

8월 29일 기준으로 Cursor 쪽의 공식 마이그레이션 정책이나 크레딧 보상 공지는 CEO의 소셜 발언 외에 나온 것이 없습니다.

## 남는 것

Cursor가 모델 불가지론을 내세워 온 회사라는 점이 이 사건의 아이러니입니다. 어떤 모델이든 골라 쓸 수 있다는 것이 유료 사용자 100만 명과 기업 고객 5만 곳을 모은 포지셔닝이었습니다.

그 선택지 하나가 공급자 판단으로 사라집니다. 사용자가 고른 게 아니라 위쪽에서 정해진 것입니다. 5퍼센트라 체감이 작을 뿐, 구조는 그대로 남습니다. 모델 불가지론은 모델 회사들이 계속 팔아줄 때만 성립하는 성질이었습니다.

Cursor가 2026년에 자체 모델과 자체 인프라 쪽으로 그렇게 서둘러 움직인 이유가 여기 있었다고 봅니다. 인수 이전부터 이미 그 방향이었고, 인수는 속도를 붙였을 뿐입니다. 이번 차단은 그 판단이 옳았다는 사후 증명에 가깝습니다.

앞으로 볼 것은 이 형태가 반복되는지입니다. 모델 제공사가 유통 채널의 소유 구조를 이유로 공급을 끊는 사례는 이번이 처음입니다. 한 번 열린 문이라 다음이 있을 수 있고, 그때는 5퍼센트가 아닐 수 있습니다.

관련해서는 [[Cursor Compile 2026 총정리]]에 인수 발표와 자체 모델 로드맵이, [[Composer와 Grok]]에 인수 직후 모델 선택권 논의가 정리돼 있습니다.

---

참고:
- [Our decision on Cursor following its acquisition by SpaceX - OpenAI](https://openai.com/index/our-decision-on-cursor-following-its-acquisition-by-spacex/)
- [OpenAI to end model access to Cursor after acquisition by Elon Musk's SpaceX - CNBC](https://www.cnbc.com/2026/08/29/openai-cursor-spacex-model-access.html)
- [Musk defiant as OpenAI to cut off SpaceX-owned Cursor - Seeking Alpha](https://seekingalpha.com/news/4638037-musk-defiant-openai-cut-off-spacex-owned-cursor)
- [SpaceX officially closes its Cursor acquisition - TechCrunch](https://techcrunch.com/2026/08/15/spacex-officially-closes-its-cursor-acquisition/)
- [OpenAI Ends Cursor Model Access Nov 12, Migration Plan - explainx.ai](https://www.explainx.ai/blog/openai-ends-cursor-partnership-spacex-acquisition-august-2026)
- [Higher usage limits for Claude and a compute deal with SpaceX - Anthropic](https://www.anthropic.com/news/higher-limits-spacex)
- [Anthropic keeps Claude in Cursor as OpenAI pulls out over SpaceX deal - Cryptopolitan](https://www.cryptopolitan.com/anthropic-keeps-cursor-openai-pulls-out/)
