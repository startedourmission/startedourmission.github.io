---
date: 2026-09-05
ready: false
tags:
  - 정보
  - LLM
  - 에이전트
  - AI평가
description: "OpenAI가 자사 Preparedness Framework의 Critical 사이버 임계를 넘었다고 스스로 공표했습니다. 사흘 사이 세 회사가 같은 구조를 택했습니다."
image: "![[GPT-6 Astra와 심사받는 사이버 능력-thumb.png]]"
---

[[OpenAI]]가 2026년 9월 3일 GPT-6 Astra를 공개했습니다. 벤치마크 표가 길게 붙었지만 이번 릴리스에서 실제로 새로운 건 점수가 아닙니다. OpenAI가 자사 Preparedness Framework에서 사이버보안 능력이 **Critical 등급에 도달했다고 스스로 밝힌 첫 모델**이라는 문장입니다.

Preparedness Framework는 원래 이 임계를 넘으면 배포에 제약을 거는 장치입니다. 그런데 모델은 제약과 함께 그대로 출시됐습니다. 이 조합이 이번 건의 핵심입니다.

## Critical 임계

Critical 사이버 등급의 정의는 이렇습니다. 사람의 개입 없이 잘 방어된 실제 핵심 시스템 다수에서 모든 심각도의 제로데이 익스플로잇을 찾아내고 작동하게 만들 수 있거나, 높은 수준의 목표만 주어졌을 때 방어된 표적에 대한 새로운 공격 전략을 처음부터 끝까지 설계하고 실행할 수 있으면 해당합니다.

측정치는 두 갈래로 나왔습니다. ExploitBench에서 100%를 기록했습니다. 직전 프런티어 모델인 GPT-5.6 Sol이 78.5%였습니다. 알려진 취약점을 작동하는 익스플로잇으로 바꾸는 능력을 재는 벤치마크입니다.

더 무거운 쪽은 오염 통제 테스트입니다. 2026년 6월부터 8월 사이 공개된 고위험 V8 취약점 20건으로 내부 포팅을 만들어 재봤더니, 임의 코드 실행 성공률이 39.0%였습니다. Sol은 5.5%였고, Astra는 그 성적을 훨씬 적은 출력 토큰으로 냈습니다. 학습 데이터 오염을 통제한 세트라서 "외운 것"으로 설명하기 어렵습니다.

여기에 더해 Astra는 알려지지 않은 제로데이 2건을 직접 찾아 익스플로잇했습니다. OpenAI는 해당 소프트웨어 메인테이너에게 신고 절차를 밟고 있다고 밝혔습니다.

## 무엇을 잠갔나

임계를 넘었다고 선언한 다음 OpenAI가 실제로 건 제약은 세 가지입니다.

첫째, 공개된 Astra는 개념 증명 익스플로잇 생성 요청을 거부합니다. OpenAI 표현으로는 "출시되는 Astra 버전은 보안 코드 리뷰와 패치로 제한되며, PoC 익스플로잇 생성과 관련된 프롬프트에는 응하지 않습니다." 취약점을 찾아 고치는 쪽은 되고, 공격 코드를 만드는 쪽은 막았다는 뜻입니다.

둘째, 엔터프라이즈에서 기본값이 꺼짐입니다. 워크스페이스 관리자가 수동으로 켜야 합니다.

셋째, 모델 자체의 행동 통제를 강화했습니다. 허가된 범위를 넘어서는지 재는 테스트에서 Astra는 권한 초과가 0%로 나왔습니다. Sol은 48%였습니다. 사이버 능력이 올라간 만큼 통제 지표도 같이 올려야 배포가 정당화되는 구조라서, 이 숫자가 릴리스에 붙어 있는 것 자체가 설계 의도를 보여줍니다.

그리고 이 제약을 푸는 통로를 따로 만들었습니다. Daybreak라는 프로그램입니다. 심사를 통과한 방어자에게는 완화된 세이프가드로 취약점과 PoC 검증, 멀웨어 분석, 탐지 엔지니어링을 열어 줍니다. 몇 주 안에 시작한다고 했습니다.

## 사흘, 세 회사

이 릴리스만 보면 OpenAI 혼자의 판단처럼 보입니다. 앞뒤 이틀을 붙이면 그림이 달라집니다.

