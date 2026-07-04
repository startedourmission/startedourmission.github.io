---
date: 2026-06-15
tags:
  - 논문
  - LLM
  - 강화학습
description: PPO와 GRPO가 long-tail 어휘에서 흔들리는 이유를 파헤치고, hard mask 대신 smooth regularizer로 trust region을 구현한 DRPO를 소개합니다. 6가지 실험 설정에서 일관되게 안정적인 학습을 보여주었습니다.
image: "![[drpo-gradient-weights.png]]"
citations: 0
buzz: 35
---

> J. Yao, X. Zhou, P. Qi, W. S. Lee, L. Bo, and T. Pang, "Rethinking the Divergence Regularization in LLM RL," arXiv:2606.09821, 2026.

## 저자

[[Hunyuan|Tencent Hunyuan]]과 싱가포르국립대(NUS)의 공동 연구입니다. Tencent 측에서는 [[Jiarui Yao]](UIUC 박사과정 + Hunyuan 인턴), [[Xiangxin Zhou]], [[Liefeng Bo]], [[팡톈위]]이 참여했고, NUS에서는 [[치펑후이]]와 [[Wee Sun Lee]]가 합류했습니다.

두 그룹의 연결 고리는 DPPO입니다. [[치펑후이]]와 [[팡톈위]]은 이미 2026년 초 "Rethinking the Trust Region in LLM Reinforcement Learning"을 함께 썼습니다. 그 논문에서 ratio 기반 trust region의 한계를 이론으로 정리했고, 이번 DRPO는 그 분석 위에서 hard mask를 제거하는 다음 단계를 밟은 것입니다.

## 배경

LLM post-training에서 강화학습은 이제 필수 구성 요소입니다. 인간 피드백으로 학습하는 RLHF, 수학·코딩 문제를 검증기로 보상하는 GRPO가 대표적입니다. 어느 방식이든 핵심 과제는 같습니다. 학습 안정성입니다.

LLM RL은 구조적으로 off-policy입니다. 추론 엔진과 학습 엔진의 수치 계산이 미묘하게 다르고, 한 번 모은 배치를 여러 미니배치로 나눠 여러 번 업데이트합니다. 즉, 지금 업데이트하는 정책(policy)은 데이터를 생성한 정책(behavior policy)과 이미 달라져 있습니다.

이때 안정성을 잡는 핵심 장치가 trust region입니다. 한 스텝에서 정책이 너무 멀리 움직이지 못하도록 제한하는 것입니다. PPO가 이 역할을 하는데, 방법은 간단합니다. per-token importance ratio $r_t = \pi(y_t|s_t) / \mu(y_t|s_t)$가 $[1-\epsilon, 1+\epsilon]$ 구간을 벗어나면 gradient를 자릅니다(clipping).

문제는 LLM의 어휘가 수만 개에 이르고 분포가 극도로 long-tail이라는 점입니다. 저빈도 토큰은 확률 변화가 작아도 ratio가 폭발적으로 커집니다. 예를 들어 $\mu = 10^{-5}$인 토큰이 $\pi = 10^{-3}$이 되면 ratio는 100입니다. 반면 $\mu = 0.99$인 토큰이 $\pi = 0.80$이 되어도 ratio는 0.81에 불과합니다. 실제 분포 변화는 후자가 훨씬 크지만, ratio 기반 trust region은 전자를 더 강하게 제약합니다.

[[치펑후이]] 팀이 2026년 초 DPPO로 이 문제에 대응했습니다. ratio 대신 sampled token의 절대 확률 이동량 $|π(y_t|s_t) - µ(y_t|s_t)|$(Binary-TV)을 trust region 기준으로 쓰는 것입니다. Long-tail 어휘에서 훨씬 안정적입니다. 하지만 DPPO도 한 가지 문제를 안고 있었습니다. 여전히 binary mask입니다. 토큰이 trust region을 벗어나면 gradient를 통째로 0으로 만듭니다. 경계 근처에서 gradient가 급변하고, 벗어난 방향으로 돌아오게 유도하는 신호도 없습니다.

DRPO는 여기서 출발합니다. DPPO의 trust region 기하(geometry)는 유지하되, binary mask를 smooth regularizer로 교체합니다.

## 어떻게 만들었나

핵심 아이디어는 두 선행 논문을 교차한 것입니다.

- **SPO** (Simple Policy Optimization): PPO의 hard clipping을 smooth quadratic regularizer로 대체한 방법. Ratio 기반 trust region은 그대로지만 경계 밖에서도 corrective gradient를 제공합니다.
- **DPPO**: Binary-TV 기반 trust region. Ratio 대신 절대 확률 이동량으로 경계를 정의합니다.

