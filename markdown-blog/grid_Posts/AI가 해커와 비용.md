---
date: 2026-05-15
tags:
  - 정보
  - LLM
description: "같은 날 Google에서 정반대 결의 두 뉴스가 나왔습니다. Google Threat Intelligence Group이 *AI로 만들어진 첫 zero-day 익스플로잇* 을 잡았고, Google Research가 LLM의 KV cache를 *6배 압축* 하는 TurboQuant를 ICLR 2026에 공개했습니다. 한쪽은 공격 자동화, 다른 쪽은 비용 자동화입니다. AI가 양날의 검이라는 추상적 표현이 *같은 회사의 두 보도자료* 로 구체화된 하루였습니다."
---

2026년 5월 11일, 같은 날 Google에서 정반대 결의 두 뉴스가 나왔습니다.

[Google Threat Intelligence Group](https://cloud.google.com/blog/topics/threat-intelligence/ai-vulnerability-exploitation-initial-access)이 *AI로 만들어진 첫 zero-day 익스플로잇* 을 잡았다고 발표했습니다. *대규모 자동 익스플로잇 작전(mass exploitation event)* 을 계획하던 범죄 해커 조직이 LLM으로 취약점을 발견하고 코드를 작성한 정황이 문서화된 첫 사례입니다.

같은 날 [Google Research](https://research.google/blog/turboquant-redefining-ai-efficiency-with-extreme-compression/)는 [[TurboQuant]]를 공개했습니다. LLM의 KV cache를 6배 압축하고, Nvidia H100에서 8배 처리 속도를 내는 양자화 알고리즘입니다. 같은 GPU로 6배 큰 모델을 굴릴 수 있게 되니, *비용이 자동으로 떨어진다* 는 시그널입니다.

*공격 자동화 vs 비용 자동화* — AI의 양면이 한 날에 압축되어 노출됐습니다. 이 글은 두 뉴스를 *그 자체로* 풀고, *왜 같은 회사에서 같은 날 나왔는가* 를 짚습니다.

## AI의 첫 zero-day

GTIG가 잡은 것은 *2FA(이중 인증) 우회* zero-day입니다. 인기 있는 오픈소스 웹 기반 시스템 관리 도구를 노린 익스플로잇으로, Python 스크립트 형태였습니다.

GTIG가 *AI 작성* 이라고 판단한 단서는 다음 셋입니다.

- **과도한 docstring** — 교육용 주석이 부자연스럽게 많이 들어가 있음
- **환각된 CVSS 점수** — 실제 존재하지 않는 점수값이 코드 주석에 박혀 있음
- **textbook Pythonic 구조** — 사람 해커가 실전에서 쓰는 코드와 다르게, LLM 학습 데이터에 흔한 "교과서적" 구조

세 가지 모두 *LLM이 작성한 코드의 흔적* 으로 잘 알려진 패턴입니다. *코드 자체* 가 *작성자* 를 가리키는 셈입니다.

GTIG는 영향받은 벤더와 함께 *책임 있는 공개(responsible disclosure)* 절차를 거쳐 패치를 발행했고, 대규모 익스플로잇 작전은 발생 전에 차단됐다고 보고합니다.

이 한 건이 끝이 아닙니다. GTIG 보고서는 *중국·북한 연계 그룹* 도 *AI를 취약점 발견에 활용하는 데 상당한 관심* 을 보였다고 명시했습니다. 국가 후원 actor들이 *대규모 익스플로잇* 의 자동화 능력을 강화하기 위해 LLM을 도입하는 사례가 *복수* 발견됐습니다.

기존에 수개월이 걸리던 작업이 *분 단위 자동 파이프라인* 으로 압축되는 그림입니다.

1. 대상 소프트웨어 스캔
2. 약점 식별
3. 익스플로잇 코드 생성
4. 대규모 배포

이 사이클이 사람 손에서 *LLM + 도구* 조합으로 옮겨가면서, 보안 운영자가 대응할 시간이 *주 단위에서 시간 단위* 로 줄어들 가능성이 큽니다.

## TurboQuant

[[바하브 미로크니]] (Google Fellow, VP)와 Amir Zandieh가 ICLR 2026에 발표한 [TurboQuant](https://research.google/blog/turboquant-redefining-ai-efficiency-with-extreme-compression/)는 한 줄로 이렇게 정리됩니다 — *학습 없이 LLM의 KV cache를 3-bit으로 압축하면서 정확도 손실 zero*.

핵심 결과는 다음 셋입니다.

- **메모리 6× 압축** — KV cache 메모리를 *최소 6배* 줄임. 같은 GPU에서 *6배 큰 모델* 또는 *6배 긴 컨텍스트* 가능
- **H100에서 8× 빠른 처리** — unquantized keys 대비 최대 8배 처리 속도
- **정확도 손실 없음** — needle-in-a-haystack 검색에서 *unquantized와 동일한* 점수
- **fine-tuning 불필요** — 기존 모델에 그대로 적용. 런타임 오버헤드도 무시할 수준

기법은 두 단계입니다.

**1. 무작위 회전(random rotation)** — 데이터 벡터의 기하 구조를 단순화합니다. 회전 후의 벡터는 *각 차원이 비슷한 분포* 를 가지므로 표준 양자화가 쉬워집니다.

**2. PolarQuant** — 데카르트 좌표를 *극좌표* 로 바꿉니다. 반지름(크기)과 각도(방향)를 분리하면, 각도 분포가 *예측 가능하고 집중* 되어 있어 기존 양자화기에 필수였던 *per-block 정규화* 단계를 건너뛸 수 있습니다.

[Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/googles-turboquant-compresses-llm-kv-caches-to-3-bits-with-no-accuracy-loss) 보도에 따르면 이 결과가 공개된 직후 *메모리 칩 주가가 흔들렸다* 고 합니다. *같은 GPU·메모리로 6배의 일을 한다* 는 메시지가 메모리 수요 전망을 직접 압박했기 때문입니다.

[GitHub에서 빠르게 오픈소스 재구현](https://github.com/OnlyTerp/turboquant)이 나왔고, [[llama.cpp]] 같은 추론 엔진도 통합 논의를 시작했습니다. KV cache 압축뿐 아니라 *벡터 검색* (vector DB)에도 그대로 적용되는 알고리즘이라, *RAG 운영자* 에게도 직접 이득을 줍니다.

## 왜 같은 날 같은 회사에서

두 뉴스가 같은 날 [[Anthropic]]·OpenAI도 아닌 *Google* 에서 나왔다는 점이 흥미롭습니다. 한 가지 해석은 *Google이 AI의 양면을 모두 운영하는 위치* 라는 점입니다.

- *Google Cloud / GTIG* — 클라우드 운영자로서 *AI를 사용한 공격* 을 실시간 관측. 본인 인프라를 노리는 시도를 막아야 하는 자리
- *Google Research* — 모델 자체의 효율을 끌어올리는 자리. *AI 비용 자동 하락* 을 직접 만드는 위치

두 흐름은 사실 *같은 동력* 의 두 출구입니다. AI 모델 + 도구가 *사람이 손으로 하던 일을 자동화* 하는 흐름이 *공격 자동화* (해커가 LLM으로 vuln 찾기)와 *비용 자동화* (KV cache 압축으로 inference 비용 떨어뜨리기) 양쪽으로 동시에 흘러갑니다.

다른 회사 단위로 본 분포는 다음과 같습니다.

| 회사 | 공격 자동화 관측 | 비용 자동화 기여 |
| --- | --- | --- |
| Google | GTIG의 zero-day 차단 | TurboQuant, MoR, Gemini Nano |
| [[Anthropic]] | Claude의 evil-twin 시도 차단 보고 | (모델 효율 연구 상대적으로 비공개) |
| OpenAI | 보안 인텔리전스 비공개 위주 | (메모리 압축 연구 비공개) |
| [[Meta]] | (관측 비공개) | [[Muse Spark]] 효율 주장, LLM 추론 양자화 |

*Google이 양면을 모두 공개* 한 자리에 있는 셈입니다. 클라우드 운영과 연구 조직을 한 회사에서 굴리는 구조가, *AI가 양날의 검이라는 추상* 을 *오늘 같은 보도자료 두 장* 으로 구체화하는 위치로 만듭니다.

## 운영자에게 의미

**보안 운영자에게** — *AI가 만든 코드* 의 시그니처(과도한 docstring, 환각 CVSS, textbook 스타일)를 IDS·SAST 룰에 추가해 둘 가치가 있습니다. *사람이 쓴 익스플로잇* 과 *LLM이 만든 익스플로잇* 의 코드 시그니처가 다르다는 게 GTIG 보고서의 직접적 시사점입니다.

**ML 엔지니어에게** — [[TurboQuant]]가 자기 LLM 추론 스택에 들어올 가치가 있는지 직접 검증해 보세요. *학습 불필요·런타임 오버헤드 무시* 라는 두 조건이라, 적용 위험이 매우 낮습니다. [공식 발표](https://research.google/blog/turboquant-redefining-ai-efficiency-with-extreme-compression/)의 needle-in-a-haystack 결과를 본인 RAG 시스템에서 재현해 보는 게 가장 빠른 검증입니다.

**경영진에게** — 두 뉴스가 같은 날 나왔다는 사실 자체를 *AI 정책 검토* 의 단서로 쓸 수 있습니다. *AI 도입으로 비용이 떨어진다는 시나리오와 AI로 공격 자동화가 진행 중인 시나리오가 같은 속도로 굴러간다* 는 것이 5월 11일에 노출된 메시지입니다. 한쪽만 보고 다른 쪽을 안 보는 것은 부분 정보입니다.

## 정리

- *AI로 만든 첫 zero-day* 가 잡혔다는 것은 *사람만 하던 공격 자동화가 AI로 옮겨가는 변곡점* 에 도달했다는 뜻입니다. 코드 시그니처로 식별 가능하다는 점이 그나마 다행입니다.
- [[TurboQuant]]는 *KV cache 6× 압축 + 정확도 zero loss* 라는 강한 결과를 *학습 없이* 달성했습니다. RAG·long context 운영자가 즉시 검증해 볼 가치가 있습니다.
- 두 뉴스가 *같은 날 같은 회사* 에서 나왔다는 사실이 본 글의 진짜 핵심입니다. AI가 양날의 검이라는 일반론이 *오늘 보도자료 두 장* 으로 구체화됐고, 어느 한쪽만 보면 분석이 부분적입니다.
