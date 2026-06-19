---
date: 2026-05-15
tags:
  - 논문
  - 벤치마크
  - LLM
  - 에이전트
aliases:
  - "LongMemEval-V2"
image: "![[longmemeval-v2-overview.png]]"
description: UCLA 팀이 ICLR 2025의 LongMemEval을 웹 에이전트 trajectory 환경으로 확장한 후속 벤치마크입니다. 451개 수작업 문항으로 static state recall·dynamic state tracking·workflow knowledge·environment gotchas·premise awareness 다섯 메모리 능력을 측정하며, 채팅 히스토리에서 ServiceNow·WebArena의 실제 에이전트 행적으로 옮겨가 25M~115M 토큰 규모의 haystack을 다룹니다.
buzz: 57
---

> D. Wu, Z. Ji, A. Kawatkar, B. Kwan, J.-C. Gu, N. Peng, and K.-W. Chang, "LongMemEval-V2: Evaluating Long-Term Agent Memory Toward Experienced Colleagues," arXiv:2605.12493, 2026.

에이전트 메모리를 평가하는 일이 왜 이렇게 어색했는지를 다시 생각하게 만드는 논문입니다. 그동안 메모리 벤치마크는 대부분 두 갈래 중 하나였습니다. 길어진 채팅 히스토리에서 사용자 정보를 회상하거나, 길어진 문서에서 needle을 뽑거나. 정작 실제 에이전트가 일하는 환경, 즉 ServiceNow 같은 사내 툴이나 WebArena 같은 웹 환경에서 *몇 달치 trajectory를 기억하는 동료*를 측정하는 평가는 비어 있었습니다. LongMemEval-V2는 그 빈자리를 채우려는 시도입니다.

저자들은 한 줄로 프레임을 박아둡니다. *고품질 메모리는 에이전트를 특정 환경의 숙련된 동료로 만든다*. 동료 1년치 노하우를 LLM이 가질 수 있는가, 가졌다면 어떻게 측정할 것인가. 이 질문에 451개 수작업 문항과 최대 115M 토큰짜리 haystack으로 답을 시도합니다.

## 저자

UCLA NLP의 [[장카이웨이]] 그룹과 [[펑난윈]] 그룹이 함께 붙은 작업입니다. 1저자 Di Wu는 2025년 ICLR에 발표된 1세대 LongMemEval의 1저자이기도 합니다. V1이 user-assistant 채팅 기반이었고 평가 대상이 RAG 컴포넌트(인덱싱·검색·읽기) 위주였던 반면, 같은 저자가 그 한계를 인정하면서 *채팅 히스토리만으로는 진짜 에이전트 메모리를 못 본다*고 자기 작업을 다시 짚어 V2로 이어왔습니다.

시니어 저자 라인은 [[펑난윈]]과 [[장카이웨이]]입니다. Kai-Wei Chang은 UCLA NLP 그룹을 이끄는 Associate Professor이자 Amazon Scholar로, 멀티모달·신뢰성 NLP 쪽에서 VisualBERT 같은 초기 비전-언어 모델 작업으로도 알려져 있습니다. 이번 논문에서 *coding agent를 memory controller로 쓴다*는 발상이 자연스럽게 나오는 배경에는 이 그룹이 그동안 쌓아온 multimodal·long-context 경험이 있습니다.

## 배경

기존 long-term memory 평가가 어떤 식으로 비어 있었는지를 표 한 장으로 정리한 게 인상적입니다. LongBench V2, MemoryAgentBench, CL-Bench 같은 일반 long-context 벤치는 멀티모달이 아니거나, 메모리 능력 다섯 축 중 일부만 다룹니다. LoCoMo, LongMemEval-V1, PersonaMem, BEAM 같은 대화형 long-context는 모두 user-assistant chat 도메인입니다. 에이전트 trajectory를 보는 쪽인 MemoryArena, AgentLongBench, EMemBench, FileGramBench, AMA-Bench도 멀티모달이 빠지거나 trajectory 한 개에 한정됩니다.

LongMemEval-V2 한 줄로 정리하면 *Web agent 도메인 + 멀티모달 + 다섯 능력 모두 + 100~498 sessions + 25M~115M tokens*입니다. 표에서 LME-V2만 모든 칸이 채워진 이유가 여기 있습니다. 메모리 능력 평가가 처음으로 trajectory 단위가 아니라 *trajectory들 사이*의 환경 지식을 다룹니다.

