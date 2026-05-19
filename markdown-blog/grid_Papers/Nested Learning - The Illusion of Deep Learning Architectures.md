---
date: 2026-05-14
tags:
  - 논문
  - LLM
  - 딥러닝
  - headliner
aliases:
  - "Nested Learning: The Illusion of Deep Learning Architectures"
image: "![[1-NestedLearning.png]]"
description: 트랜스포머와 모던 옵티마이저(Adam, Muon)는 사실 같은 것의 다른 레벨이라는 주장입니다. Google Research가 NeurIPS 2025에서 발표한 Nested Learning은 모델 아키텍처와 옵티마이저를 "본인의 컨텍스트 흐름을 압축하는 연상 기억"의 중첩 시스템으로 통합합니다. 이를 토대로 만든 Hope 아키텍처는 1.3B/100B 토큰 규모에서 트랜스포머·Titans·Samba를 넘기며, 10M 컨텍스트까지 성능을 유지합니다.
---

> A. Behrouz, M. Razaviyayn, P. Zhong, and V. Mirrokni, "Nested Learning: The Illusion of Deep Learning Architectures", *Advances in Neural Information Processing Systems (NeurIPS) 2025*.

딥러닝 10년의 발전은 더 좋은 아키텍처 와 더 좋은 옵티마이저 라는 두 축을 따로 굴려 왔습니다. 트랜스포머는 아키텍처고, AdamW는 옵티마이저입니다. 모델을 더 깊게 쌓고, 학습 규칙은 그 위에서 따로 도는, 분리된 두 시스템입니다.

**[[Nested Learning]]은 이 분리가 환상(illusion)이라고 주장합니다.** 옵티마이저도, 아키텍처의 각 레이어도, 본질적으로 "자기 자신의 컨텍스트 흐름을 압축하는 연상 기억(associative memory) 모듈"이라는 것입니다. 둘은 다른 *종류* 가 아니라, 다른 *업데이트 빈도* 를 가진 같은 종류의 모듈입니다. 그리고 이걸 명시적으로 인정하고 나면, 지금까지 보이지 않던 "레벨(level)"이라는 새로운 설계 축이 열린다는 것이 이 논문의 골자입니다.

저자들은 이 패러다임을 증명하기 위해 [[Hope]] 라는 자기 수정(self-modifying) 아키텍처를 만들었습니다. Hope는 760M 파라미터 + 30B 토큰 규모에서 트랜스포머·Samba·Titans보다 평균 정확도가 높고, 1.3B + 100B 토큰 규모에서는 격차가 더 벌어집니다. 10M 토큰 컨텍스트에서도 성능을 유지합니다.

## 저자

저자는 네 명뿐입니다. 모두 Google Research New York의 Algorithms and Optimization 팀에 직접 또는 부속으로 묶여 있습니다.

[[Ali Behrouz]]는 1저자입니다. Cornell 박사과정 학생이자 Google NYC의 Student Researcher로, 2025년부터 Titans → Atlas → Miras로 이어지는 메모리 모듈 시리즈를 빠르게 발표해 왔습니다. Titans가 "테스트 시점에 기억하는 법을 배우는" 장기 기억 모듈을 제안했다면, [[Nested Learning]]은 그 흐름을 메타 레벨에서 묶어 *왜* 그런 메모리 모듈이 트랜스포머의 MLP 자리를 차지할 수 있는지, *어떻게* 그것이 옵티마이저와 연결되는지를 형식화하는 작업입니다.

[[Vahab Mirrokni]]는 시니어 저자입니다. Google Fellow이자 VP, Algorithms and Optimization 그룹의 오랜 리더이며, 최근에는 Gemini Data Area Lead까지 맡고 있습니다. MIT에서 응용수학으로 박사를 받은 이론 전산학 출신입니다. 베흐루즈의 메모리 노선이 미로크니의 알고리즘·최적화 인프라와 결합하는 자리가 바로 이 논문입니다.

