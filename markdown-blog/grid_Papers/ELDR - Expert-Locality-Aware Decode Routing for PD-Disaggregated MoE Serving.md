---
date: 2026-07-05
tags:
  - 논문
  - LLM
  - GPU
  - 머신러닝
description: "PD 분리(Prefill-Decode 분리) 환경에서 MoE 모델의 decode 지연을 5.9-13.9% 줄이는 ELDR을 제안합니다. Prefill 단계의 전문가 활성화 패턴(서명)을 활용해, 이미 해당 전문가 가중치를 캐시한 워커로 decode 요청을 라우팅합니다."
image: "![[eldr-architecture.png]]"
buzz: 37
---

> S. Choi, S. Cho, Y. Xiong, Z. Yang, Y. Kwon, and P. Cheng, "ELDR: Expert-Locality-Aware Decode Routing for PD-Disaggregated MoE Serving," arXiv:2607.00466, 2026.

## 저자

Microsoft Research 팀이 주도했습니다. Sangjin Choi, Yifan Xiong, Peng Cheng이 Microsoft Research 소속이고, [[Youngjin Kwon]]이 책임 저자입니다. Sukmin Cho와 Ziyue Yang이 공동 참여했습니다. MoE 서빙 인프라, 분산 시스템, LLM 추론 최적화를 모두 다루는 팀 구성입니다.

## 배경

대형 MoE(Mixture-of-Experts) 모델을 추론할 때 핵심 병목 중 하나는 전문가(expert) 가중치 로딩입니다. 토큰마다 전체 전문가 중 일부만 활성화하는 sparse activation이 MoE의 핵심이지만, 이것이 decode 단계에서는 예측하기 어려운 메모리 접근 패턴을 만들어냅니다.

PD 분리(Prefill-Decode disaggregation) 아키텍처는 이 문제를 구조적으로 다루려는 시도입니다. Prefill 워커 풀과 Decode 워커 풀을 분리해 각 단계의 자원을 독립적으로 확장합니다. KV cache를 네트워크로 전달해 두 단계를 이어줍니다. Prefill은 메모리 대역폭과 연산 집약적이고, Decode는 메모리 접근 대기시간에 민감합니다. 분리하면 두 단계가 서로를 방해하지 않습니다.

그런데 PD 분리만으로 decode 지연이 해결되는 건 아닙니다. Decode 워커 풀에서도 전문가 가중치를 상황에 따라 로드해야 하는데, 특정 도메인의 요청이 특정 전문가 집합에 몰리는 **전문가 지역성(expert locality)** 현상을 활용하지 않으면 그 잠재력이 낭비됩니다.

전문가 지역성은 측정 가능한 현상입니다. 같은 도메인(코딩, 수학, 일반 대화)의 요청들이 레이어별로 비슷한 전문가 집합을 활성화합니다. ELDR은 이 패턴을 오프라인에서 미리 파악해, Decode 워커마다 전담하는 전문가 지역 영역을 배정합니다. 그리고 온라인에서 들어오는 각 요청의 Prefill 서명을 보고 가장 적합한 Decode 워커로 라우팅합니다.

## 어떻게 만들었나

![[eldr-architecture.png]]

ELDR은 오프라인 클러스터링과 온라인 라우팅 두 단계로 구성됩니다.

**전문가 서명 정의.** Prefill 단계에서 각 레이어의 전문가 활성화 패턴을 서명(expert signature)으로 압축합니다. 서명은 IDF-reweighted, layer-masked L2-normalized 카운트 벡터입니다.

$$\mathbf{s}_i = \text{Norm}\left(\mathbf{W}_{\text{layer}} \odot \sum_{\ell} w_\ell \cdot \mathbf{c}_i^\ell\right)$$

여기서 $\mathbf{c}_i^\ell$는 요청 $i$의 레이어 $\ell$에서 활성화된 전문가의 one-hot 카운트 벡터, $w_\ell$은 레이어 가중치, $\mathbf{W}_{\text{layer}}$는 IDF 가중치입니다. IDF는 TF-IDF의 역문서빈도 개념을 그대로 가져옵니다. 자주 활성화되는 "범용 전문가"보다 특정 도메인에서만 활성화되는 "전문 전문가"에 더 높은 가중치를 부여합니다.

레이어 마스킹은 전문가 활성화가 집중적으로 발생하는 중간 레이어에 높은 가중치를 줍니다. 초반 레이어와 후반 레이어는 도메인 구분력이 낮아 서명 품질을 떨어뜨립니다.

**오프라인 Hungarian-balanced K-means.** 수집한 서명들을 $K$개의 지역 영역으로 클러스터링합니다. $K$는 Decode 워커 수와 같습니다. 일반 K-means는 클러스터 크기가 불균형할 수 있어 특정 Decode 워커에 요청이 쏠리는 문제가 생깁니다. ELDR은 Hungarian 알고리즘으로 클러스터 크기를 균등하게 맞춥니다.

$$\min_{\mathbf{C}} \sum_{i} \|\mathbf{s}_i - \mu_{c(i)}\|^2 \quad \text{subject to} \quad |c^{-1}(k)| \approx N/K \;\; \forall k$$

