---
date: 2026-05-15
tags:
  - 논문
  - LLM
  - AI평가
aliases:
  - "EvoSafety"
description: fine-tuning 없이 모델 외부에 safety 자산을 두는 LLM 안전 프레임워크입니다. 공격 스킬 라이브러리와 경량 보조 디펜더가 공진화하며, victim model을 바꿔도 safety 자산을 그대로 재사용할 수 있습니다.
image: "![[evosafety-overview.png]]"
buzz: 0
citations: 0
---

> Zhang, X., Li, C., Liu, H., Yan, S., Yan, B., Ye, Q., & Li, H. (2026). Model-Agnostic Lifelong LLM Safety via Externalized Attack-Defense Co-Evolution. arXiv:2605.13411.

지금까지 LLM safety는 거의 전부 가중치 안에 있었습니다. [[Anthropic]]의 Constitutional AI도, RLHF도, safety SFT도, 결국 "이 모델의 파라미터에 safe behavior를 새긴다"는 발상이었습니다. 그래서 모델을 한 번 갈아끼울 때마다 safety 파이프라인 전체를 다시 돌려야 했습니다. EvoSafety는 그 흐름에서 한 발 빠져나옵니다. safety를 모델 밖에 있는 외부 구조(공격 스킬 라이브러리, 검증된 메모리 뱅크, 경량 보조 디펜더)로 옮기고, 그것을 victim model과 분리해서 운영합니다. 모델은 얼려둔 채로, safety 자산만 따로 키우는 발상입니다.

## 저자

교신저자는 Beijing University of Posts and Telecommunications(BUPT)의 Chaozhuo Li (李朝卓)입니다. 베이항대에서 박사를 받고 2020 ~ 2024년 MSRA에서 Lead Researcher로 일하다 BUPT 사이버스페이스 보안대학원으로 옮겼습니다. WSDM 2023, PAKDD 2023 Best Paper Nomination을 받았고, LLM jailbreak / defense, NLP, 소셜 네트워크 분석을 합니다. 1저자 Xiaozhe Zhang은 City University of Hong Kong 소속이며, 공저자에는 Beihang University와 Beijing Academy of Artificial Intelligence (BAAI) 연구자가 함께 들어가 있습니다.

## 배경

기존 LLM safety 패러다임은 크게 두 갈래입니다.

하나는 학습 시점에 safety를 모델 파라미터에 새기는 방식입니다. [[Anthropic]]의 Constitutional AI, [[OpenAI]] 계열의 RLHF, safety SFT가 여기 속합니다. 원리는 깔끔하지만 fragile해서 jailbreak에 쉽게 뚫리고, over-refusal이나 일반 성능 저하를 동반합니다. 무엇보다 victim model이 바뀌면 처음부터 다시 fine-tuning을 해야 합니다.

다른 하나는 추론 시점에 외부에서 거르는 방식입니다. 프롬프트 기반 self-scrutiny, Llama-Guard, Qwen3Guard 같은 별도 가드 모델이 그렇습니다. 모듈러하지만 base model을 손대지 않는 만큼 모델 내부의 safety mechanism은 활용하지 못합니다.

저자들이 짚는 두 패러다임의 공통 한계는 둘입니다. 첫째, red-teaming이 closed loop에서 빠르게 saturate되어 novel attack vector를 더 못 찾습니다. 둘째, safety 자산이 특정 victim model의 weight에 종속되어 있어 모델 교체 시 재사용이 어렵습니다. 프런티어 모델을 fine-tune하는 비용을 생각하면 둘 다 무거운 제약입니다.

## 어떻게 풀었나

EvoSafety의 발상은 단순합니다. 인류가 인지 부담을 외부 도구로 externalize해온 것처럼, safety game의 양쪽(공격자와 방어자) 모두에게 외부 지식 저장소를 붙여주자는 것입니다.

공격 쪽은 end-to-end 프롬프트 생성기에서 skill execution engine으로 바뀝니다. Adversarial Skill Library에 들어 있는 명시적 skill을 retrieval해서 조합하는 형태입니다. saturate되면 라이브러리를 확장하면 그만이라, zero-shot으로도 새 attack vector를 계속 만들어낼 수 있습니다.