[[Peilin Zhong]]은 미로크니 팀의 Research Scientist입니다. Columbia에서 sketching·streaming·고차원 기하 같은 이론 알고리즘으로 박사를 받았습니다. 메모리 모듈을 "컨텍스트 흐름을 압축하는 연산자"로 형식화하고, 업데이트 빈도로 레벨을 명시적으로 정렬하는 정의가 이 사람의 시각과 닮아 있습니다.

[[Meisam Razaviyayn]]은 USC 부교수이자 Google Research의 파트타임 Research Scientist입니다. 신뢰 가능한 대규모 최적화 — min-max, 공정성, 연합 학습, 차분 프라이버시 — 가 본업입니다. 이 논문에서 새로 등장하는 Delta Gradient Descent, Delta Momentum, Multi-scale Momentum Muon(M3) 같은 학습 규칙들이 최적화 측면에서 깊이를 갖는 데 그의 합류가 중요했을 것으로 보입니다.

## 배경

현재 LLM의 한계를 저자들은 *순행성 기억상실증(anterograde amnesia)* 에 빗댑니다. 사전 학습이 끝나는 순간 모델은 새로운 장기 기억을 형성할 수 없습니다. 알 수 있는 것은 사전 학습 시점까지의 정적 지식과, 현재 컨텍스트 윈도우 안에 들어온 즉각적 정보뿐입니다. 사람의 뇌에서 해마가 새 기억을 피질로 전송하지 못하는 환자처럼, 모델은 영원히 "사전 학습 종료" 시점을 산다는 것입니다.

여기에 단순히 새 데이터로 가중치를 계속 업데이트하면 *치명적 망각(catastrophic forgetting)* 이 발생합니다. 새 작업을 배우면 기존 작업의 능력이 깎입니다. 이 문제를 풀려는 시도는 크게 두 갈래로 나뉘어 왔습니다. 아키텍처를 손보거나(메모리 모듈 추가, 외부 메모리, 게이트 등), 옵티마이저 규칙을 손보거나(EWC, orthogonal gradient descent 등). 그러나 두 갈래는 따로 다뤄졌습니다.

저자들이 출발점으로 삼는 관찰은 두 가지입니다. 

첫째, 뇌는 균일하고 재사용 가능한 구조를 갖습니다. 어린 시절 한쪽 반구를 제거하는 hemispherectomy 수술 후에도 환자가 거의 정상적으로 인지 기능을 유지하는 임상 사례가 그 증거입니다. 

둘째, 뇌의 각 부분은 서로 다른 *시간 척도* 로 정보를 처리합니다. Gamma(30~150 Hz), Beta(13~30 Hz), Delta·Theta(0.5~8 Hz)가 각각 감각 정보 통합, 능동적 사고, 기억 통합과 학습을 담당합니다.

이 두 관찰을 머신러닝 모델 설계에 옮기면, "균일한 구조의 모듈들이 서로 다른 빈도로 업데이트되는 시스템"이 됩니다. 그리고 그게 사실 트랜스포머의 attention(빈도 ∞)과 MLP(빈도 1) 사이에 이미 존재하던 구분이라는 것이 저자들의 주장입니다. 다만 우리가 그렇게 보지 않았을 뿐입니다.

## 어떻게 풀었나

[[Nested Learning]] 패러다임은 세 단계로 구성됩니다.

**연상 기억의 일반 정의(Definition 1).** 

키 집합 K에서 값 집합 V로의 매핑을 학습하는 연산자 M이 연상 기억입니다. 신경망의 한 레이어를 역전파로 학습시키는 과정 자체가 사실 입력을 그 출력의 *놀라움(local surprise)* 값에 매핑하는 연상 기억이라는 것이 첫 번째 결정적인 재해석입니다. 즉 "학습"과 "기억"이라는 별개 단어로 부르던 두 가지가 형식적으로 같은 객체가 됩니다.

**업데이트 빈도로 레벨을 정렬(Definition 2).** 

