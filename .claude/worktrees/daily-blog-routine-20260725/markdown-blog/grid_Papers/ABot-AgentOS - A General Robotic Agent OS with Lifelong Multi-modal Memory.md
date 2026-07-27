---
date: 2026-07-17
tags:
  - 논문
  - 에이전트
  - LLM
  - 머신러닝
description: "Alibaba AMAP CV Lab이 설계한 로봇 운영체제 레이어. VLM 지각과 VLA 행동 사이에 빠진 심의적 계층을 채우는 에이전트 하네스와 평생 학습 멀티모달 그래프 메모리를 함께 제안합니다."
image: "![[abot-agentos-overview.png]]"
buzz: 74
---

> J. Tian, S. Liu, Y. Xu, J. Lu, Y. Qian, T. Zhang, F. Wang, X. Li, W. Zhang, S. Su, et al., "ABot-AgentOS: A General Robotic Agent OS with Lifelong Multi-modal Memory," arXiv:2607.10350, 2026.

## 저자

AMAP CV Lab은 Alibaba Group의 지도·공간 인텔리전스 부문 연구 조직입니다. 이 팀은 ABot-N0(항법 VLA 기반 모델)와 ABot-M0(조작 VLA 기반 모델)를 연달아 공개하며 구현체 AI를 위한 VLA 파운데이션 모델 스택을 쌓아왔습니다.

ABot-AgentOS는 그 다음 질문에서 출발합니다. VLM이 씬을 보고 VLA가 몸을 움직이는 사이에, 장기 계획과 메모리와 검증을 담당하는 계층은 누가 만드는가? [[추저동|Zedong Chu]]와 [[인밍양|Mingyang Yin]]이 이끄는 25인 이상 팀이 그 답으로 에이전트 OS를 제안합니다.

팀은 Research(알고리즘), Engineering(인프라), Benchmark(평가 환경) 세 트랙으로 나뉘어 운영됐습니다. [[추저동]]은 Alibaba AMAP의 Algorithm Expert로 구현체 AI, 디지털 휴먼, 디지털 트윈 연구를 이끌고 있고, [[인밍양]]은 논문 교신저자를 맡아 전체 방향을 조율했습니다.

## 배경

최근 VLM과 VLA 연구는 로봇의 지각과 행동 예측 능력을 크게 끌어올렸습니다. 그러나 실제 환경에서 로봇이 장시간 임무를 수행하려면 아직 세 가지 빈자리가 남아 있습니다.

**추론-실행 갭.** 파운데이션 모델의 출력을 행동으로 변환하는 과정에서 스킬 위임, 검증, 복구 논리가 빠져 있습니다. 많은 시스템이 모델 출력을 단계 없이 바로 행동으로 보냅니다.

**구현체 일반화 갭.** 기존 로봇 에이전트 시스템은 특정 하드웨어나 제어 API에 묶여 있어, 동일한 고수준 논리를 휴머노이드와 사족보행 로봇 모두에 재사용하기 어렵습니다.

**지속 메모리 갭.** 단기 버퍼나 텍스트 캐시는 멀티모달, 관계적, 출처 추적 가능한 경험을 장기간 유지하지 못합니다. 지난 세션에서 만난 사람의 얼굴이나 가구 위치를 다음 세션에도 기억하려면 구조화된 외부 메모리가 필요합니다.

## OS 레이어 구조

![[abot-agentos-overview.png]]

ABot-AgentOS는 VLM/VLA 파운데이션 모델 위, 저수준 로봇 컨트롤러 아래에 위치하는 심의적 에이전트 계층입니다. 입력(마이크, 앱, 카메라)을 받아 에지의 Tiny LLM이 매 턴을 처리하고, 복잡한 추론이 필요하면 클라우드의 Large LLM을 온디맨드로 호출합니다.

