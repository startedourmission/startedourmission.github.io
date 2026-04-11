---
date: 2026-04-11
tags:
  - 정보
  - Headliner
  - LLM
description: "Meta Superintelligence Labs의 첫 모델 Muse Spark. 네이티브 멀티모달 추론, 비주얼 CoT, 멀티에이전트 오케스트레이션을 갖춘 Meta의 AI 전략 전환점."
---

# Meta Muse Spark: 140조 원을 건 AI 전략의 첫 번째 결과물

2026년 4월 8일, Meta가 새로운 AI 모델 **Muse Spark**를 공개했습니다. 이름만 보면 여느 모델 업데이트처럼 보일 수 있지만, 이 모델이 갖는 의미는 상당히 무겁습니다. Muse Spark는 Mark Zuckerberg가 기존 AI 전략에 불만을 품고 140억 달러(약 19조 원)를 투입해 영입한 Alexandr Wang이 이끄는 Meta Superintelligence Labs의 첫 번째 공식 모델이기 때문입니다. 코드명 'Avocado'로 개발된 이 모델은 Meta가 그동안 고수해 온 오픈소스 노선에서 벗어나 비공개 모델로 출시되었다는 점에서도 업계의 주목을 받고 있습니다.

## Alexandr Wang과 Meta Superintelligence Labs의 탄생

이야기는 2025년 6월로 거슬러 올라갑니다. 당시 Meta의 CEO Mark Zuckerberg는 자사 AI 모델 Llama 시리즈가 OpenAI, Google, Anthropic 등 경쟁사 대비 뒤처지고 있다는 현실에 만족하지 못했습니다. 그의 해법은 과감했습니다. 데이터 레이블링 기업 Scale AI의 공동창업자이자 CEO였던 Alexandr Wang을 Meta 역사상 최초의 Chief AI Officer(최고AI책임자)로 영입한 것입니다. 이 딜의 규모도 남달랐습니다. Meta는 Scale AI의 비의결권 지분 49%를 143억 달러(약 19조 원)에 인수하며 Wang을 데려왔습니다.

Wang이 맡은 임무는 명확했습니다. Meta Superintelligence Labs라는 새로운 조직을 이끌며 Meta의 AI 역량을 근본부터 재구축하는 것이었습니다. 그리고 영입 후 약 9개월 만에, 그 첫 번째 결과물이 세상에 나왔습니다. 바로 Muse Spark입니다.

## 네이티브 멀티모달: 텍스트, 이미지, 음성을 하나로

Muse Spark의 가장 핵심적인 특징은 **네이티브 멀티모달(natively multimodal)** 설계입니다. 기존 많은 AI 모델이 텍스트 중심으로 설계된 후 이미지나 음성 기능을 별도 모듈로 붙이는 방식이었다면, Muse Spark는 처음부터 텍스트, 이미지, 음성 입력을 통합적으로 처리하도록 만들어졌습니다.

사용자는 텍스트를 타이핑하는 것은 물론, 이미지를 업로드하거나 음성으로 질문을 던질 수 있습니다. 다만 현재 출력은 텍스트로 한정됩니다. 이미지나 음성 생성 기능은 아직 포함되어 있지 않지만, Muse 시리즈의 향후 모델에서 확장될 가능성이 높습니다. "Muse Spark"라는 이름 자체가 Muse 시리즈의 첫 번째 모델임을 암시하고 있으니까요.

이 멀티모달 설계 덕분에 Muse Spark는 과학, 수학, 의료 등 복잡한 영역의 질문에도 다양한 형태의 입력을 조합해 추론할 수 있습니다. 예를 들어, 피부 발진 사진을 찍어 올리면서 음성으로 증상을 설명하면 모델이 이를 종합적으로 분석해 답변을 제공하는 식입니다.

## 비주얼 Chain of Thought: 이미지 위에서 생각하는 AI

Muse Spark가 도입한 가장 흥미로운 기능 중 하나는 **비주얼 Chain of Thought(Visual CoT)**입니다. 일반적인 Chain of Thought가 텍스트 기반으로 단계별 추론 과정을 보여주는 것이라면, 비주얼 CoT는 이미지 위에서 직접 추론 과정을 전개합니다.

구체적으로 어떻게 작동하는지 생각해 보겠습니다. 복잡한 차트나 다이어그램이 포함된 이미지를 모델에 제공하면, Muse Spark는 해당 이미지의 특정 영역을 참조하면서 "이 부분이 X를 나타내고, 저 부분과 비교하면 Y라는 결론이 나온다"는 식으로 시각적 단서를 활용한 단계별 추론을 수행합니다. 이는 단순히 이미지를 텍스트로 설명하는 것과는 질적으로 다른 접근입니다.

Meta는 이 기능을 "contemplating mode(숙고 모드)"라고도 부르는데, 이미지 속 정보를 깊이 있게 분석할 때 특히 유용합니다. 의료 영상 해석, 과학 논문의 복잡한 도표 분석, 건축 설계도 검토 등에서 실질적인 활용이 기대됩니다.

