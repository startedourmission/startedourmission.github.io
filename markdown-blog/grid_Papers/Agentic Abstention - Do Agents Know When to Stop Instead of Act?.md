---
date: 2026-07-01
tags:
  - 논문
  - 에이전트
  - AI평가
  - LLM
description: LLM 에이전트가 '지금 멈춰야 할 때'를 아는지 측정하는 첫 체계적 벤치마크. 웹·터미널·QA 3개 환경 28K 샘플로 평가한 결과, 대부분의 모델은 너무 늦게, 혹은 전혀 멈추지 않는다는 사실이 드러났습니다.
image: "![[agentic-abstention-overview.png]]"
buzz: 50
---

> H. Luo, B. Wen, and L. L. Wang, "Agentic Abstention: Do Agents Know When to Stop Instead of Act?," arXiv:2606.28733, 2026.

## 저자

[[뤄한|Han Luo]]와 [[원빙빙|Bingbing Wen]]이 공동 1저자입니다. Han Luo는 University of Leeds·Southwest Jiaotong University 소속으로 LLM 심리사회적 안전 평가를 연구하다가 UW 방문 연구를 통해 이 프로젝트에 합류했습니다. Bingbing Wen은 UW iSchool 박사과정생으로, LLM abstention 서베이(TACL 2025)와 과학 QA abstention 분석(EMNLP 2024) 등 abstention 주제를 집중 연구해 왔습니다. 시니어 저자 [[루시 루 왕|Lucy Lu Wang]]은 UW iSchool 조교수 겸 Allen Institute for AI Research Scientist로, LARCH 랩을 이끌며 과학·의료 텍스트 접근성을 위한 NLP를 연구합니다.

세 저자 모두 LLM이 '말할 수 없을 때 말하지 않는 능력'을 다져온 공동체에서 나왔습니다. 이번 논문은 그 주제를 단순 답변 거부에서 에이전트 행동 제어로 확장한 자연스러운 다음 단계입니다.

## 배경

LLM 에이전트는 웹 쇼핑부터 터미널 작업까지 점점 더 많은 환경에서 실제 도구를 쥐고 움직입니다. 그런데 기존 평가 체계는 에이전트가 태스크를 완수했느냐만 묻습니다. 완수가 불가능한 상황에서 에이전트가 어떻게 행동하느냐는 거의 측정하지 않았습니다.

단순 QA에서 LLM abstention, 즉 모델이 불확실하거나 답할 수 없을 때 답변을 거부하는 능력은 오랫동안 연구되어 왔습니다. Bingbing Wen 등의 서베이(TACL 2025), AbstentionBench(Kirichenko et al., 2025) 같은 벤치마크가 이 분야를 정리했습니다. 하지만 이들은 모두 단일 턴 설정입니다. 모델이 한 번의 기회에 답하거나 거부하면 끝입니다.

에이전트 설정은 다릅니다. 에이전트는 환경을 탐색하면서 상황을 바꿉니다. 태스크가 처음에는 실현 가능해 보이다가 몇 번의 탐색 끝에 불가능하다는 사실이 드러나기도 합니다. "핑크색 거실 베개를 찾아 구매해 줘"라는 요청은 처음에는 멀쩡해 보이지만, 검색을 돌려보면 해당 제품이 카탈로그에 없을 수 있습니다. 이 순간 에이전트는 멈춰야 합니다. 계속 탐색하면 불필요한 도구 호출과 비용만 쌓입니다.

이 논문은 이 공백을 채웁니다. 에이전트가 행동을 멈춰야 하는 시점을 아는가, 그것도 타이밍에 맞게 아는가를 처음으로 체계적으로 측정합니다.

## 어떻게 만들었나

### 형식화: POMDP로 abstention 정의하기

논문은 에이전트 abstention을 POMDP 틀로 정의합니다.

$$M = (S, A, O, T, \Omega, R)$$

행동 공간은 세 가지입니다.

$$A = \{ANSWER, ABSTAIN, ACT\}$$

- $ANSWER$: 최종 답변을 제시하고 종료
- $ABSTAIN$: 태스크가 해결 불가능함을 설명하고 종료
- $ACT$: 환경과 상호작용(도구 호출, 검색 등)하고 계속

에이전트는 관찰 이력 $h_t = (o_1, a_1, \ldots, o_t)$를 기반으로 정책 $\pi(a_t | h_t)$를 따릅니다. Abstention이 정당한 시점 $w_i$가 있고, 에이전트가 실제 abstain하는 시점이 $\tau_i$일 때, $w_i \leq \tau_i < \infty$이면 성공으로 봅니다. $\tau_i < w_i$는 너무 이른 중단(premature abstention)이므로 실패입니다.

### 벤치마크 구성

논문은 세 환경에서 합계 약 28,000개 샘플을 구축했습니다.

**웹 환경 (WebShop 기반, 1,000개)**

WebShop은 실제 Amazon 상품 데이터 약 100만 건을 기반으로 한 웹 쇼핑 에이전트 환경입니다. 원래 지시문 500개(풀 수 있는 태스크)에 500개의 abstention-warranted 인스턴스를 추가했습니다.

