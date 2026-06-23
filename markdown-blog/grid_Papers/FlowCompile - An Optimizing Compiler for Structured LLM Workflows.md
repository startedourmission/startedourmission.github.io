---
date: 2026-05-15
tags:
  - 논문
  - LLM
  - 오픈소스
  - 에이전트
aliases:
  - "FlowCompile"
description: 사전 정의된 워크플로 그래프 위에서 sub-agent의 모델·reasoning budget·구조 선택을 컴파일 타임에 한 번에 탐색해 정확도-지연 trade-off 집합을 만들어내는 컴파일러입니다. DSPy가 프롬프트 자동화였다면, FlowCompile은 그래프 자체의 자동화로 한 칸 더 나아간 시도입니다.
image: "![[flowcompile-overview.png]]"
buzz: 0
citations: 0
---
> Li, J., Hong, Z.-W., Shen, M., Zhang, Y., & Gan, C. (2026). *FlowCompile: An Optimizing Compiler for Structured LLM Workflows*. arXiv:2605.13647.

DSPy가 등장하고 **프롬프트는 손으로 안 짠다**는 분위기가 자리 잡았습니다. 다음 질문은 **워크플로 자체는 누가 짜느냐**로 넘어갑니다. 

LangGraph, CrewAI, AFlow 등 multi-agent 그래프를 다루는 도구가 늘어나면서, 하나의 태스크를 풀기 위해 sub-agent 여러 개를 엮는 구조가 표준이 되었습니다. 

문제는 그 다음입니다. sub-agent마다 모델은 무엇으로 할지, reasoning 토큰은 몇 개까지 줄지, 어떤 가지를 켜고 끌지를 정하는 순간 설정 공간이 폭발합니다. FlowCompile은 이 폭발하는 공간을 "런타임 라우팅"이 아니라 "컴파일"로 풀자고 주장합니다.

## 저자

1저자 Junyan Li는 UMass Amherst의 박사 과정 학생으로, Apple, NVIDIA, Microsoft Research Asia 인턴을 거치며 효율적인 LLM 시스템을 다뤄왔습니다. 

시니어 저자인 Chuang Gan은 MIT-IBM Watson AI Lab principal research staff이자 UMass Amherst 조교수로, embodied AI와 neural-symbolic reasoning을 오래 다뤄왔고 최근에는 NSF CAREER Award도 받았습니다. 

공저자 Zhang-Wei Hong, Maohao Shen, Yang Zhang은 MIT 및 MIT-IBM Watson AI Lab 소속으로, ML 시스템과 강화학습 쪽에서 활동해온 그룹입니다. 코드는 `UMass-Embodied-AGI/FlowCompile` 레포로 공개되었습니다.

## 배경

지금까지 structured LLM workflow를 효율화하는 주된 접근은 라우팅이었습니다. MaaS, MasRouter, DAAO, LLMSELECTOR 같은 방법들은 모두 inference 타임에 쿼리를 보고 모델을 고르거나 구조를 바꾸는 학습 가능한 라우터를 둡니다. 이 방식은 직관적이지만 두 가지 한계가 있습니다. 

- 라우터는 학습 시 정한 단일 정확도-지연 목표에 맞춰져 있습니다. 배포 후 "조금 더 빠르게" 같은 요구가 들어오면 다시 학습해야 합니다. 
- 라우터가 탐색해야 하는 공간은 여전히 전체 워크플로 설정 공간입니다.

DSPy는 비슷한 문제의식에서 출발했지만, 그 도구가 다룬 단위는 프롬프트와 데모입니다. 모델 선택, reasoning budget, 그래프 구조 같은 워크플로 레벨 결정은 DSPy의 주된 관심사가 아닙니다. FlowCompile은 바로 이 빈 자리, 즉 "그래프 자체의 컴파일"을 채우려고 합니다.

탐색 공간이 얼마나 큰지부터 보면 그림이 쉽게 잡힙니다. 

- sub-agent 5개
- 모델 후보 5개
- reasoning budget 4단계

sub-agent마다 (모델, 예산) 조합이 $5 \times 4 = 20$가지이고, 이걸 5개 sub-agent에 독립적으로 배정하면

$$
(5 \times 4)^5 = 20^5 = 3{,}200{,}000
$$

가지가 나옵니다. 여기에 가지를 켜고 끄는 구조 선택까지 더하면 HotpotQA 기준 약 104만 개, MATH-500 기준 약 484만 개 설정이 나옵니다. 모든 설정을 끝까지 돌려서 정확도와 지연을 측정하는 것은 현실적으로 불가능합니다.

## 어떻게 풀었나

