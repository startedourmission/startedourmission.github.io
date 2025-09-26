---
date: 2025-09-24
tags:
  - 논문
  - LLM
aliases:
image: "![[1-SoftTokens_HardTruths.png]]"
description: 대형 언어 모델(LLM)의 추론 능력은 Chain-of-Thought(CoT) 기법을 통해 크게 향상되었지만, 기존의 discrete token 기반 접근법은 여러 추론 경로를 동시에 탐색하는 데 한계가 있습니다. 이러한 한계를 극복하기 위해 continuous token을 사용한 새로운 강화학습 기반 훈련 방법을 제안합니다.
---
언어 모델은 텍스트를 숫자로 바꾸기 위해 토큰화 작업을 거칩니다. 보통은 discrete token이라는 단위로 처리합니다. 이 방식은 토큰을 명확하게 구분되는 하나의 단위로 처리합니다. 예를 들어 "안녕하세요"는 ["안녕", "하세", "요"]처럼 바뀝니다. 각 토큰은 vocabulary에서 고유한 하나의 위치를 차지하는 one-hot 벡터로 표현됩니다. 명확하고 이해하기 쉽지만, 추론 과정에서 한 번에 하나의 경로만 따라갈 수 있다는 한계가 있습니다. 대형 언어 모델(LLM)의 추론 능력은 Chain-of-Thought(CoT) 기법을 통해 크게 향상되었지만, 바로 이런 discrete token 기반 접근법 때문에 여러 추론 경로를 동시에 탐색하는 데 제약이 따릅니다. 본 논문은 이러한 한계를 극복하기 위해 continuous token을 사용한 새로운 강화학습 기반 훈련 방법을 제안합니다.

> N. Butt, A. Kwiatkowski, I. Labiad, J. Kempe and Y. Ollivier, "Soft Tokens, Hard Truths", arXiv preprint arXiv:2509.19170, pp. 1-24, 2024.
## 요약

**아키텍처**: 표준 Transformer 구조를 기반으로 하되, CoT 단계에서 discrete token 대신 continuous token을 사용하는 "soft token"과 "fuzzy token" 방식을 도입했습니다.

**모델**: Llama 3.1 8B Instruct, Llama 3.2 3B Instruct, Qwen 2.5 3B Instruct 모델을 기반으로 실험을 진행했습니다.

**데이터셋**: GSM8K, MATH, DeepScaleR 등 수학 추론 데이터셋에서 훈련하고 GSM8K, MATH-500, OlympiadBench에서 평가했습니다.

**평가 메트릭**: pass@1과 pass@32 정확도를 통해 성능을 측정했으며, 추가로 out-of-domain 데이터(HellaSwag, MMLU, ARC)에서 robustness를 평가했습니다.

**훈련 방법**: RLOO(Reinforce with Leave-One-Out baseline)를 사용한 강화학습 방식을 채택했습니다.

![[1-SoftTokens_HardTruths.png|371x396]]

## 논문 상세

### 배경 및 동기

기존 연구들은 continuous CoT의 이론적 장점을 입증했지만, 실제 훈련에서는 큰 어려움을 겪었습니다. 기존 방법들은 ground-truth discrete CoT에서 distillation하거나 inference 시에만 적용되어 제한적이었습니다.

### 방법론

**핵심 아이디어**는 다음과 같습니다:

1. **Soft tokens**: Temperature $\tau = 0.5$에서 확률 분포 전체를 embedding으로 사용 $$h_t^0 = p_{t-1}E + \sigma N(0, I_d)$$
    
2. **Fuzzy tokens**: Temperature $\tau = 0.0001$로 거의 discrete token에 가깝지만 noise 추가
    
3. **Noise injection**: 탐색을 위해 Gaussian noise를 embedding에 추가 ($\sigma = 0.33 \times$ RMS norm)
    

**강화학습 공식화**:

- 목표: $E_{(\tilde{h},a)\sim\pi}[R(a)]$ 최대화
- Reinforce 정리에 의해: $\log \pi(\tilde{h}^0) = \sum_t \log \pi(\tilde{h}_t^0 | \tilde{h}_{<t}^0)$
- 각 항은 $\log \pi(\tilde{h}_t^0 | \tilde{h}_{<t}^0) = -\frac{1}{2\sigma^2}|\tilde{h}_t^0 - h_t^0|^2 + \text{const}$로 계산 가능

### 실험 설계

**훈련 설정**:

- Batch size: 2 prompts × 32 samples
- 최대 CoT 길이: GSM8K (128 tokens), MATH/DeepScaleR (512 tokens)
- Reward: 정답일 때 100점, 부분 정답일 때 10점, 오답일 때 0점

**평가 설정**:

- 6가지 inference 방식 조합: Hard/Soft/Fuzzy × Greedy/Sample
- 3개 random seed로 실험 반복

### 실험 결과

**주요 발견사항**:

1. **Pass@1 성능**: Soft/fuzzy 훈련이 hard 훈련과 거의 동등한 성능을 보였습니다.
    
2. **Pass@32 성능**: Soft/fuzzy 훈련이 hard 훈련을 상회했으며, 이는 더 다양한 추론 경로 생성을 의미합니다.
    
3. **Out-of-domain robustness**: Hard 훈련은 base 모델의 negative log-likelihood를 악화시켰지만, soft/fuzzy 훈련은 이를 보존했습니다.
    
4. **특별한 경우**: Llama-8B-Instruct를 GSM8K로 훈련하고 MATH에서 평가할 때, hard 훈련은 성능이 크게 하락했지만 soft/fuzzy 훈련은 성능을 유지했습니다.
    
5. **최적 조합**: Soft/fuzzy로 훈련하고 hard inference를 사용하는 것이 가장 효과적이었습니다.
    

### 엔트로피 분석

흥미롭게도 entropy 분석에서는 다음을 발견했습니다:

- Base 모델에서 hard sampling 시 CoT가 진행되면서 entropy가 급증
- Hard 훈련 후에는 이러한 entropy 급증이 사라져 과신(overconfidence) 현상 발생
- Soft/fuzzy 훈련은 base 모델의 entropy profile을 더 잘 보존

### 의의와 한계

**의의**:

- Continuous CoT를 위한 첫 번째 scalable 강화학습 방법
- Ground-truth CoT 없이도 훈련 가능
- 기존 discrete 방식과 동등하거나 더 나은 성능
- Out-of-domain에서 더 robust한 성능

**한계**:

- 아직 수학 추론 도메인에서만 검증
- 더 큰 모델에서의 효과는 미지수
- Inference 시 soft token 사용의 이점이 명확하지 않음

## 결론

본 논문은 continuous reasoning이 단순한 이론적 호기심을 넘어 실용적인 대안이 될 수 있음을 보여줍니다. 특히 모델의 다양성을 보존하면서도 성능을 유지할 수 있다는 점에서 의미가 큽니다. 향후 연구에서는 더 다양한 도메인과 큰 모델에서의 효과를 검증할 필요가 있겠습니다.