DRPO는 SPO의 smooth regularizer를 DPPO의 Binary-TV trust region에 적용합니다.

DPPO의 Binary-TV 제약 $|π(y_t|s_t) - µ(y_t|s_t)| \leq \delta$는 token-adaptive ratio 제약으로 다시 쓸 수 있습니다.

$$|r_t - 1| \leq \frac{\delta}{\mu(y_t|s_t)}$$

이 제약 아래서 SPO와 동일한 방식으로 quadratic regularizer를 유도하면 DRPO의 목적 함수가 나옵니다.

$$\mathcal{L}_{\text{DRPO}}(x, \pi) = \mathbb{E}_{y \sim \mu(\cdot|x)} \left[ \sum_t r_t \hat{A}_t - \frac{|\hat{A}_t|}{2\delta} \mu(y_t|s_t)(r_t - 1)^2 \right]$$

첫 번째 항은 원래 policy gradient, 두 번째 항은 quadratic regularizer입니다. Regularizer의 곡률이 behavior probability $\mu(y_t|s_t)$로 scaling된다는 점이 핵심입니다. 이 한 가지 인수(factor)가 trust region의 기하를 ratio 공간에서 절대 확률 이동 공간으로 바꿉니다.

이 목적 함수를 미분하면 gradient에 연속 가중치 $w_t$가 붙습니다.

$$w_t = 1 - \text{sign}(\hat{A}_t(r_t - 1)) \cdot \frac{D_t^{\text{Bin-TV}}}{\delta}$$

$\text{sign}(\hat{A}_t(r_t - 1))$은 현재 업데이트가 behavior policy에서 멀어지는지($> 0$) 가까워지는지($< 0$)를 나타냅니다.

- **멀어지는 방향**: $w_t = 1 - D_t^{\text{Bin-TV}}/\delta$. Trust region 내부에서는 양수 가중치로 정상 업데이트, 경계 도달 시 가중치가 0, 경계 밖으로 나가면 음수가 되어 gradient가 역전됩니다. 정책을 경계 안으로 끌어당기는 corrective 신호입니다.
- **가까워지는 방향**: $w_t = 1 + D_t^{\text{Bin-TV}}/\delta$. Gradient가 증폭됩니다. 벗어났다가 돌아오는 방향을 장려합니다.

가중치는 $1 - 1/\delta \leq w_t \leq 1 + 1/\delta$ 범위로 유계(bounded)입니다. Binary-TV가 $[0, 1]$에 속하기 때문입니다. 반면 SPO의 ratio 기반 가중치는 저빈도 토큰에서 무한정 커질 수 있습니다.

![[drpo-gradient-weights.png]]

위 그림이 이 차이를 직관적으로 보여줍니다. 가로축은 behavior probability $\mu$, 세로축은 current probability $\pi$입니다. SPO는 $\mu$가 작아질수록 가중치가 폭발적으로 커지지만, DRPO는 전 영역에서 가중치가 유계 범위 안에 머뭅니다.

**SPO와의 정규화 비교.** 같은 quadratic 형태이지만 내부 기하가 다릅니다. SPO의 regularizer는 importance-weighted expectation에서 advantage-weighted Pearson-$\chi^2$ divergence에 해당합니다.

$$\sum_{a \in \mathcal{A}} |\hat{A}(a)| \cdot \frac{(\pi(a|s_t) - \mu(a|s_t))^2}{\mu(a|s_t)}$$

분모의 $\mu(a|s_t)$가 저빈도 토큰 편향을 일으킵니다. DRPO는 이 분모가 없습니다.

$$\sum_{a \in \mathcal{A}} |\hat{A}(a)| \cdot (\pi(a|s_t) - \mu(a|s_t))^2$$

같은 절대 확률 이동에 같은 비용을 부여하므로, 고빈도·저빈도 토큰을 대칭적으로 다룹니다.

## 무엇으로 구성돼 있나

아래 표가 네 방법의 trust region 설계를 한눈에 비교합니다.