저자들의 동기 한 줄을 그대로 옮기면 다음과 같습니다. *동료 한 명이 어떤 환경에서 반복적으로 일하며 무엇을 내재화하는가*. 이 질문이 다섯 메모리 능력으로 쪼개지고, 그 다섯 축이 곧 벤치의 평가 차원이 됩니다.

## 어떻게 만들었나

전부 수작업입니다. 자동 큐레이션을 의도적으로 피했습니다.

**Trajectory Collection.** WebArena와 WorkArena, WorkArena++의 customized website (Magento shopping/admin, Postmill forum, Reddit, CMS, ServiceNow OneStopShop)에서 trajectory를 모았습니다. AgentLab 라이브러리 기반의 ReAct 스타일 에이전트가 GPT-5.2와 GPT-5-mini로 rejection sampling을 돌려 599개의 WebArena trajectory와 941개의 WorkArena/WorkArena++ trajectory를 얻었습니다. 전체 성공률 52.0%, trajectory당 평균 28.1 states. 실패 trajectory도 일부러 섞었습니다. *환경 gotcha는 실패에서 더 잘 드러나기 때문*이라는 게 저자들의 설명입니다.

**Question Annotation.** 451개 모두 사람이 만든 문항입니다. 다섯 메모리 능력 분류를 따라 trajectory를 일일이 들여다보고 *숙련 동료라면 자연스럽게 알 만한 사실*을 추려 질문화합니다. 그 후 강한 proprietary LLM이 parametric knowledge만으로 풀 수 없는지 직접 검증합니다. 저자들은 Gemini-3-Pro, GPT-5.2, Grok-4.1-thinking, Claude Opus 4.6 네 모델로 테스트해서 *최소 두 모델이 못 맞히는 문항만* 채택했다고 명시합니다. Gotcha 문항은 *경험 없는 신입이 스크린샷을 첨부해 질문을 던지는 시나리오*로 멀티모달까지 자연스럽게 들어가 있고, 그 외는 텍스트 기반 true/false·객관식·단답형으로 구성됩니다. 마지막에 *premise abstention* 문항도 추가되는데, 다른 환경에서는 맞지만 현재 환경에서는 틀린 전제를 모델이 거부해야 합니다.

**Answer Trajectory Labeling.** 각 문항마다 정답 근거가 되는 trajectory들을 사람과 Codex 코딩 에이전트가 함께 라벨링합니다. 평균적으로 한 문항을 풀려면 1.4개 trajectory가 필요하고 최대 5개까지 갑니다. 동적 또는 워크플로 문항은 *여러 supporting trajectory들이 모여야 상태 변화가 합성*되는 경우가 많습니다.

**Haystack Creation.** 두 티어를 만듭니다. LME-V2-Small은 100개 trajectory(2.5K states, 25M token)를 모든 문항이 공유하고, LME-V2-Medium은 문항별로 498개 trajectory(14.9K states, 115M token)를 갖습니다. 답이 들어 있는 trajectory가 전체에서 차지하는 비율은 일부러 *희박*하게 유지합니다(figure 3 오른쪽 분포 참고). Small은 Medium보다 trajectory 수 기준 359배 작지만 token 기준으로는 82배 차이. Oracle haystack은 정확히 답에 필요한 trajectory만 모은 1.39개(평균), 39.3개 state, 310.8K token입니다.

## 무엇을 측정하나

다섯 메모리 능력입니다. 저자들의 정의를 한국어 워크플로 예시로 함께 풀어 적습니다.

**Static state recall.** 특정 페이지의 버튼 위치나 모듈 affordance 같은 *변하지 않는 화면 사실*을 회상합니다. *네이버 페이 결제 화면에서 환불 버튼이 우상단인지 하단인지*를 묻는 셈입니다. 451 중 가장 흔한 카테고리이고 single-trajectory로도 풀리는 경우가 많습니다.

**Dynamic state tracking.** 어떤 액션 뒤에 환경이 어떻게 바뀌는지, 즉 world model 능력입니다. *카카오톡 톡채널 메시지 발송 후 어떤 통계 페이지가 갱신되는지*에 가깝습니다. 여러 trajectory가 같은 전이를 반복하면 그 패턴을 합성해야 답할 수 있습니다.