Abstention 인스턴스는 두 종류입니다.
- Request-based: 지시문 자체가 불가능한 요청을 담고 있음. GPT-5.4-mini를 사용해 세 범주(Subjective Preference, Underspecified Intent, False Premise / Contradiction)로 재작성하고 저자들이 전수 검토
- Environment-based: 지시문은 정상이지만 목표 상품을 카탈로그에서 제거하고 Lucene 인덱스를 재빌드. 에이전트가 환경을 탐색해야만 불가능함을 알 수 있음 (Missing Target)

**터미널 환경 (Terminal-Bench 2.0 기반, 277개)**

Terminal-Bench 2.0은 레거시 시스템 설정, 연구 논문 재현, 소프트웨어 엔지니어링 문제 등 전문가 수준의 89개 태스크로 구성됩니다. 여기에 False Premise / Contradiction, Underspecified Intent, Missing Prerequisite(환경 기반) 범주로 188개를 추가했습니다.

터미널 환경에서는 스캐폴드도 변수입니다. 동일한 기반 모델(GPT-5.4-mini)에 대해 Codex CLI와 Terminus 2 두 가지 스캐폴드로 평가했습니다.

**QA 환경 (AbstentionBench 기반, 27,073개)**

AbstentionBench의 16개 데이터셋을 선별했습니다. 각 질의를 에이전트 설정으로 변환해 ANSWER / ABSTAIN / 검색 도구 호출 중 하나를 선택하는 순차 의사결정 문제로 다룹니다. Wikipedia 2026-01-01 덤프를 검색 코퍼스로 사용하고, E5-base 임베딩과 FlashRAG로 매 검색 호출마다 상위 3개 문서를 반환합니다. 최대 10회 검색.

### 평가 지표

**AbsRec@K (Abstention Recall at K steps)**

$$AbsRec@K = \frac{1}{N^+} \sum_{i \in D^+} \mathbf{1}\{w_i \leq \tau_i \leq K\}$$

$D^+$는 abstention이 정당한 에피소드 집합이고, $N^+ = |D^+|$입니다.

- Timely Recall = $AbsRec@1$: 정당한 abstention 시점에 즉시 멈춘 비율
- Overall Recall = $AbsRec@10$: 최대 10턴 내에 결국 멈춘 비율

**SPL (Success weighted by Path Length)**

$$SPL = \frac{1}{N^+} \sum_{i \in D^+} S_i \cdot \frac{L_i}{\max(P_i, L_i)}$$

$S_i$는 성공 지표, $P_i$는 실제 abstention 턴, $L_i$는 oracle 최조 정당 abstention 턴입니다. 빠를수록 높은 점수를 받습니다.

### CONVOLVE: context evolution으로 abstention 개선

CONVOLVE(CONtext eVOLution for agEnttic abstention)는 모델 파라미터를 건드리지 않고 context engineering만으로 abstention을 개선하는 방법입니다.

에이전트가 $k$번째 롤아웃을 마치면, 해당 에피소드 궤적 $\tau^{(k)}$과 abstention 여부 결과 $y^{(k)}$를 리플렉션 모델에 넘깁니다. 리플렉션 모델은 "언제 멈췄어야 했는가"를 분석해 재사용 가능한 중단 규칙 "플레이북"으로 증류합니다.

$$c^{(k+1)} = U(c^{(k)}, \tau^{(k)}, y^{(k)})$$

플레이북 $c^{(k)}$는 다음 롤아웃 전에 에이전트 컨텍스트에 주입됩니다. 단 20개의 학습 궤적만으로 이 과정을 수행합니다.

## 결과

### 에이전트는 거의 멈추지 못한다

![[agentic-abstention-results.png]]

세 환경 전반에서 대부분의 모델은 $AbsRec@1$, 즉 timely recall이 극히 낮습니다. 웹 환경에서는 8개 모델 중 6개가 10턴 후에도 $AbsRec@10 < 0.5$입니다.

| 모델 | Web AbsRec@1 | Web AbsRec@10 | QA AbsRec@1 | QA AbsRec@10 |
|------|-------------|--------------|------------|--------------|
| Llama-3.3-70B | ~0.07 | **~0.84** | ~0.29 | ~0.49 |
| Qwen3-235B | ~0.18 | ~0.55 | **0.59** | **~0.71** |
| Grok-4-Fast | ~0.12 | ~0.40 | - | - |
| GPT-5.4-mini | ~0.05 | ~0.25 | ~0.10 | ~0.34 |
| GLM-5.1 | ~0.03 | ~0.20 | ~0.10 | ~0.42 |
| Gemma-4-31B | ~0.04 | ~0.18 | ~0.08 | ~0.34 |

웹 환경에서는 Llama-3.3-70B가 결국 가장 많이 멈추지만(AbsRec@10 약 0.84), 즉각 멈추는 비율(AbsRec@1)은 0.07에 불과합니다. QA에서는 Qwen3-235B가 timely recall 0.59로 유일하게 절반을 넘습니다.