각 클러스터 $k$의 중심 벡터 $\mu_k$가 해당 Decode 워커의 "전문가 프로파일"이 됩니다. 이 프로파일에 맞는 요청을 해당 워커로 모으면, 그 워커에 캐시된 전문가 가중치 재사용률이 높아집니다.

**온라인 locality-band 라우팅.** 새로운 요청의 Prefill 서명 $\mathbf{s}$와 각 Decode 워커의 중심 $\mu_k$ 사이의 코사인 유사도를 계산합니다.

$$d_k = 1 - \cos(\mathbf{s}, \mu_k)$$

가장 유사도가 높은 워커(거리 $d_{k^*}$)에 배정하되, 과부하를 막기 위해 band 허용 범위 $\tau = 0.1$을 둡니다. $d_k \leq d_{k^*} + \tau$를 만족하는 워커 중 현재 큐 길이가 가장 짧은 곳으로 라우팅합니다.

$$\text{route}(\mathbf{s}) = \arg\min_{k:\; d_k \leq d_{k^*} + \tau} |\text{queue}_k|$$

$\tau$가 작으면 지역성이 강해지고, $\tau$가 크면 부하 균형이 강해집니다. $\tau = 0.1$은 실험을 통해 결정한 균형점입니다.

Prefill 서명은 KV cache와 함께 Decode 워커로 전달됩니다. 기존 PD 분리 아키텍처에서 KV cache를 어차피 전달해야 하므로, 서명 추가는 무시할 수 있는 크기의 부가 데이터입니다.

## 결과

실험은 4개 Decode 워커 구성에서 실시했습니다. 모델은 Mixtral-8x7B와 DeepSeek-V3를 사용했으며, 요청 트레이스는 도메인이 혼재된 실제 서빙 워크로드를 모사합니다. 핵심 지표는 TPOT(Time Per Output Token)입니다.

**Mixtral-8x7B 기준 (4 Decode 워커, TPOT):**

| 라우팅 방식 | TPOT (ms) | 기준 대비 |
| ---------- | --------- | --------- |
| 랜덤 라우팅 | 23.4 | +13.9% |
| Round-robin | 22.6 | +9.7% |
| 최단 큐 | 21.2 | +2.9% |
| **ELDR** | **20.6** | 기준 |

ELDR이 랜덤 라우팅 대비 TPOT를 13.9% 줄입니다. 이미 부하 균형을 고려하는 최단 큐 라우팅과 비교해도 2.9% 추가 개선입니다.

**DeepSeek-V3 기준 (요청 동시성 증가에 따른 TPOT):**

| 동시 요청 수 | Round-robin | 최단 큐 | ELDR |
| ----------- | ----------- | ------- | ---- |
| 32 | 18.1 | 17.4 | **16.8** |
| 64 | 21.3 | 20.2 | **19.4** |
| 128 | 26.7 | 25.1 | **23.9** |

모든 부하 수준에서 ELDR이 일관되게 우위를 보입니다. 부하가 증가할수록 전문가 캐시 미스 비용이 커지기 때문에, 지역성 이점이 고부하일수록 두드러집니다.

전문가 캐시 히트율 분석에서 ELDR은 랜덤 라우팅 대비 레이어당 평균 전문가 재사용률이 1.8배 높았습니다. 이것이 TPOT 개선의 직접 원인입니다.

## 회고

ELDR의 효과는 전문가 지역성이 실제로 강한 경우에 의존합니다. 저자들이 밝히는 두 가지 조건이 있습니다.

첫째, 도메인이 혼재되지 않은 요청 트레이스에서 효과가 더 큽니다. 코딩 요청과 수학 요청과 일반 대화가 고루 섞인 것이 아니라, 시간대별로 특정 도메인이 몰리는 실제 서빙 패턴에서 지역성이 뚜렷합니다. 완전히 균일한 랜덤 트레이스에서는 클러스터링 자체가 의미를 잃습니다.

둘째, $K$ Decode 워커 수가 클수록 각 워커가 담당하는 지역 영역이 좁아져 지역성이 강화됩니다. 그런데 워커 수가 늘어나면 KV cache 전달 대역폭과 네트워크 비용도 증가합니다. ELDR이 주는 TPOT 이득이 이 비용을 상쇄하는 균형점이 존재하며, 논문에서는 4-8 워커 범위를 권장합니다.

오프라인 K-means 클러스터링은 학습 트레이스가 실제 서빙 트레이스와 다를 때 성능이 저하됩니다. 드리프트 감지 후 주기적으로 재클러스터링하는 온라인 적응 메커니즘이 후속 연구 과제로 남아 있습니다.

## 정리

1. MoE decode에서 전문가 활성화 패턴은 도메인별로 뚜렷하게 다릅니다. 이 지역성을 Prefill 단계에서 미리 포착해 Decode 워커 배정에 쓸 수 있습니다.
2. IDF-reweighted 서명 + Hungarian-balanced K-means 클러스터링 + locality-band 온라인 라우팅을 조합해 기존 PD 분리 아키텍처에 비침습적으로 추가됩니다.
3. TPOT 5.9-13.9% 감소는 별도 하드웨어 추가나 모델 수정 없이 라우팅 정책 변경만으로 얻은 이득이라는 점에서 실용성이 높습니다.