| 날짜 | 회사 | 공개 모델 | 게이트된 사이버 능력 | 심사 통로 |
| --- | --- | --- | --- | --- |
| 09-01 | [[Anthropic]] | Claude Fable 5.1 | Claude Mythos 5.1 | Cyber Verification Program |
| 09-02 | [[Google]] | [[Gemini]] 3.8 Flash | Gemini 3.8 Flash Cyber | Fairwind Program |
| 09-03 | [[OpenAI]] | GPT-6 Astra | Astra의 공격 능력 | Daybreak |

사흘 사이에 셋이 같은 구조를 택했습니다. 그리고 이 구조는 "위험한 모델을 안 내놓는다"가 아닙니다. **모델은 내놓되, 능력의 일부를 신원으로 잠급니다.**

[[Anthropic]] 쪽이 이 구조를 가장 노골적으로 드러냅니다. [[Claude Fable 5|Fable]] 5.1과 Mythos 5.1은 **같은 모델이고 세이프가드 수준만 다릅니다.** Fable 5.1은 전체 공개, Mythos 5.1은 사이버보안과 생명과학에서 검증된 조직에만 열립니다. 관련해서는 [[Claude Mythos Preview 시스템 카드 분석]]에 먼저 정리해 둔 적이 있습니다.

[[Google]]은 여기에 한 가지를 더합니다. Gemini 3.8 Flash Cyber는 **공개 가격표에 올라 있지 않습니다.** 정부 기관, 핵심 인프라 운영자, 소프트웨어 메인테이너만 Fairwind 승인을 거쳐 쓸 수 있고, 통제된 환경에서만 돌려야 합니다. CodeMender 하네스와 묶어서 제공합니다. 앞선 세대에 대해서는 [[Gemini 3.6 Flash와 Flash Cyber - Pro는 어디에?]]에서 다뤘는데, 그때 나뉘기 시작한 선이 이번에 프로그램으로 굳었습니다.

세 곳을 겹쳐 놓으면 어느 발표문도 명시하지 않은 게 보입니다. 프런티어 사이버 능력이 **가격이 아니라 심사로 배분되기 시작했다**는 것입니다. 돈을 더 내면 더 센 모델을 쓰는 구조가 아니라, 누구인지를 증명해야 열리는 구조입니다. 클라우드 업계에서 정부 전용 리전이 갈라져 나간 것과 비슷한 분화가 모델 계층에서 일어나고 있습니다.

## 숫자 읽기

사이버 말고 나머지 벤치마크도 정리해 둡니다. 비교 대상은 대부분 직전 모델인 Sol입니다. [[GPT-5.6 Sol Terra Luna 출시 분석]]에 그쪽 수치가 있습니다.

| 항목 | Astra | 비교 |
| --- | --- | --- |
| [[OSWorld]] 2.0 | **72.6%** | Sol 65.7% |
| ScreenSpot-Pro (외부 툴 없이) | **92.7%** | Sol 76.9% |
| [[FrontierMath]] Tier 4 | **97.6%** | Fable 5.1 87.8% |
| [[GPQA Diamond]] | 96.0% | |
| Humanity's Last Exam (툴 사용) | 57.2% | Fable 5.1 **65.0%** |
| DeepSWE v1.1 | 74.1% | Muse Spark 1.3 **75.4%** |
| SRE-Bench (단일 시도) | 88.0% | |
| ExploitBench | **100%** | Sol 78.5% |
| 컨텍스트 512K~1M 유지율 | **96.3%** | Sol 73.8% |

점수보다 실무에 와닿는 건 [[OSWorld]] 2.0의 시간입니다. 정확도가 6.9%포인트 오른 것보다, 같은 과제를 약 75분이 아니라 약 40분에 끝낸다는 쪽이 큽니다. 47% 단축입니다. 컴퓨터를 직접 조작하는 에이전트는 실패보다 지연이 실사용을 막는 경우가 많습니다.

가격은 100만 토큰당 입력 10달러, 출력 50달러입니다.

주목할 건 **Astra가 전부 이긴 게 아니라는 점**입니다. Humanity's Last Exam은 툴을 붙여도 57.2%로 Fable 5.1의 65.0%에 밀립니다. 에이전틱 코딩인 DeepSWE v1.1도 74.1%로 Meta의 Muse Spark 1.3이 보고한 75.4%보다 낮습니다. 사이버와 컴퓨터 조작에서 크게 벌리고, 학술 추론과 코딩에서는 접전이거나 뒤집힌 자리가 있습니다.

