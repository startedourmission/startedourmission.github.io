---
date: 2026-03-13
tags:
  - 논문
  - Headliner
  - 베스트논문
---
OpenClaw-RL은 사용자와의 대화 자체를 강화학습 신호로 전환하는 비동기 RL 프레임워크입니다. 기존 RLHF/RLVR가 사전 수집된 데이터셋 위에서 배치 학습을 전제했다면, OpenClaw-RL은 실시간 대화를 가로채서 모델을 계속 개선합니다. 에이전트가 배포된 상태에서, 서빙을 중단하지 않고, 수동 레이블링 없이요.

개인화 에이전트와 범용 에이전트(터미널, GUI, SWE, 도구호출)를 하나의 파이프라인에서 동시에 훈련할 수 있다는 게 핵심 주장입니다. Princeton의 Yinjie Wang, Mengdi Wang과 Ling Yang이 참여했고, 칭화대 THUDM의 Slime 프레임워크 위에 구축되었습니다.

---

## 핵심 아이디어: Next-State Signal은 낭비되고 있다

논문이 출발하는 관찰은 단순합니다. 에이전트가 행동($a_t$)을 하면, 반드시 다음 상태($s_{t+1}$)가 돌아옵니다. 사용자 응답, 터미널 stdout, GUI 화면 전환, 테스트 결과 등이요. 기존 시스템은 이걸 단순히 "다음 행동을 위한 컨텍스트"로만 쓰고 버립니다.

OpenClaw-RL은 이 next-state signal에 두 가지 정보가 담겨있다고 봅니다:

1. **평가 신호(Evaluative signal)**: 이전 행동이 얼마나 좋았는지. 사용자가 같은 질문을 다시 하면 불만족, 테스트 통과하면 성공.
2. **지시 신호(Directive signal)**: 어떻게 달랐어야 하는지. "파일부터 확인했어야지"라는 사용자 피드백은 단순 점수가 아니라, 토큰 수준에서 뭘 바꿔야 하는지 알려줍니다.

기존 RLVR은 스칼라 보상만 다루니까 directive signal을 날려버리고, distillation 방법들은 사전 수집 데이터에 의존합니다. OpenClaw-RL은 두 신호를 모두 실시간으로 회수합니다.

---

## 시스템 아키텍처: 4개 비동기 루프

OpenClaw-RL은 Slime 프레임워크 위에서 4개 컴포넌트를 완전히 디커플링합니다:

- **Policy Serving** (SGLang): 모델이 사용자 요청을 처리
- **Environment**: 개인 에이전트는 사용자 기기, 범용 에이전트는 클라우드 환경
- **PRM Judge** (SGLang/API): 응답 품질을 평가
- **Policy Training** (Megatron): 정책 업데이트

4개가 서로를 블로킹하지 않습니다. 모델이 다음 요청을 처리하는 동안 PRM이 이전 응답을 평가하고, 트레이너가 그래디언트를 업데이트합니다. 개인 에이전트의 경우, 사용자 기기에서 OpenAI 호환 API로 RL 서버에 연결합니다. 대화 데이터가 외부로 나가지 않는 셀프 호스팅 구조입니다.

세션 인식(session-aware) 환경 서버가 API 요청을 두 유형으로 분류합니다:

- **Main-line turn**: 학습 대상이 되는 에이전트의 주요 응답
- **Side turn**: 메모리 정리, 환경 전환 같은 보조 쿼리 (학습 제외)

---

## 학습 방법: Binary RL + OPD + Combined

### 1. Binary RL

PRM(Process Reward Model)이 에이전트 응답 $a_t$과 다음 상태 $s_{t+1}$을 보고 +1(좋음), -1(나쁨), 0(중립)으로 평가합니다. $m$번 독립 평가 후 다수결(majority vote)로 최종 점수를 결정합니다.

이 스칼라 보상을 advantage로 사용해서 PPO 스타일의 clipped surrogate objective로 학습합니다. 비대칭 클리핑($\varepsilon = 0.2$, $\varepsilon_{high} = 0.28$)을 적용하고, KL 정규화($\beta_{KL} = 0.02$)를 더합니다.