### 범주별 난이도가 크게 다르다

- 웹 환경: Missing Target(환경 탐색 후에야 불가능함이 드러남)이 가장 어렵고, False Premise는 비교적 쉽습니다. 지시문만 보면 가능해 보이는 태스크일수록 에이전트가 늦게 멈춥니다.
- 터미널: Underspecified Intent가 두 스캐폴드 모두에서 특히 어렵습니다.
- QA: False Premise와 Underspecified Intent가 Answer Unknown보다 더 어렵습니다.

### 스캐폴드가 성능을 결정한다

터미널 환경에서 동일한 GPT-5.4-mini 기반 모델도 스캐폴드에 따라 결과가 크게 달라집니다.

| 스캐폴드 | AbsRec@10 |
|---------|----------|
| Codex CLI | ~0.38 |
| Terminus 2 | ~0.18 |

에이전트 abstention은 기반 모델만의 속성이 아니라 환경과 스캐폴드의 합작 결과입니다.

### 추론 강화는 timely recall을 높이지만 overall recall을 낮춘다

웹 환경에서 Qwen3-235B의 thinking 모드는 instruct 모드에 비해 timely recall을 높이지만 overall recall을 떨어뜨립니다. 추론 능력이 강해지면 멈춰야 할 시점을 더 빨리 판단하지만, 한 번 그 시점을 놓치면 오히려 계속 탐색하는 경향이 강해진다는 뜻입니다.

### CONVOLVE: 20개 궤적으로 극적인 개선

| 방법 | Llama-3.3-70B AbsRec@1 | AbsRec@10 | SPL |
|------|----------------------|----------|-----|
| Base Model | 26.7 | 83.2 | 55.3 |
| + In-Context Learning | 55.1 | 97.0 | 77.2 |
| + CONVOLVE (70B 플레이북) | **57.4** | **100.0** | **78.9** |
| + CONVOLVE (8B 플레이북) | 55.3 | 99.0 | 76.4 |

Llama-3.3-70B 기준으로 CONVOLVE는 timely recall을 26.7에서 57.4로, overall recall을 83.2에서 100.0으로 끌어올립니다. 특히 주목할 점은 Llama-3.3-8B가 학습한 플레이북을 70B에 이식했을 때도 70B 자체 플레이북과 거의 동일한 성능이 나온다는 것입니다. 플레이북에 담긴 유용한 중단 규칙은 모델 크기와 무관합니다.

AbstentionBench와 TerminalBench에서도 CONVOLVE는 일관되게 base model과 in-context learning을 앞섭니다. Llama-3.3-70B + 70B 플레이북 기준으로 AbstentionBench AbsRec@10은 41.6에서 64.2로, TerminalBench AbsRec@10은 66.2에서 79.1로 오릅니다.

## 회고

저자들은 세 가지 한계를 솔직하게 인정합니다.

**환경의 범위.** 웹·터미널·QA 세 환경은 에이전트가 실제 직면하는 상황의 일부에 불과합니다. 장기 사용자 상태, 복잡한 멀티스텝 워크플로우, 비공개 도구 등은 다루지 않습니다. 환경 기반 abstention도 현재는 "목표 대상 부재"와 "사전 조건 부재" 위주입니다. 권한 경계, 오래된 외부 리소스, 상충하는 도구 출력 같은 형태의 infeasibility는 빠져 있습니다.

**벤치마크 오염.** 일부 모델이 사전 학습 또는 후훈련 과정에서 유사한 예제에 노출됐을 가능성을 배제할 수 없습니다. 논문은 여러 시나리오와 새로운 abstention-warranted 변형 구축으로 이 위험을 줄였지만 완전한 차단은 아닙니다.

**과도한 abstention의 역설.** Qwen3-235B-Instruct는 웹 환경 solvable 태스크에서 10턴 누적 over-abstention rate가 34%에 달합니다. 잘 멈추는 것만큼, 멈추지 말아야 할 때 멈추지 않는 것도 중요합니다. 이 트레이드오프는 벤치마크 최적화만으로는 해결되지 않으며, 실제 배포 정책과 결합되어야 합니다.

한 가지 더: 논문은 CONVOLVE를 WebShop abstention-only 서브셋으로 훈련했습니다. 플레이북이 다른 환경·모델로 얼마나 일반화되는지는 추가 연구가 필요합니다.

## 정리

- 에이전트 abstention은 단순 QA abstention과 다릅니다. 멀티턴 환경 탐색 끝에 infeasibility가 드러나는 상황을 다루며, POMDP로 형식화합니다.
- 현재 LLM 에이전트 대부분은 timely abstention이 극히 낮습니다. 결국 멈추더라도 너무 늦어서 불필요한 도구 호출을 반복합니다.
- CONVOLVE는 단 20개 궤적으로 학습한 플레이북을 컨텍스트에 주입해 timely recall을 2배 이상 끌어올립니다. 작은 모델의 플레이북도 큰 모델에 거의 그대로 전이됩니다.