스킬은 플러그인 인터페이스로 통합됩니다. 각 스킬은 실행 환경(에지/클라우드)과 의존 스킬을 선언하고, ABot-AgentOS는 하드웨어 세부사항 없이 스킬을 선택하고 위임합니다. 같은 "물 가져다줘" 명령이 휴머노이드와 이동 로봇에서 다른 저수준 컨트롤러를 쓰더라도 고수준 논리를 공유할 수 있는 이유입니다.

중심에 있는 **Agent Harness**는 세 역할을 분리합니다.

**씬 조건부 플래닝.** 메인 LLM이 현재 씬, 맵, 기억, 로봇 상태를 고려해 고수준 계획을 세우고 어떤 스킬을 직접 호출할지, 서브에이전트에 위임할지를 결정합니다. 같은 명령도 현재 씬에 따라 다른 실행 전략이 필요하기 때문에 계획이 순수 언어 처리가 아닌 씬 조건부가 됩니다.

**스킬 러너.** 서브태스크를 받은 스킬 러너는 격리된 로컬 컨텍스트에서 반복 이동, 관찰, 재시도를 처리하고 메인 LLM에는 요약된 결과만 돌려줍니다. 로컬 충돌이나 뷰 조정 같은 절차 세부사항이 메인 컨텍스트를 오염시키지 않습니다.

**다단계 검증(Verifier).** 런타임, 스킬 레벨, 종료 시점 세 단계에서 에이전트의 언어 레벨 믿음과 환경 사실을 비교합니다. "이동했다"고 믿지만 실제로는 제자리인 상황을 잡아냅니다.

이 세 역할을 통해 ABot-AgentOS는 추론-실행-검증 루프를 닫고, 에이전트가 오래 실행될수록 생기는 컨텍스트 드리프트와 조기 종료를 줄입니다.

## 멀티모달 그래프 메모리

![[abot-agentos-memory-arch.png]]

단기 실행 계층이 Agent Harness라면, 세션을 가로질러 경험을 쌓는 계층이 **Universal Multi-modal Graph Memory**입니다. 메모리를 타입드 그래프 $\mathcal{G} = (\mathcal{V}, \mathcal{E})$로 표현하며, 각 노드 $v \in \mathcal{V}$는 엔티티, 장소, 이벤트, 시각 증거 등의 단위이고, 엣지 $e \in \mathcal{E}$는 시간, 공간, 신원, 상호작용 관계를 담습니다.

영상 프레임을 그대로 보관하거나 전체 대화 스크립트를 텍스트로 쌓는 대신, 모든 입력을 소스가 추적 가능한 그래프 레코드로 변환합니다. "어제 말티즈를 입양했다"는 발화는 시간 기준 앵커와 신원 가설과 소스 레퍼런스를 담은 노드-엣지 쌍으로 변환되어 나중에 "언제 개를 입양했어요?" 같은 질문에 그라운드된 답변을 가능하게 합니다.

**검색**은 하이브리드 시드 선택으로 시작합니다.

$$s(q,v) = \lambda_\text{sem}\, s_\text{sem}(q,v) + \lambda_\text{lex}\, s_\text{lex}(q,v) + \lambda_\text{meta}\, s_\text{meta}(q,v) + \lambda_\text{type}\, s_\text{type}(q,v)$$

시멘틱 임베딩, 어휘 오버랩, 메타데이터 필터, 노드 타입 제약을 가중합해 시드 노드를 고르고, 타입드 엣지를 따라 증거 서브그래프로 확장합니다. 검색 결과는 출처 참조와 검색 경로가 담긴 트레이스와 함께 직렬화되어 메인 LLM에 주입됩니다.

**실패 기반 평생 자기진화**가 이 메모리 시스템의 독특한 점입니다. 형식적으로 다음과 같이 정의됩니다.

$$\mathcal{T}_t,\, G_t = \text{Run}(\mathcal{D}_t;\, G_{t-1}, A_{<t})$$
$$\Delta A_t = \text{Gate}\bigl(\text{Compile}\bigl(\text{Propose}\bigl(\text{Diagnose}(\mathcal{T}_t)\bigr)\bigr)\bigr)$$
$$A_{\leq t} = A_{<t} \cup \Delta A_t$$