방어 쪽은 victim model 자체를 fine-tune하지 않습니다. 대신 경량 Auxiliary Defense Model이 safety prefix를 만들어서 입력 앞에 붙입니다. 이 디펜더는 과거에 성공한 공격 프롬프트들을 모아둔 Verified Memory Bank에서 비슷한 사례를 retrieval해 참고합니다. 새로운 공격이 들어오면 그 프롬프트를 메모리에 추가하기만 해도 방어력이 올라갑니다. 추가 학습이 필요 없습니다.

두 정책은 GRPO로 공진화 학습됩니다. attacker는 라이브러리 활용과 novel attack 진화 사이를 메우고, defender는 over-defensiveness와 safety 사이를 맞춥니다. 비정상성(non-stationarity)을 다루기 위해 라운드를 두며 번갈아 업데이트합니다.

## 무엇으로 구성돼 있나

네 가지 외부 구조가 핵심입니다.

**Adversarial Skill Library**. heterogeneous attack artifact (실행 가능한 코드, 자연어 기술 등)를 Dual-Path Skill Grounding으로 통일된 표현으로 변환합니다. 각 skill은 실행 스크립트와 Markdown 명세서를 함께 갖습니다. Tri-Axis Skill Validation(functional validity, schema consistency, behavioral diversity)으로 거른 뒤, Skill Family Induction으로 동일 schema 안에서 변형을 합성해 라이브러리를 확장합니다.

**Attack Policy π_A**. Skill Retriever가 요청 r에 대해 상위 2개 skill을 가져오고, 그것을 컨텍스트로 받아 adversarial prompt a_t를 생성합니다. reward는 단순 judge score가 아닙니다. judge model이 한국어 / 영어 multi-tier로 0(Safe) / 0.5(Controversial) / 1(Unsafe)를 매기지만, attacker가 reward hacking으로 의도와 동떨어진 프롬프트를 만들면 의미가 없으므로 Early-Stage Alignment Gating을 추가합니다. trajectory 공간에서 a_t와 원 요청 r의 유사도가 threshold τ를 못 넘으면 reward를 0으로 만드는 indicator를 곱해줍니다. victim model을 부르기 전 단계에서 거르므로 추론 비용도 아낍니다.

**Verified Memory Bank**. 성공한 adversarial prompt만 누적해 둡니다. defender가 새 프롬프트 a_t를 받으면 vector retrieval로 top-k를 가져와 safety prefix d_t를 합성합니다.

**Auxiliary Defense Model π_D**. Llama-3.2-3B-Instruct를 LoRA로 학습한 경량 모델입니다. 학습 한 번으로 두 가지 모드를 다 합니다. Steer 모드는 prefix를 입력 앞에 붙여 victim model의 intrinsic safety를 활성화시키고, Guard 모드는 prefix가 거부를 유도하는지 미리 보고 그러면 입력 자체를 필터링합니다. defender의 reward는 benign / adversarial 두 분포에 걸쳐 정의해 over-refusal을 막습니다. benign 요청에 대해서는 정답을 맞추되 prefix가 너무 길면 페널티를 주는 length-shaping term을 넣었습니다(α = 0.8, β = 0.2).

전체 파이프라인은 attacker는 Mistral-7B-Instruct-v0.3에서 출발, defender는 Llama-3.2-3B-Instruct, embedding은 Qwen3-Embedding-0.6B, judge는 Qwen3Guard-Gen-8B를 씁니다. 학습은 모두 LoRA, VERL 위에서 16 × H100으로 돌렸습니다.

## 결과

공격, 방어, Guard 모드를 차례로 봅니다.

**공격 성능 (ASR@1, %, 높을수록 강함).** Qwen3-4B / Llama-3.1-8B / Llama-3.1-70B / GPT-5.1 / Gemini-3-Flash 다섯 victim에 대해 1턴 공격 성공률 평균입니다.

| 공격 방법 | Judge: Qwen3Guard | Judge: LLM |
| --- | --- | --- |
| **EvoSafety** | **92.8** | **86.3** |
| ICON (이전 최강 multi-turn) | 90.2 |  |
| Jailbreak-R1 (RL baseline) | 27.5 |  |
| EvoSafety zero-shot (held-out skill) | 84.6 | 74.8 |

1턴 만에 multi-turn 최강이던 ICON을 2.6%p 앞서고, RL 베이스라인 Jailbreak-R1과는 65.3%p 차이입니다. held-out skill만 써도 평균 84.6%로 대부분의 multi-turn 방법보다 12.18%p 높습니다. saturation 이후에도 새 skill을 라이브러리에 더하기만 하면 ASR이 회복됩니다.