모든 평가된 턴에서 학습 샘플을 만들 수 있다는 게 장점입니다. 단점은 풍부한 directive 정보를 스칼라 하나로 압축한다는 것.

### 2. Hindsight-Guided On-Policy Distillation (OPD)

OPD는 directive signal을 토큰 수준 supervision으로 변환합니다. 4단계로 동작합니다:

**Step 1. Hindsight hint 추출**: Judge가 $s_{t+1}$에서 구체적이고 실행 가능한 힌트(1-3문장)를 추출합니다. 원본 next-state를 그대로 쓰지 않는 이유는, 사용자 응답에 수정 사항과 무관한 새 질문이 섞여 있을 수 있기 때문입니다.

**Step 2. 힌트 선택 및 필터링**: $m$개 투표 중 양성(+1)이면서 10자 이상인 힌트 중 가장 긴 걸 선택합니다. 유효한 힌트가 없으면 샘플 자체를 드롭합니다. 양보다 질을 택하는 설계입니다.

**Step 3. Enhanced teacher 구성**: 힌트를 원래 프롬프트 뒤에 붙여서 enhanced prompt($s_{enhanced} = s_t \oplus \text{hint}$)를 만듭니다. 사용자가 처음부터 수정 사항을 알려줬더라면 모델이 봤을 컨텍스트를 시뮬레이션하는 것.

**Step 4. 토큰 수준 advantage 계산**: 동일 모델이 enhanced prompt 하에서 원래 응답 $a_t$에 대한 log-probability를 계산합니다. 그리고:

$$A_t = \log \pi_{teacher}(a_t | s_{enhanced}) - \log \pi_\theta(a_t | s_t)$$

$A_t > 0$이면 teacher가 이 토큰을 더 선호 → 강화. $A_t < 0$이면 teacher가 덜 선호 → 억제. 같은 응답 내에서도 토큰마다 방향이 다릅니다.

핵심은 **별도의 teacher 모델이 필요 없다**는 점입니다. 같은 모델이 힌트가 있을 때와 없을 때의 분포 차이로 자기 자신을 가르칩니다.

### 3. Combined Method

Binary RL과 OPD의 advantage를 가중합으로 결합합니다:

$$A_t = w_{binary} \cdot r_{final} + w_{opd} \cdot (\log \pi_{teacher}(a_t | s_{enhanced}) - \log \pi_\theta(a_t | s_t))$$

기본값은 $w_{binary} = w_{opd} = 1$. Binary RL이 모든 턴에서 넓은 커버리지를, OPD가 directive signal이 풍부한 턴에서 고해상도 보정을 제공합니다.

### 4. 범용 에이전트: Step-wise Reward

범용 에이전트 설정에서는 outcome reward에 process reward를 추가합니다. RLAnything [Wang et al., 2026] 방식을 따라 $o + \sum_{i=1}^{m} r_i / m$을 보상으로 사용합니다. 같은 step index를 가진 action끼리 그룹핑해서 standardization하는데, 터미널 같은 환경에서는 상태 클러스터링이 어렵기 때문에 이 단순한 접근이 실용적입니다.

---

## 실험 결과

### 개인 에이전트: 시뮬레이션 실험

Qwen3-4B 기반으로 두 가지 시나리오를 시뮬레이션했습니다:

- **학생 시나리오**: AI가 숙제를 대신 해주되, AI가 쓴 것처럼 보이지 않게 (GSM8K 문제)
- **교사 시나리오**: 숙제 채점 시 구체적이고 친근한 피드백 생성

|방법|8 step 후|16 step 후|
|---|---|---|
|Binary RL|0.25|0.23|
|OPD|0.25|0.72|
|Combined|**0.76**|**0.81**|

(base score: 0.17)

Combined 방법이 압도적입니다. OPD는 초반에 Binary RL과 동일하지만 16 step에서 급격히 올라갑니다. 학습 샘플이 sparse하기 때문에 효과가 늦게 나타나는 것. Binary RL 단독은 거의 개선이 없습니다.

학생 시나리오에서 최적화 후 에이전트가 bold 처리나 과도한 단계별 구조를 피하고, 자연스러운 문체로 바뀌는 것을 확인했습니다. 교사 시나리오에서는 "Correct. Well done!" 같은 짧은 피드백이 구체적이고 친근한 코멘트로 변했습니다.