각 컴포넌트의 가중치가 단위 시간당 몇 번 업데이트되는지를 *빈도 f* 로 정의합니다. 빈도가 높을수록 상위 레벨, 낮을수록 하위 레벨입니다. 트랜스포머에서 self-attention은 매 토큰마다 캐시를 갱신하니 빈도 ∞이고, MLP의 가중치는 사전 학습 동안만 업데이트되니 빈도가 사실상 0입니다. 모멘텀 옵티마이저는 매 스텝 갱신되므로 사이 어딘가에 위치합니다.

**연상 기억의 중첩 시스템(Definition 4, NSAM).** 

빈도로 정렬된 K개의 레벨로 구성되는 시스템이 NSAM(Nested System of Associative Memories)입니다. 각 레벨은 자기만의 손실 함수와 컨텍스트를 갖고, 자기 레벨의 그래디언트 descent로 업데이트됩니다. 트랜스포머든 RNN이든 Mamba든 RWKV든, 모던 시퀀스 모델은 모두 이 정의의 인스턴스라는 것이 저자들의 주장입니다.

레벨 간 *지식 전달(knowledge transfer)* 은 네 가지 방식으로 정리됩니다. 

1. 직접 연결(parametric): 한 레벨의 출력이 다른 레벨의 weight를 조건짓는 방식. 
2. 비파라메트릭 직접 연결: softmax attention처럼 컨텍스트만 조건짓는 방식. 
3. 역전파를 통한 연결: 두 레벨이 같은 그래디언트 흐름을 공유하지만 빈도는 다른 경우. 
4. 초기화를 통한 연결: MAML이 대표적인 케이스로, 상위 레벨이 하위 레벨의 초기점을 학습합니다.

이 형식화의 결과 중 핵심 두 가지는 다음과 같습니다.

**역전파 자체가 자기 참조적(self-referential) 연상 기억.** 

§4.1에서 저자들은 역전파를 통한 가중치 업데이트가 본질적으로 "입력을 해당 레이어의 local error signal에 매핑하는" 연상 기억의 학습이라는 것을 보입니다. 더 나아가 이는 단순한 선형 어텐션이 아니라 자기 자신의 값(target)을 자기 자신이 생성하는 *자기 참조적* 과정이라는 점이 §4.5에서 강조됩니다.

**옵티마이저가 곧 연상 기억.** 

모멘텀이 있는 SGD, Adam, AdaGrad, Muon, Lion 같은 옵티마이저들은 사실 "과거 그래디언트를 자신의 파라미터로 압축하는 연상 기억 모듈"이라는 점이 §4.2와 Appendix B에서 입증됩니다. 모멘텀이 dot-product similarity를 내부 목적 함수로 쓰는 1-level associative memory라면, Adam은 L2 회귀 손실을 내부 목적으로 갖는 최적의 연상 기억이 됩니다. preconditioning은 그래디언트를 다른 좌표계로 매핑하는 또 다른 연상 기억입니다.

여기서 자연스럽게 두 가지 *생성적* 결과가 따라옵니다. 옵티마이저를 더 표현력 있는 학습 규칙으로 일반화할 수 있고(deep optimizers), 메모리 모듈을 여러 빈도의 연속체(continuum)로 일반화할 수 있다는 것입니다.

## 무엇으로 구성돼 있나

논문이 제시하는 구성 요소는 크게 셋입니다.

**Deep Optimizers.** 모멘텀 옵티마이저를 연상 기억으로 보면, 더 강한 메모리 관리 능력을 갖춘 학습 규칙을 설계할 수 있습니다.

- *Delta Gradient Descent(DGD)*: 그래디언트 디센트의 내부 목적을 dot-product similarity 대신 L2 회귀 손실로 바꾼 변형입니다(§4.5, Appendix C). 입력이 정규화되어 있을 때 Sherman-Morrison 공식으로 풀리며, 가중치의 *현재 상태* 를 반영해 적응형 decay를 갖게 됩니다.
- *Delta Momentum, Deep Momentum Gradient Descent(DMGD)*: 모멘텀 항을 단순 벡터가 아니라 linear layer 또는 MLP로 모델링해서, 더 풍부한 과거 그래디언트 매핑을 학습하게 만듭니다. 직교 작업(orthogonal tasks)에서 표준 모멘텀이 보여 주는 한계 — 최근 43스텝이 누적 모멘텀의 99%를 차지하는 — 를 넘어서기 위한 설계입니다.
- *Multi-scale Momentum Muon(M3)*: Adam, Muon, CMS의 결합으로 만든 옵티마이저입니다(Algorithm 1). 두 개의 모멘텀(빠른 것, 느린 것)을 각자 다른 빈도로 업데이트하고, 둘 모두에 Newton-Schulz 직교화를 적용합니다.