## 멀티에이전트 오케스트레이션: AI가 AI를 부리는 시대

Muse Spark의 또 다른 주목할 기능은 **멀티에이전트 오케스트레이션(Multi-Agent Orchestration)**입니다. 하나의 Muse Spark 인스턴스가 여러 개의 서브에이전트를 동시에 배치해 복잡한 작업을 병렬로 처리할 수 있습니다.

Meta가 소개한 대표적인 예시는 여행 계획 수립입니다. 사용자가 "도쿄 5일 여행 계획 짜줘"라고 요청하면, 하나의 에이전트가 여행 일정을 구성하는 동시에, 다른 에이전트는 목적지별 비교 분석을 수행하고, 또 다른 에이전트는 현지 액티비티를 검색합니다. 이 모든 작업이 병렬로 이루어지기 때문에, 단일 에이전트가 순차적으로 처리할 때보다 응답 속도와 품질이 모두 향상됩니다.

여기에 더해 Muse Spark는 **도구 사용(tool-use)** 기능도 내장하고 있습니다. 모델이 외부 API나 웹 검색 등의 도구를 직접 호출해 실시간 정보를 가져오고, 이를 추론에 활용할 수 있다는 뜻입니다. 멀티에이전트 오케스트레이션과 도구 사용이 결합되면, AI가 단순한 질의응답을 넘어 실질적인 작업 수행 도구로 기능할 수 있는 기반이 마련됩니다.

흥미로운 기술적 디테일도 있습니다. Meta는 Muse Spark 개발 과정에서 **"thought compression(사고 압축)"** 기법을 적용했다고 밝혔습니다. 강화학습 단계에서 모델이 과도한 추론 토큰을 사용하면 페널티를 부과해, 효율적인 다단계 문제 해결 능력을 갖추도록 유도한 것입니다. 빠르면서도 정확한 추론을 동시에 추구한 설계 철학이 엿보입니다.

## 어디서 만날 수 있나: 20억 사용자 플랫폼에 탑재

Muse Spark는 현재 **Meta AI 앱**과 **meta.ai** 웹사이트에서 먼저 이용할 수 있으며, 향후 몇 주 내로 Meta의 주력 플랫폼 전반으로 확대될 예정입니다. 구체적으로는 다음 플랫폼에 탑재됩니다.

- **Facebook**: 피드 내 AI 어시스턴트
- **Instagram**: DM 및 검색 내 AI 기능
- **WhatsApp**: 채팅 내 AI 비서
- **Messenger**: 대화형 AI 지원
- **Ray-Ban Meta 스마트 글래스**: 음성 기반 AI 인터랙션

20억 명 이상의 사용자를 보유한 Meta의 플랫폼 생태계에 직접 탑재된다는 점은, 기술적 성능과 별개로 엄청난 배포 규모를 의미합니다. 다만 현재 **미국 한정 출시**이며, 글로벌 확대 일정은 아직 공개되지 않았습니다.

## 성적표: 선두는 아니지만 경쟁권 진입

솔직히 말해, Muse Spark가 현존 최고 성능의 모델은 아닙니다. Artificial Analysis Intelligence Index 기준으로 Muse Spark의 점수는 52점으로, Claude Opus 4.6, GPT-5.4, Gemini 3.1 Pro Preview에 이어 4위를 기록했습니다. Claude Sonnet 4.6보다는 앞섰지만, 최상위 모델과는 분명한 격차가 있습니다.

특히 취약한 영역이 두 가지 있습니다.

**첫째, 코딩 성능입니다.** Terminal-Bench 2.0에서 Muse Spark는 59.0점을 기록한 반면, GPT-5.4는 75.1점을 달성했습니다. 자율적 코드 생성, 멀티파일 리팩토링, 테스트 루프 실행 같은 장기 코딩 워크플로우에서 의미 있는 격차입니다. Meta 역시 코딩을 현재의 gap으로 인정하고 있습니다.

**둘째, 추상적 추론 능력입니다.** ARC-AGI-2 벤치마크에서 Muse Spark는 42.5%에 그쳤습니다. Gemini 3.1 Pro의 76.5%, GPT-5.4의 76.1%와 비교하면 구조적인 차이라 할 수 있습니다. 많은 연구자가 범용 지능의 대리 지표로 보는 유동적 패턴 인식 영역에서 아직 갈 길이 멀다는 뜻입니다.

반면 **멀티모달 이해**와 **건강/의료 정보 처리**에서는 경쟁 모델과 대등하거나 우위를 보인다고 Meta 측은 밝혔습니다. "작고 빠르게(small and fast)" 설계한 첫 번째 모델이라는 점을 고려하면, 향후 Muse 시리즈의 후속 모델에서 성능 격차를 좁혀나갈 가능성이 높습니다.

## Llama는 어떻게 되나: 오픈소스와 비공개의 이중 전략

Meta의 AI 전략에서 가장 큰 변화는 **오픈소스 노선의 수정**입니다. 그동안 Meta는 Llama 시리즈를 오픈소스(정확히는 오픈 웨이트)로 공개하며 AI 업계의 독특한 포지션을 구축해 왔습니다. 그런데 Muse Spark는 완전한 비공개(proprietary) 모델입니다.