각 스플릿 평가가 끝난 뒤 Diagnoser가 실패 트레이스를 분석하고, HypothesisGenerator가 수정 후보(evo-asset)를 제안하며, CompilerCritic이 안전 제약으로 좁히고, GateAnalyst가 타깃 게인과 회귀 없음 기준으로 수용 여부를 판단합니다.

$$\text{Accept}(a) = \mathbb{I}\bigl[\Delta S_\text{target}(a) \geq \tau_\text{gain} \;\wedge\; \Delta S_\text{reg}(a) \geq -\tau_\text{reg}\bigr]$$

핵심 제약은 스플릿 $t$의 evo-asset이 $t$의 추론에는 절대 사용되지 않는다는 것입니다. 이후 스플릿에만 적용됩니다. 현재 스플릿의 정답으로 사후 수정하는 것이 아니라 진정한 누적 평생 개선으로 작동하는 이유입니다.

프라이버시 측면에서는 에지의 **Private Memory**(맵, 개인 상호작용 기록)와 클라우드의 **Common Memory**(비민감 공간 정보)로 분리하며, 프라이버시 판별 정확도 99% 이상으로 업로드 대상을 필터링합니다.

## EmbodiedWorldBench

![[abot-agentos-ewb.png]]

기존 구현체 AI 벤치마크는 실내 또는 실외 중 하나에 한정되거나, 단일 능력 차원만 테스트하거나, 에이전트에게 평가 신호를 직접 노출하는 문제가 있었습니다. [[EmbodiedWorldBench]]는 이 세 제약을 동시에 해결하는 실행 가능 벤치마크입니다.

Unreal Engine 5 기반 UnrealZoo로 실내, 실외, 하이브리드를 포함한 16개 실행 가능 씬을 구성하고 각 태스크를 다음과 같이 형식화합니다.

$$\text{Scenario} = \langle \mathcal{M},\, \mathcal{S}_0,\, \mathcal{O},\, \mathcal{N},\, \mathcal{C} \rangle$$

$\mathcal{M}$은 공간 맵, $\mathcal{S}_0$는 초기 상태, $\mathcal{O}$는 관찰 규칙, $\mathcal{N}$은 NPC 행동, $\mathcal{C}$는 성공 기준입니다. 4단계 난이도, 200개 이상 태스크, 탐색, 오브젝트 탐색, NPC 대화, 동적 이벤트 등 4가지 태스크 유형을 포함합니다.

에이전트는 필터링된 시멘틱 맵과 자연어 명령만 받고, NPC 위치나 평가 신호는 알 수 없습니다. 모든 채점은 실행 트레이스에서 결정론적으로 이뤄지며 인간 주관 채점 없이 재현 가능합니다.

평가 지표는 두 가지입니다. **TSR(Task Success Rate)**는 모든 서브태스크와 종료 조건을 동시에 만족해야 하는 엄격한 지표이고, **GCR(Goal Completion Rate)**는 달성된 서브태스크 비율로 부분 완료도 인정하는 세밀한 지표입니다.

## 결과

**EmbodiedWorldBench 에이전트 평가** (Table 1):

| 에이전트 | 모델 | TSR (%) | GCR (%) |
| --- | --- | --- | --- |
| ReAct (베이스라인) | Qwen3.6-Plus | 49.97 | 57.95 |
| ABot-AgentOS | Qwen3.6-Plus | 61.96 | 68.79 |
| ABot-AgentOS | DeepSeek-V4-Pro | **68.18** | **74.62** |

같은 Qwen3.6-Plus 모델에서 ABot-AgentOS는 ReAct 베이스라인 대비 TSR +11.99%p, GCR +10.84%p를 달성했습니다. 더 강한 메인 모델(DeepSeek-V4-Pro)로 교체하면 추가로 TSR +6.22%p, GCR +5.83%p가 더 붙습니다. 에이전트 OS 계층이 모델 자체 능력 위에 곱해지는 방식으로 작동함을 보여줍니다.