**Continuum Memory System(CMS, §7).** 기존 트랜스포머가 short-term memory(attention)와 long-term memory(MLP) 둘만 두던 이분법을 *스펙트럼* 으로 일반화합니다. 서로 다른 빈도로 업데이트되는 MLP 블록들의 체인을 만들고, 빈도가 높은 블록은 빠르게 적응하되 작은 컨텍스트만 기억하고, 빈도가 낮은 블록은 영구적 지식을 담당하는 식입니다. 망각이 일어나도 다른 빈도 블록에 같은 지식이 남아 있어 역전파를 통해 회복할 수 있다는 것이 핵심 메커니즘입니다.

**Hope 아키텍처(§8).** 위 두 가지를 합쳐 만든 자기 수정 시퀀스 모델입니다. 구조적으로는 Titans에 두 가지를 추가한 것입니다.

- *Self-modifying Titans*: 키·값·쿼리·학습률·retention gate 각각에 별도의 연상 기억을 두고, 모델이 자기 자신의 값을 컨텍스트로부터 *생성* 하게 합니다(§8.1, Eq. 83~88). DGD를 weight decay와 함께 사용해 토큰 간 상관관계를 반영합니다.
- *CMS 블록*: Titans 위에 여러 빈도의 MLP 체인을 얹어 더 큰 컨텍스트 윈도우로 확장합니다(Eq. 97).

저자들은 또한 *Hope-Attention* 이라는 변형도 함께 제시합니다. self-modifying Titans 자리에 softmax global attention을 그대로 넣고, MLP 위에 CMS만 얹은 형태입니다. "CMS 디자인 자체의 효과"를 분리해 측정하기 위한 변형으로 보입니다.

## 결과

실험은 크게 다섯 갈래입니다.

**언어 모델링과 상식 추론(Table 2).** 

760M 파라미터 + 30B 토큰 스케일에서 Hope의 Wikitext perplexity 18.68, 평균 정확도 52.28로, Titans(20.08 / 51.68), Samba(21.07 / 51.46), Transformer++(24.18 / 50.11)를 모두 넘습니다. 1.3B + 100B 토큰 스케일에서는 격차가 더 벌어집니다. Hope 14.39 / 58.04 vs Titans 15.60 / 56.82 vs Transformer++ 17.92 / 53.38. 

파라미터·토큰을 늘릴수록 attention-free 모델들 사이에서 Hope의 우위가 커지는 패턴입니다.

**Needle-In-A-Haystack(Table 1).** 

16K 컨텍스트의 가장 어려운 setting인 S-NIAH-3(uuid 검색)에서 Transformer 40.8, Titans 21.2, Hope 78.2로 크게 벌어집니다. 

attention-free 모델들 중에서 Hope가 모든 NIAH 변형에서 최고이며, 깊은 메모리(Hope, Titans)가 선형 메모리(RWKV-7, Comba, DeltaNet)를 일관되게 압도합니다.

**BABILong(Figure 9).** 

모든 대형 모델(GPT-4, GPT-4o-mini, Llama-8B+RAG)이 128K~256K 컨텍스트 부근에서 성능이 급락하는 반면, Hope는 *10M 토큰* 컨텍스트까지 성능을 유지합니다. 

RMT, ARMT, Titans 같은 다른 fine-tuned 소형 모델은 1M 이후 빠르게 떨어집니다. CMS 디자인이 만든 차이로 저자들은 해석합니다.

**클래스 증분 학습(Figure 6).** 