FlowCompile의 핵심 발상은 ML 컴파일러, 특히 TVM과 Ansor에서 빌려옵니다. 신경망을 통째로 측정해 최적화하는 대신, 그래프를 작은 단위로 쪼개 각각의 비용을 한 번 측정해두고 그 결과를 composition rule로 합성해 전체 비용을 추정하는 방식입니다. FlowCompile은 워크플로를 sub-agent 단위로 쪼개고, sub-agent의 (모델, reasoning budget) 조합마다 정확도와 지연을 한 번씩만 측정합니다. 그러고 나서 워크플로 레벨 정확도와 지연은 structure-aware proxy로 합성합니다.

합성 규칙은 단순합니다. sub-agent $i$의 정확도를 $p_i$, 지연을 $t_i$, 조건 분기 가중치를 $w_i$로 두면

$$
\begin{aligned}
p_{\text{seq}}      &= \prod_i p_i, & t_{\text{seq}}      &= \sum_i t_i \\
p_{\text{OR}}       &= 1 - \prod_i (1 - p_i), & t_{\text{OR}}       &= \max_i t_i \\
p_{\text{AND}}      &= \prod_i p_i, & t_{\text{AND}}      &= \max_i t_i \\
p_{\text{cond}}     &= \sum_i w_i \, p_i, & t_{\text{cond}}     &= \sum_i w_i \, t_i
\end{aligned}
$$

식 자체가 정확할 필요는 없습니다. 이 proxy가 만족해야 할 조건은 두 가지뿐입니다. 첫째, frontier consistency. 진짜 non-dominated 설정이 proxy 추정에서도 non-dominated여야 합니다. 둘째, local order preservation. frontier 근처에서 설정 간 상대 순위가 보존되어야 합니다. 이 두 조건만 지키면, proxy는 정확한 시뮬레이터가 아니어도 탐색을 안내하기에 충분합니다.

탐색은 두 단계로 진행됩니다. 먼저 sub-agent 레벨에서 locally dominated 설정을 잘라냅니다. sub-agent 하나의 후보가 65~80개라면, 이 단계에서 6~19개까지 줄어듭니다. 그 다음 가지치기된 워크플로 설정들에 대해 proxy로 정확도와 지연을 추정하고, Kung-Luccio-Preparata의 $O(N \log N)$ non-dominated sorting으로 Pareto frontier를 뽑습니다.

## 무엇으로 구성돼 있나

탐색 공간은 세 축으로 정의됩니다. 첫째는 모델 크기로, 실험에서는 Qwen-3 패밀리의 0.6B, 1.7B, 4B, 8B, 14B를 씁니다. 둘째는 reasoning budget으로, 벤치마크에 따라 10토큰에서 16,000토큰까지 budget forcing 방식으로 강제합니다. s1 논문의 budget forcing 기법을 그대로 차용한 셈입니다. 셋째는 워크플로 구조 자체로, AFlow가 발견한 그래프를 base로 두고 각 가지를 켜고 끌 수 있게 옵션화합니다.

GSM8K, MATH-500용 수학 워크플로는 Programmer-Refiner 가지, Generator 가지 둘, Detailed Generator 가지로 구성되고, 두 가지 이상이 켜졌을 때만 SelfEnsemble이 작동합니다. HotpotQA는 Generator 셋, SelfEnsemble, Formatter로 이루어지고, LiveCodeBench는 Programmer 셋, SelfEnsemble, 그리고 테스트 실패 시 Fix를 최대 3번 시도하는 retry 가지를 가집니다.

흥미로운 부분은 sub-agent 데이터 induction 방식입니다. 라벨이 final answer에만 있다는 한계를 우회하기 위해, GPT-5 같은 reference 모델로 워크플로를 한 번 돌려서 중간 입출력을 수집하고, LLM-as-a-judge로 잘 굴러간 호출만 남겨 sub-agent별 의사 데이터셋을 만듭니다. 이 데이터셋이 각 sub-agent의 정확도와 지연을 측정할 때 ground truth 역할을 합니다. Ablation에서 reference 모델을 GPT-5-mini나 Qwen3-1.7B로 바꿔도 결과가 거의 일관되게 나옵니다.

## 결과

실험은 GSM8K, MATH-500, HotpotQA, LiveCodeBench 네 벤치마크에서 진행됐고, baseline은 세 부류입니다. 단일 모델(Qwen3-32B, QwQ-32B), 고정 워크플로(Qwen3-4B/8B), 라우터 기반(MaaS, KNN Router, Preference-Aware Router, Preference-Aware MaaS).

heterogeneous preference 설정에서 평균 expected utility 기준 FlowCompile은 85.5점으로, 가장 강한 baseline(Pref-Aware MaaS 75.8) 대비 9.7점 차이입니다. 개별 벤치마크에서도 GSM8K 89.2, MATH-500 84.2, HotpotQA 88.4, LiveCodeBench 80.1로 모든 부문에서 1위를 차지합니다.