**메모리 벤치마크 5종** (Static 기준, 기존 최고 대비):

| 벤치마크 | ABot-AgentOS Static | 기존 최고 | 차이 |
| --- | --- | --- | --- |
| LoCoMo | **87.5** | Mem0 85.6 | +1.9 |
| OpenEQA (24 frames) | **59.9** | GaussExplorer 57.8 | +2.1 |
| Mem-Gallery | **88.6** | MemGPT 87.6 | +1.0 |
| NExT-QA (Acc@All) | **76.5** | GraphVideoAgent 73.3 | +3.2 |
| EgoLife | **65.4** | WorldMM 56.0 | +9.4 |

자기진화(Self-Evolving)를 적용하면 LoCoMo +1.2(88.7), NExT-QA +4.1(80.6), EgoLife +0.8(66.2)이 추가 상승합니다. 가장 큰 폭은 NExT-QA로, 인과(Acc@C +4.5)와 시간적(Acc@T +1.6) 질문 카테고리에서 집중 개선이 나타납니다.

진화 자산이 현재 스플릿이 아닌 이후 스플릿에만 적용되기 때문에, 이 수치는 훈련-테스트 누수 없는 누적 학습의 효과입니다. LoCoMo는 인간 기준치(Human 87.9)에 0.4%p 차이까지 근접했고, OpenEQA는 기억 기반 방법 중 최고 수치를 기록했습니다.

## 회고

저자들은 §6 Conclusion에서 네 가지 한계를 명시합니다.

**실제 환경 검증 부재.** 잡음 있는 지각, 불완전한 구동, 네트워크 지연, 안전 제약, 이기종 로봇 구현체 환경에서의 대규모 실험은 미래 과제로 남습니다. 현재 모든 검증은 시뮬레이션 환경에 한정됩니다.

**EmbodiedWorldBench 커버리지 제한.** 씬 다양성, 사회적 상호작용의 깊이, 현재 에이전트 평가 범위가 더 넓어져야 합니다. 완전한 벤치마크 평가는 오픈 릴리즈 이후 공개 예정입니다.

**소형 모델 훈련 파이프라인의 범위.** SFT + GiGPO 기반 RL 파이프라인이 텍스트 샌드박스에 한정되어 있어, 시각 관찰과 멀티모달 피드백, 추가 시뮬레이션 플랫폼으로 확장이 필요합니다.

**자기진화의 프라이버시·거버넌스.** 실패 트레이스와 사후 피드백에 의존하는 자기진화 구조는 프라이버시 감사, 사용자 통제, 접근 관리를 더 강화해야 합니다.

## 정리

- ABot-AgentOS는 VLM 지각과 VLA 행동 사이에 빠져 있던 심의적 에이전트 계층을 채우며, 플러그인 기반 스킬 통합으로 이기종 로봇에서 같은 고수준 논리를 재사용할 수 있게 합니다.
- Universal Multi-modal Graph Memory는 원시 영상과 대화 대신 타입드 소스 그라운디드 그래프로 경험을 압축하고, 실패 트레이스 기반 자기진화 루프가 현재 스플릿을 오염시키지 않으면서 파이프라인 수준의 개선을 누적 적용합니다.
- [[EmbodiedWorldBench]]는 실내, 실외, 하이브리드 씬을 가로지르는 200개 이상 실행 가능 태스크와 결정론적 채점으로, 장기 구현체 에이전트 평가의 기준점을 제시합니다.

---

> J. Tian, S. Liu, Y. Xu, J. Lu, Y. Qian, T. Zhang, F. Wang, X. Li, W. Zhang, S. Su, et al., "ABot-AgentOS: A General Robotic Agent OS with Lifelong Multi-modal Memory," arXiv:2607.10350, 2026.