**Workflow knowledge.** 특정 작업을 끝내기 위해 필요한 절차 전체. *환불 신청 → 환불 사유 입력 → 환불 승인 → 정산 페이지 확인*처럼 단계 묶음을 기억해야 합니다. 19.1%의 문항이 이쪽이며 single trajectory만으로는 안 풀리는 경우가 많습니다.

**Environment gotchas.** 그 환경에서만 발생하는 잠재적 함정. *결제 금액에서 부가세가 자동 포함인지 별도인지*, *고객사 검색에서 ‘완료된 항목’ 필터가 기본으로 켜져 있는지* 같은 잘 모르면 무조건 실수하는 사실들입니다. Gotcha 문항은 신입이 스크린샷을 들고 질문하는 멀티모달 시나리오로 출제됩니다.

**Premise awareness.** 잘못된 전제를 거부해야 하는 능력. 다른 환경에서는 통하지만 현재 환경에서는 통하지 않는 가정을 묻습니다. 모델이 *답이 없다* 또는 *그런 필드 없음*을 분명히 말해야 정답입니다. abstention 카테고리는 static·dynamic·workflow 각각에 별도로 붙어 있어, 다섯 능력이 사실상 다섯 + abstention 분기 구조가 됩니다.

전체 분포는 static 29.7% / dynamic 19.1% / workflow 12.2% / gotchas 16.4% / static abstention 7.5% + dynamic abstention 9.1% + workflow abstention 6.4%. 정답 형식은 객관식 15.3% / 단답형 50.1% / free-form 34.6%. 출처 도메인은 WorkArena-ServiceNow 46.8%(n=211)가 가장 크고, WebArena Reddit 20.2%, CMS 18.4%, OneStopShop 14.6%로 따라옵니다.

## 결과

평가 포뮬레이션이 흥미롭습니다. *context gathering*이라는 이름으로, 메모리 시스템은 `Insert(h)`와 `Query(q)` 두 API만 노출합니다. trajectory를 순서대로 Insert하고, 마지막에 Query로 200K 토큰 budget의 context를 받아 *고정 reader model*(Qwen3.5-9B)이 답합니다. 메모리 시스템의 품질이 reader 능력에 묻히지 않도록 reader를 고정해둔 게 핵심입니다. accuracy와 query latency 둘 다 보고합니다.

먼저 두 개의 기준점을 잡습니다. trajectory를 전혀 안 주고 frontier LLM이 parametric knowledge만으로 푸는 *no-context* 하한과, 정답이 들어 있는 trajectory만 정확히 골라준 *oracle* 상한입니다.

| 기준점 | 모델 | 정확도 (%) |
| --- | --- | --- |
| No-context (parametric only) | Kimi K2.5 | **14.1** |
| No-context | Gemini-3.1-Pro | 11.0 |
| No-context | [[Claude]] Opus 4.6 | 11.8 |
| No-context | GPT-5.2 | 4.7 |
| Oracle trajectory | Qwen3.5-9B (reader) | 59.6 |
| Oracle trajectory | GPT-5.4-mini | 65.3 |
| Oracle trajectory | Codex (GPT-5.4-mini xhigh) | **89.7** |

모델이 그냥 알지는 못합니다(14% 이하). 반면 정답 trajectory만 정확히 찾아주면 89.7%까지 갑니다. 메모리 시스템이 메우는 건 이 두 끝점 사이입니다.

저자들이 제안한 베이스라인 두 가지가 그 간극을 다른 방식으로 채웁니다.

**AgentRunbook-R**(R for RAG)은 trajectory를 세 개의 knowledge pool로 분리합니다. raw state slice(상태 윈도우 + 주변 액션), state transition event(상태 변화 이벤트), procedure & hint note(워크플로 요약과 환경 gotcha 노트). query time에 LLM controller가 어느 pool에 어떤 쿼리를 던질지 정합니다. slice + note 조합이 빠지면 워크플로 정확도가 무너지는 ablation 결과를 함께 보입니다.

**AgentRunbook-C**(C for coding agent)는 더 과감합니다. trajectory를 그대로 파일로 디스크에 깔아두고, query마다 coding agent(Codex)에게 sandbox workspace를 만들어 던집니다. 그 워크스페이스에는 workflow document, manifest artifacts(현재 메모리 레이아웃 요약), helper script(상태 span 보기, trajectory 검색)가 들어 있어 *코딩 에이전트가 trajectory를 마음대로 grep·열람*해서 답에 필요한 증거를 모읍니다. workflow guidance·manifest·helper script가 *coding agent의 메모리 컨트롤러 역할을 정형화*해주기 때문이라는 해석입니다.