정확도-지연 trade-off 관점에서는 더 흥미로운 숫자가 나옵니다. Qwen3-14B 풀 워크플로를 baseline으로 잡았을 때, accuracy-priority 설정은 같은 정확도를 유지하면서 평균 3.4배 빠르고, LiveCodeBench에서는 6.4배 빠릅니다. latency-priority 설정은 정확도를 비슷하게 유지하면서 평균 12.7배 빠릅니다. 구체적으로 GSM8K에서 정확도 96.02점에 지연 88.3초 (풀 baseline은 95.55점 168.3초), latency-priority 설정에서는 92.13점 10.9초까지 떨어집니다. HotpotQA F1 기준으로는 86.69점에 지연 7.8초로 baseline 86.29점 26.5초를 압도합니다.

컴파일 비용도 짚고 갈 만합니다. HotpotQA의 약 104만 개 설정을 전부 돌리려면 약 173,333시간이 들지만, FlowCompile은 32개 H100 GPU 배치로 sub-agent profiling을 약 1시간만에 끝내고, 그 뒤 합성과 탐색은 CPU에서 1초 이내에 끝납니다. proxy 검증 결과도 좋아서, accuracy 추정 평균 Spearman $\rho = 0.92$, 평균 cMAE 약 2.3 percentage point, latency cMAE 4.4초 수준입니다. 즉 proxy가 완벽한 시뮬레이터는 아니지만 순위는 잘 보존합니다.

추가 분석에서 흥미로운 결과 두 가지가 더 나옵니다. 첫째, 컴파일된 설정 집합을 KNN router의 후보 풀로 쓰면 GSM8K expected utility가 89.2에서 91.8, MATH-500은 84.2에서 90.5로 더 올라갑니다. 컴파일과 라우팅이 경쟁 관계가 아니라 보완 관계라는 뜻입니다. 둘째, MATH-500에서 induce한 sub-agent profile을 GSM8K에 그대로 옮겨 써도 expected utility 88.77 vs 86.43으로 큰 손해 없이 동작합니다. 비슷한 태스크끼리는 profile 재사용이 가능하다는 신호입니다.

## 회고

저자들이 인정하는 한계는 명확합니다. 첫째, 전체 그림은 결국 "사전 정의된 execution graph"라는 가정 위에서 돌아갑니다. ReAct처럼 추론 도중 그래프 자체가 분기되는 open-ended agentic system은 이 프레임의 바깥입니다. AFlow가 만들어준 base graph 위에서 어느 가지를 켜고 끄는지를 고를 뿐, 그래프를 처음부터 생성하지는 않습니다.

둘째, proxy는 어디까지나 ordering proxy입니다. MATH-500에서 accuracy Spearman $\rho = 0.81$로 가장 낮았는데, 정확도 추정이 어려운 태스크에서는 proxy의 신뢰도가 떨어진다는 자연스러운 결과입니다. proxy가 무너지는 영역에서는 컴파일 결과의 품질도 함께 떨어질 가능성이 있습니다.

셋째, sub-agent data induction은 reference 모델의 워크플로 trace 품질에 의존합니다. ablation에서 GPT-5-mini 정도까지는 무리 없었지만, reference 모델이 워크플로를 제대로 실행하지 못하는 도메인에서는 의사 데이터셋 자체가 흔들립니다.

넷째, latency는 H100 단일 GPU vLLM 위에서 batch size 1로 측정됐습니다. 실제 서비스 환경에서는 batching, KV cache 공유, 멀티 tenant 같은 요소가 끼어들기 때문에 절대 수치가 그대로 옮겨가지는 않습니다. 다만 trade-off 구조 자체는 deployment execution model E를 갈아 끼우는 형태로 일반화할 수 있도록 설계돼 있습니다.

## 정리

- FlowCompile은 structured LLM workflow 최적화를 런타임 라우팅이 아니라 컴파일 문제로 다시 정의해, sub-agent profile을 한 번만 측정하고 워크플로 레벨 비용은 structure-aware proxy로 합성합니다.
- 모델 크기·reasoning budget·워크플로 구조를 한 공간에서 함께 탐색해, baseline 대비 평균 expected utility 9.7점, latency-priority 설정에서 평균 12.7배 속도 향상을 달성합니다.
- 컴파일된 설정 집합은 그대로 배포해도 좋고, 그 위에 KNN 라우터를 얹어도 추가 이득이 나오는 재사용 가능한 artifact입니다. 한국 스타트업이 [[Claude]] Opus와 Haiku, GPT-5 mini, [[Qwen]] 같은 모델을 한 워크플로에서 섞어 쓰는 시나리오라면, 운영 비용을 누른 채 정확도를 유지하는 후보로 한 번 따져볼 가치가 있습니다.