**방어 성능 (ASR@1, %, 낮을수록 좋음).** skill-unseen / skill-seen / co-evolved attacker 세 가지 공격을 4B / 8B / 70B victim에 걸어 측정한 평균입니다.

| 방어 방법 | 평균 ASR (%) | Reasoning 성능 저하 (%p) |
| --- | --- | --- |
| **EvoSafety (Ours+)** | **6.93** |  |
| EvoSafety | 11.62 | **−0.29** |
| TriPlay-RL (이전 co-evolutionary 최강) | 19.92 | −2.15 |

가장 강한 베이스라인 TriPlay-RL 대비 40% 이상 낮추면서, 일반 reasoning 성능 저하는 거의 없습니다.

**Guard 모드 필터링 정확도 (%, 높을수록 좋음).** attack-successful 프롬프트를 얼마나 잘 거르느냐, victim별로.

| Guard 모델 | 파라미터 | vs Qwen3-4B | vs Llama-3.1-8B | vs Llama-3.1-70B |
| --- | --- | --- | --- | --- |
| **EvoSafety defender** | **3B** | **98.89** | **98.14** | **99.47** |
| Qwen3Guard-8B | 8B | 72.15 | 61.31 | 86.80 |
| [[Llama]]-Guard-3-8B | 8B | 47.51 | 34.67 | 65.13 |

3B 모델이 8B 모델을 14.13~24.92%p 앞서면서 benign 입력에 대한 false positive도 거의 없습니다 (GSM8K 100, MMLU 99.47). 논문 abstract의 *99.61% defense success rate, Qwen3Guard-8B 대비 14.13%p, 파라미터 37.5%*라는 표현이 여기서 나옵니다.

**공진화와 신규 skill 흡수.** 4 라운드에 걸쳐 attacker ASR은 단조 증가, defender ASR은 단조 감소합니다. 새 공격 기법이 나왔을 때 그 skill로 추가 학습한 결과(Table 4)는 다음과 같습니다.

| 신규 skill 흡수 후 | victim | ASR before → after (%) |
| --- | --- | --- |
| Steer 모드 | Llama-3.1-70B | 12.54 → **2.31** |
| Guard 모드 | Qwen3-4B | **100** (전 라운드 미측정) |
| Guard 모드 | Llama-3.1-8B | **100** (전 라운드 미측정) |

기존에 방어하던 공격이나 reasoning 성능 저하 없이 그렇게 됩니다.

## 회고

저자들이 명시적으로 짚는 한계는 두 부류입니다.

하나는 reward design에 들인 trick들이 본질적으로는 미봉책이라는 점입니다. Early-Stage Alignment Gating은 attacker의 reward hacking을 가두지만, similarity threshold τ에 민감합니다. defender 쪽의 length-shaping term도 hyperparameter에 의존합니다.

다른 하나는 외재화의 한계가 그대로 외재화 자체의 한계라는 점입니다. skill library에 없는 완전히 새로운 attack vector가 등장하면 retrieval이 빈손으로 돌아옵니다. 논문이 강조하는 lifelong 특성은 어디까지나 "skill을 손으로든 자동으로든 라이브러리에 계속 넣을 수 있다"는 전제 위에 서 있습니다. memory bank도 마찬가지로 운영 비용이 누적됩니다.

여기서 명시되지 않은 더 큰 의문은 모델 내부의 intrinsic safety가 약해진 모델(예를 들어 의도적으로 safety alignment를 제거한 open-weight 변형)에서 Steer 모드가 얼마나 먹힐지입니다. prefix로 활성화시킬 안전 메커니즘 자체가 없으면 Guard 모드만 남게 됩니다.

## 정리

- safety는 모델 안에 새겨야만 한다는 통념을 깨고, 공격 / 방어 양쪽을 모델 외부 구조(skill library + memory bank + 경량 디펜더)로 옮긴 첫 RL 기반 프레임워크입니다.
- 3B 디펜더 한 번 학습으로 4B에서 70B victim까지 평균 11.62% ASR을 달성하고, Qwen3Guard-8B를 14.13%p 차이로 누릅니다. reasoning 성능 저하는 -0.29%로 거의 없습니다.
- 한국 기업이 자체 LLM을 운영하면서 모델을 GPT-5에서 5.5, 5.6으로 갈아끼우는 상황을 생각하면, safety layer를 모델과 분리해 두는 이 발상은 그 자체로 검토할 만합니다. 모델은 자주 바뀌지만 사고 사례와 공격 스킬은 누적되기 때문입니다.