| 시스템 | Small (%) | Medium (%) | 평균 (%) |
| --- | --- | --- | --- |
| **AgentRunbook-C** | **74.9** | **70.1** | **72.5** |
| Codex (vanilla, [[OpenAI]]) | 69.9 | 68.7 | 69.3 |
| AgentRunbook-R | 59.6 | 57.0 | 58.3 |
| Simple RAG | 42.8 | 38.1 | 48.5 |

한 줄로 정리하면 *coding agent를 메모리 컨트롤러로 쓰는 게 RAG보다 좋다, 다만 scaffolding을 잘 짠 경우에 한해*. latency도 AgentRunbook-C가 Codex 평균 182초 대비 약 32% 더 빠릅니다.

세부적으로 어디서 무너지는지가 더 흥미롭습니다. 카테고리별 정확도를 보면 AgentRunbook-C의 약점은 환경 gotcha와 premise abstention입니다.

| 카테고리 | AgentRunbook-C (%) |
| --- | --- |
| Static state recall | **82.0** |
| Workflow knowledge | 72.6 |
| Dynamic state tracking | 72.4 |
| Environment gotchas | 51.7 |

*없는 것을 없다고 말하기*가 가장 어렵습니다. 모델이 늘 그렇듯 confabulate 합니다.

언급된 외부 메모리 시스템들(Mem0, Letta/MemGPT, Memory-R1, Mem-α, MemSkill, A-MEM, StateLM)은 본 논문의 baseline pool에는 직접 포함되지 않습니다. 저자들은 *이런 시스템들은 user-assistant chat이나 high-level strategy 중심으로 설계돼 noisy agent trajectory에 그대로 적용하면 효과가 떨어진다*고 명시하며, 그래서 AgentRunbook 시리즈를 새로 만들었다고 설명합니다.

## 회고

저자들이 명시한 한계는 명확합니다. 첫째, AgentRunbook-C의 latency가 여전히 100~140초대입니다. coding agent를 부르는 비용이 본질적이라 *언제 답이 와도 되는 비동기 사용*에는 적합하지만 *대화형 사용*에는 멀었습니다. 둘째, gotcha와 premise abstention 정확도가 50% 근방에 머뭅니다. *없음을 단언하는 능력*은 모델 본연의 hallucination 문제와 맞물려 있어 메모리 시스템만으로는 못 해결합니다. 셋째, V2는 영어 웹 환경에 한정됩니다. 한국어 사내 워크플로(네이버 페이 정산, 카카오톡 비즈채널 대시보드)에 같은 다섯 축을 적용하려면 trajectory collection부터 다시 해야 합니다. 다만 *능력 분류 자체*는 도메인 독립적이라 그대로 옮겨 쓸 만합니다.

저자들이 직접 적은 또 한 가지. *naive 적용*에 대한 경고입니다. 채팅 기반 메모리 시스템을 web agent trajectory에 그대로 박으면 raw state observation을 *너무 회의적으로* 압축하거나 high-level strategy만 남기고 fine-grained UI 사실을 버립니다. agent trajectory는 *원자 단위의 UI 관찰*과 *고수준 절차 지식*이 함께 들어가야 하는 mixed granularity 매체라는 점을 분명히 합니다.

## 정리

- 451개 수작업 문항으로 *에이전트가 환경의 숙련된 동료가 되는가*를 다섯 메모리 능력(static / dynamic / workflow / gotchas / premise)으로 측정합니다. LongMemEval V1의 채팅 도메인에서 web agent trajectory 도메인으로 옮겨가, haystack을 25M~115M 토큰까지 키웠습니다.
- coding agent를 memory controller로 쓰는 AgentRunbook-C가 72.5% 평균으로 1위, off-the-shelf Codex(69.3%)와 RAG 기반 AgentRunbook-R(58.3%)을 모두 앞섭니다. 다만 *없음을 단언하는 능력*(gotchas·abstention)에서는 50%대에 머무릅니다.
- 한국어 사내 워크플로에 가져다 쓰려면 trajectory 수집은 새로 해야 하지만, 능력 분류 다섯 축은 그대로 살아남습니다. *동료가 1년치로 내재화하는 것*을 측정 가능한 다섯 축으로 쪼갠 게 이 논문의 가장 큰 기여입니다.