| 방법   | 메커니즘               | Trust region 기준                                 | 가중치 $w_t$                                                           | $w_t$ 범위                    |
| ---- | ------------------ | ----------------------------------------------- | ------------------------------------------------------------------- | --------------------------- |
| PPO  | hard clip          | $\|r_t - 1\| \leq \epsilon$                     | 0 또는 1                                                              | $\{0, 1\}$                  |
| SPO  | smooth regularizer | $\|r_t - 1\| \leq \epsilon$                     | $1 - \text{sign}(\hat{A}_t(r_t-1))\|r_t-1\|/\epsilon$               | $(-\infty, +\infty)$        |
| DPPO | hard mask          | $\|\pi(y_t\|s_t) - \mu(y_t\|s_t)\| \leq \delta$ | 0 또는 1                                                              | $\{0, 1\}$                  |
| DRPO | smooth regularizer | $\|\pi(y_t\|s_t) - \mu(y_t\|s_t)\| \leq \delta$ | $1 - \text{sign}(\hat{A}_t(r_t-1))\cdot D_t^{\text{Bin-TV}}/\delta$ | $[1-1/\delta,\ 1+1/\delta]$ |

DRPO는 DPPO의 trust region 기하를 그대로 물려받되, binary $\{0, 1\}$ 가중치를 연속 $[1-1/\delta, 1+1/\delta]$ 가중치로 바꾼 것입니다.

## 결과

Qwen3-4B-Base, Qwen3-30B-A3B-Base, Qwen3.5-35B-A3B-Base, DeepSeek-R1-Distill-Qwen-1.5B 네 모델로 실험했습니다. Qwen3-30B-A3B-Base는 BF16 외에 FP8(rollout only)과 FP8-E2E(학습+추론 모두 FP8) 두 가지 저정밀도 설정도 추가했습니다. 총 6가지 설정에서 AIME 2024·2025 수학 대회 문제로 평가했습니다.

![[drpo-training-results.png]]

6개 설정 전체에서 DRPO(빨간 선)는 가장 안정적인 학습 곡선을 보이며 최종 정확도에서도 모든 베이스라인과 동등하거나 높았습니다.

눈에 띄는 결과 두 가지가 있습니다. 첫째, ratio 기반 방법(GRPO, SPO)은 저정밀도 설정에서 특히 불안정합니다. FP8-E2E 설정에서는 아예 학습이 붕괴되는 경우도 있었습니다. FP8 수치 오차가 MoE 아키텍처의 training-inference mismatch와 결합하면 ratio가 더 심하게 튀기 때문입니다.

둘째, DPPO는 ratio 기반보다는 안정적이지만 DRPO보다 수렴이 느리고 최종 정확도도 낮습니다. Qwen3-30B-A3B-Base 기본(BF16) 설정에서 DPPO는 안정적으로 학습하지만 DRPO의 최종 정확도(약 0.42)에 미치지 못합니다. Hard mask의 abrupt gradient가 수렴 속도를 늦추는 것으로 저자들은 해석합니다.

Ablation에서는 절대 advantage 가중치 $|\hat{A}_t|$의 중요성도 확인됐습니다. 이 항을 제거하면 trust region 경계가 advantage magnitude에 따라 달라져 불안정해집니다.

## 회고

저자들은 논문 마지막 절에서 중요한 교훈을 남깁니다. "목적 함수에서 어떤 divergence를 쓰느냐보다 그 divergence가 유도하는 gradient의 형태가 더 결정적입니다." KL penalty와 TV penalty를 대안으로 실험했지만 둘 다 DRPO보다 성능이 낮았습니다. 둘 다 결국 ratio 기반 또는 binary 기반 gradient를 유도하기 때문입니다.

한계로 명시된 점은 없지만, 실험 범위 자체가 수학 추론 태스크(AIME)에 집중돼 있어 코딩·QA·대화 등 다른 태스크에서의 검증은 아직 없습니다. 또한 실험에 쓴 $\delta = 12.5$라는 하이퍼파라미터가 어떻게 선택됐는지 직관적 설명이 부족합니다.

## 정리

- **문제**: PPO/GRPO의 ratio 기반 trust region은 long-tail 어휘에서 저빈도 토큰을 과도하게 제약하고 고빈도 토큰을 과소 제약합니다. DPPO가 Binary-TV로 이를 해소했지만 hard mask로 인해 경계 근처에서 gradient가 급변하고 corrective 신호가 없었습니다.
- **해법**: DPPO의 Binary-TV trust region에 SPO의 smooth quadratic regularizer를 결합해 DRPO를 제안합니다. Gradient 가중치가 연속적이고 유계이며, trust region 밖에서는 자동으로 역방향 corrective 신호를 제공합니다.
- **결과**: 모델 크기, 아키텍처(dense·MoE), 정밀도(BF16·FP8) 6가지 설정 전체에서 가장 안정적이고 효율적인 학습.