숫자 하나는 특히 조심해서 읽어야 합니다. ARC-AGI-3입니다. OpenAI는 99.9%를 보고했는데, 자사 Responses API 하네스에 커스텀 컴팩션을 붙인 조건입니다. ARC Prize가 모델 중립 표준 하네스로 다시 재니 세미프라이빗 세트에서 **62.7%**가 나왔습니다. 같은 모델의 같은 벤치마크가 하네스에 따라 37%포인트 갈립니다. 흥미로운 건 비용까지 뒤집힌다는 점입니다. 표준 하네스 총비용이 26,098달러, 프로바이더 어댑터 하네스가 18,817달러였습니다. 점수는 높고 비용은 낮습니다. 추론 상태를 서버에 보존하니 같은 문제를 더 적은 행동으로 푸는 것입니다.

## 남는 문제

가장 날카로운 지적은 CSO Online에 실린 Sanchit Vir Gogia의 것입니다. 그는 투명성 역설을 짚습니다. Astra는 사이버 능력을 측정해 공표했기 때문에 **기업이 그 수준을 실제로 아는 유일한 프런티어 모델**이 됐습니다. 반대로 이미 기업 자격증명 뒤에서 돌아가고 있는 이름 없는 모델들은 그런 식으로 측정된 적이 없습니다. 재고 공개한 쪽이 더 위험해 보이는 역전이 생깁니다.

Gogia는 두 가지를 더 지적합니다. Astra는 사고 흐름 관측 가능성이 이전보다 낮아졌습니다. 그리고 "OpenAI가 Astra를 모니터링할 수 있다는 것이 기업이 Astra를 감사할 수 있다는 뜻은 아닙니다." 통제 권한이 제공자 쪽에만 있는 구조입니다.

여기에 덧붙일 게 하나 있습니다. Critical 임계 판정이 **자기 신고**라는 점입니다. Preparedness Framework는 OpenAI가 만들고 OpenAI가 적용합니다. 외부 감사 기관이 등급을 매기는 게 아닙니다. Anthropic의 ASL 체계도, Google의 Fairwind 심사 기준도 마찬가지입니다. 세 회사가 사흘 사이에 비슷한 게이트를 세운 건 규제가 시켜서가 아니라 각자 판단한 결과입니다. 판단이 겹쳤다는 사실 자체는 이 위험이 실재한다는 신호로 읽을 만합니다. 다만 기준을 세운 쪽과 통과 여부를 정하는 쪽이 같다는 구조는 그대로 남아 있습니다.

제 생각에는 앞으로 몇 달이 이 구조가 굳는지 아닌지를 가를 것 같습니다. Daybreak와 Fairwind와 Cyber Verification Program에 실제로 누가 들어가는지, 승인 기준이 공개되는지, 탈락 사유가 설명되는지가 관건입니다. 셋 다 아직 "곧 시작합니다" 단계입니다. 게이트를 세운 것까지는 각 회사의 선택이지만, 게이트 운영이 불투명해지면 결국 능력 배분이 계약과 관계로 결정되는 시장이 됩니다.

---

참고: [GPT-6 Astra 공식 발표](https://openai.com/index/gpt-6-astra/) · [GPT-6 Astra 안전성 개요](https://openai.com/index/safety-overview-gpt-6-astra/) · [OpenAI launches GPT-6 Astra, its first model to cross a critical cybersecurity threshold (CSO Online)](https://www.csoonline.com/article/4218679/openai-launches-gpt-6-astra-its-first-model-to-cross-a-critical-cybersecurity-threshold.html) · [GPT-6 Astra Scores 100% on ExploitBench as OpenAI Blocks PoC Exploit Requests (The Hacker News)](https://thehackernews.com/2026/09/gpt-6-astra-scores-100-on-exploitbench.html) · [GPT-6 Astra Benchmarks Explained (Vellum)](https://www.vellum.ai/blog/gpt-6-astra-benchmarks-explained) · [ARC Prize 검증 결과](https://arcprize.org/blog/astra) · [OpenAI begins rolling out GPT-6 Astra (CNBC)](https://www.cnbc.com/2026/09/03/open-ai-astra-gpt-6-cyber.html) · [Fairwind Program (Google)](https://blog.google/innovation-and-ai/technology/safety-security/fairwind-program/) · [Claude Mythos (Anthropic)](https://www.anthropic.com/claude/mythos) · [HN 토론 #49554643](https://news.ycombinator.com/item?id=49554643)