### 범용 에이전트: 4가지 설정

터미널(Qwen3-8B, 128 환경), GUI(Qwen3VL-8B-Thinking, 64 환경), SWE(Qwen3-32B, 64 환경), Tool-call(Qwen3-4B-SFT, 32 환경) 설정에서 학습 곡선이 안정적으로 상승하는 것을 보여줍니다.

|설정|Integrated (outcome + process)|Outcome only|
|---|---|---|
|Tool-call|0.30|0.17|
|GUI|0.33|0.31|

Process reward 통합이 특히 tool-call에서 효과적입니다 (0.17 → 0.30).

---

## 비판적 분석

### 강점

- **아이디어가 깔끔합니다.** Next-state signal이라는 보편적인 신호를 evaluative + directive로 분리해서 각각 다른 방법으로 회수한다는 구조가 직관적이고 설득력 있습니다.
- **비동기 아키텍처 설계가 실용적입니다.** 서빙을 중단하지 않고 학습하는 건 실제 배포 환경에서 핵심입니다. Slime이라는 검증된 인프라 위에 쌓은 것도 좋은 엔지니어링 판단.
- **OPD의 self-distillation 아이디어가 흥미롭습니다.** 별도 teacher 없이 힌트 유무에 따른 같은 모델의 분포 차이를 활용한다는 발상이 깔끔합니다.
- **개인화 에이전트와 범용 에이전트를 동일 프레임워크로 처리**하는 통합적 접근도 가치가 있습니다.

### 한계

- **개인 에이전트 실험이 시뮬레이션 기반입니다.** LLM이 학생/교사 역할을 하는 시뮬레이션이라, 실제 사용자와의 상호작용에서도 동일한 효과가 나타날지는 확인이 필요합니다. 실제 사용자는 시뮬레이터보다 훨씬 다양하고 예측 불가능합니다.
- **PRM의 품질에 전체 시스템이 의존합니다.** Binary RL이든 OPD든, PRM Judge가 정확하지 않으면 잘못된 신호로 학습하게 됩니다. 논문에서 PRM 자체의 정확도나 실패 사례에 대한 분석이 부족합니다.
- **개인화 실험의 스케일이 작습니다.** GSM8K 36문제, 16 step이 전부입니다. Combined의 0.76 → 0.81 개선이 통계적으로 유의미한지, 더 긴 학습에서도 안정적인지 확인하기 어렵습니다.
- **소비자급 하드웨어 접근성 의문.** 기본 설정이 8× GPU이고, 범용 에이전트는 64~128개 병렬 환경을 가정합니다. 로드맵에 저정밀 학습 지원이 있긴 하지만, 현재로서는 개인 사용자가 실제로 돌리기 어렵습니다.
- **Binary RL 단독의 성능이 기대 이하입니다.** 8 step에서 0.25, 16 step에서 오히려 0.23으로 내려간 건 의아합니다. 왜 그런지에 대한 분석이 없습니다.

### 전망

방향성 자체는 설득력이 있습니다. 에이전트가 사용될수록 자동으로 개선된다는 비전은 개인화 AI의 핵심 과제이고, next-state signal을 활용한다는 접근은 추가 데이터 수집 비용이 없다는 점에서 매력적입니다.

다만, 이 프레임워크가 연구 프로젝트에 머물지 실제로 사람들이 쓰는 도구가 될지는 하드웨어 접근성에 달려있다고 봅니다. 로드맵의 INT4/INT8 지원과 Tinker 클라우드 배포가 실현된다면, 개인 에이전트 개인화라는 영역에서 의미 있는 포지션을 잡을 수 있을 것 같습니다.

---

## 참고

- **논문**: Yinjie Wang, Xuyang Chen, Xiaolong Jin, Mengdi Wang, Ling Yang. "OpenClaw-RL: Train Any Agent Simply by Talking." arXiv:2603.10165, Mar 2026.
- **코드**: [github.com/Gen-Verse/OpenClaw-RL](https://github.com/Gen-Verse/OpenClaw-RL)
- **기반 인프라**: Slime (THUDM), OpenClaw
- **모델**: Qwen3 계열 (4B, 8B, 32B)