CLINC, Banking, DBpedia 세 데이터셋에서 Llama3-3B와 Llama3-8B의 MLP 블록을 다른 빈도로 묶어 CMS화한 Hope-augmented 모델이, in-context learning(ICL)·EWC·InCA(external continual learner) 모두를 능가합니다. 

즉 외부 학습기를 따로 두지 않고도 같은 모델 안에서 연속 학습이 가능하다는 것입니다.

**새 언어 학습(CTNL).** 

MTOB(Tanzer et al. 2024)와 Manchu(Pei et al. 2025)를 결합해 저자들이 새로 만든 *Continual Translation of a Novel Language* 작업입니다. 두 개의 새 언어를 순차적으로 학습한 뒤 영어로 번역하는 setup입니다. 

메모리 레벨이 1·2·3개인 Hope-1/2/3 variant 중, *Hope-3* 이 연속 학습 setup에서도 첫 번째(개별 학습) setup의 ICL 성능을 거의 회복합니다. 다른 모델들은 연속 setup에서 catastrophic forgetting으로 성능이 급락합니다.

**옵티마이저(Figure 11~12).** 

M3는 ImageNet-21K에서 ViT를 학습시킬 때 AdamW와 Muon보다 train/test loss가 모두 낮습니다. Ablation(Table 6)에서 Hope의 대부분 컴포넌트가 양의 기여를 합니다.

full Hope의 언어 모델링 ppl 12.24를 기준으로 DGD를 빼면 13.41, momentum을 빼면 13.58, weight decay를 빼면 13.71, CMS를 빼면 13.04로 악화됩니다. 세 가지 핵심 컴포넌트(DGD/momentum/CMS) 중에서는 모멘텀 제거의 타격이 가장 큽니다.

## 마무리

> "Is Catastrophic Forgetting Solved?"
> 
> "치명적 망각은 해소되었나?"

답은 **no** 입니다. Hope와 CMS가 일부 작업에서 망각을 줄이는 데 성공했지만, "Nested Learning 관점에서 보면 catastrophic forgetting은 압축의 자연스러운 귀결"이라고 인정합니다. 모델의 용량은 유한하고, 새 정보를 받아들이려면 무언가는 잊혀야 합니다. NL은 이 문제를 *완전히* 푸는 도착지가 아니라, *어떻게* 풀어 나갈지에 대한 로드맵이라는 입장입니다.

기술적 한계도 두 가지 언급됩니다. M3 옵티마이저는 컴퓨트 오버헤드가 있어 더 큰 네트워크로 확장할 때 어려움이 예상됩니다(Figure 12). 1.3B 모델 학습에서 M3는 Muon보다 명확히 느리고, AdaMuon과 비슷한 수준입니다. CMS도 사전 학습된 모델을 그대로 가져다 쓰는 ad-hoc 초기화 방식을 같이 제안했지만, 그 효과는 더 검증이 필요해 보입니다.

Appendix는 본문이 압축한 수식 유도(Adam이 L2 회귀 손실에 대한 최적 연상 기억임을 보이는 §B, DGD의 Sherman-Morrison 풀이를 보이는 §C)에 집중되어 있어, 별도의 한계 토론이 부록에 따로 묻혀 있지는 않습니다.

- [[Nested Learning]]은 모델 아키텍처와 옵티마이저를 별개의 두 객체로 보던 관점을 깨고, 둘 모두를 *업데이트 빈도가 다른 연상 기억 모듈의 중첩 시스템* 으로 통합합니다.
- 그 결과 (1) 옵티마이저는 Delta Momentum, DMGD, M3 같은 더 표현력 있는 학습 규칙으로 확장되고, (2) 메모리는 long/short 이분법 대신 여러 빈도의 연속체(CMS)로 일반화됩니다.
- 이를 합친 자기 수정 아키텍처 [[Hope]]는 1.3B/100B 토큰 규모에서 Transformer·Titans·Samba를 모두 넘으며, 10M 토큰 컨텍스트까지 BABILong 성능을 유지합니다. 다만 catastrophic forgetting 자체가 해결된 것은 아니며, M3는 컴퓨트 오버헤드라는 실용적 비용을 갖습니다.