Meta 대변인은 기존 Llama 모델은 계속 오픈소스로 유지된다고 확인했지만, 향후 Llama 모델의 공개 여부에 대해서는 명확한 답변을 피했습니다. Muse Spark의 가중치 공개에 대해서도 "향후 버전을 오픈소스로 공개하고 싶다는 희망이 있다(hope to open-source future versions)"는 모호한 표현에 그쳤습니다. 구체적인 타임라인이나 약속은 없었습니다.

결과적으로 Meta는 현재 이중 전략을 구사하고 있는 셈입니다.

- **Llama 계열**: 오픈 웨이트, 커뮤니티 및 생태계 확장용
- **Muse 계열**: 비공개, Meta 자사 제품 탑재 및 상업적 경쟁력 확보용

이 구조가 장기적으로 유지될지, 아니면 Llama마저 비공개로 전환될지는 아직 불분명합니다. 하지만 분명한 건, Meta가 더 이상 "모든 것을 공개한다"는 원칙만으로는 OpenAI나 Google과의 경쟁에서 승리하기 어렵다고 판단했다는 점입니다.

## 72조에서 135조로: Meta의 AI 투자 규모가 말해주는 것

Muse Spark의 등장을 이해하려면, Meta가 AI에 쏟아붓고 있는 투자 규모를 알아야 합니다.

- **2025년 설비 투자(CapEx)**: 약 722억 달러(약 97조 원)
- **2026년 설비 투자 전망**: 1,150억~1,350억 달러(약 155조~182조 원)

2026년 투자 규모는 2025년의 거의 두 배에 달합니다. 이 금액은 차세대 GPU 수십만 장 확보, 글로벌 데이터센터 확장, 네트워킹 인프라, 전력 및 냉각 시설, 그리고 인재 확보에 투입됩니다. Meta의 CFO Susan Li는 회사가 여전히 "용량 제약(capacity constrained)" 상태라고 밝혔습니다. 더 강력한 AI 모델을 만들고, 핵심 광고 사업의 AI 최적화를 확대하려면 지금보다 훨씬 더 많은 컴퓨팅 파워가 필요하다는 뜻입니다.

이 천문학적 투자가 Muse Spark 하나를 위한 것은 아닙니다. Meta Superintelligence Labs가 "초지능(superintelligence)"이라는 궁극적 목표를 향해 나아가는 과정에서, Muse Spark는 그 여정의 첫 발자국에 불과합니다. Muse 시리즈의 후속 모델, 그리고 아직 공개되지 않은 프로젝트들이 이 인프라 위에서 구동될 것입니다.

---

Muse Spark는 완벽한 모델이 아닙니다. 코딩과 추상적 추론에서 선두 모델과 격차가 있고, 오픈소스를 포기한 전략적 선택에 대한 비판도 존재합니다. 하지만 9개월 만에 AI 스택을 근본부터 재구축하고, 20억 사용자 플랫폼에 직접 탑재되는 경쟁력 있는 모델을 내놓았다는 점은 분명한 성과입니다. Meta가 AI 경쟁에서 뒤처진 추격자에서 진지한 경쟁자로 전환하고 있다는 신호로 읽을 수 있습니다.

Muse 시리즈의 다음 모델이 나올 때, 이 격차가 얼마나 좁혀질지 지켜보는 것이 앞으로의 관전 포인트가 될 것입니다.

---

Sources:
- [Introducing Muse Spark - Meta AI Blog](https://ai.meta.com/blog/introducing-muse-spark-msl/)
- [Meta debuts the Muse Spark model - TechCrunch](https://techcrunch.com/2026/04/08/meta-debuts-the-muse-spark-model-in-a-ground-up-overhaul-of-its-ai/)
- [Meta debuts new AI model - CNBC](https://www.cnbc.com/2026/04/08/meta-debuts-first-major-ai-model-since-14-billion-deal-to-bring-in-alexandr-wang.html)
- [Meta debuts Muse Spark - Axios](https://www.axios.com/2026/04/08/meta-muse-alexandr-wang)
- [Meta unveils Muse Spark - Fortune](https://fortune.com/2026/04/08/meta-unveils-muse-spark-mark-zuckerberg-ai-push/)
- [Goodbye, Llama? - VentureBeat](https://venturebeat.com/technology/goodbye-llama-meta-launches-new-proprietary-ai-model-muse-spark-first-since)
- [Meta Muse Spark Benchmarks - Nerd Level Tech](https://nerdleveltech.com/meta-muse-spark-proprietary-ai-model-benchmarks)
- [Muse Spark vs Llama 4 - WaveSpeedAI](https://wavespeed.ai/blog/posts/muse-spark-vs-llama-4-meta-strategy-2026/)
- [Meta beats earnings as 2026 AI capex tops out at $135 billion - Quartz](https://qz.com/meta-earnings-q4-2025-ai-mark-zuckerberg)
