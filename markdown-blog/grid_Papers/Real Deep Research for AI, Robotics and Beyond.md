---
date: 2025-10-30
tags:
  - 논문
  - 데이터분석
aliases:
image: "![[1-rdr.png]]"
description: |-
  매년 10,000개가 넘는 논문이 나옵니다. AI와 로봇 분야는 새로운 트렌드가 계속 생겨나고, 한 분야의 전문가도 다른 분야를 따라가기 어렵습니다. 제가 물어오는 논문도 전체 논문 수에 비하면 아주, 아주 아주 일부분일 뿐이니까요.

  RDR(Real Deep Research)은 수천 개의 논문을 체계적으로 분석하여 과제 트렌드를 파악하고, 분야 간 협력 기회를 찾아내는 파이프라인을 제시합니다..

  그래도 ,, 제 스레드 팔로우 해주실거죠?
---
RDR은 embedding 기반의 자동화된 분석 파이프라인으로, 논문 수집, 콘텐츠 분석, embedding 기반 클러스터링, 추세 분석을 통해 연구 분야를 종합적으로 파악합니다. Foundation Models과 Robotics를 중심으로 적용되었으며, Computer Vision, NLP, Machine Learning 등 다양한 분야로 확장되었습니다.

![[1-rdr.png|654x310]]



> X. Zou, J. Ye, H. Zhang, X. Xiang, M. Ding, Z. Yang, Y. J. Lee, Z. Tu, S. Liu, and X. Wang, "Real Deep Research for AI, Robotics and Beyond", arXiv preprint arXiv:2510.20809, 2025.

## 요약

RDR은 대규모 논문 데이터를 자동으로 분석하여 연구 트렌드를 파악하고 학제간 연구 기회를 발견하는 파이프라인입니다. 주요 구성요소는 다음과 같습니다.

**아키텍처**: 4단계 파이프라인으로 구성됩니다 - (1) 데이터 준비 및 필터링, (2) LLM 기반 콘텐츠 추론, (3) 임베딩 공간으로의 투영, (4) 임베딩 분석 및 시각화

**사용 모델**:

- 경량 작업용 Doubao 언어 모델
- 복잡한 추론 작업용 o3 모델
- 텍스트 임베딩용 nvidia/NV-Embed-v2

**데이터셋**: 2021-2025년 주요 학회(CVPR, ECCV, ICCV, CoRL, RSS, ICRA, NeurIPS, ICLR, ACL 등)에서 수집한 37,569편의 논문. 필터링 후 foundation model 관련 4,424편, 로봇공학 관련 1,186편 추출

**평가 매트릭**:

- 설문 품질: 도메인 전문가들의 쌍별 비교를 통한 승률(winning rate)
- 임베딩 품질: AG News 및 20 News Groups 데이터셋에서 ACC, NMI, ARI 지표로 평가

**주요 결과**:

- RDR은 GPT-4 및 Gemini 기반 상용 도구 대비 평균 순위 1.30으로 최고 성능 달성
- AG News에서 84.86% 정확도, 20 News Groups에서 52.91% 정확도로 비지도 클러스터링 벤치마크 최고 성능
- 로봇공학에서 teleoperation, dexterous manipulation, low-cost open-source robotics가 상승 트렌드로 식별됨

## 논문 상세

### 1. Introduction

연구자들은 제한된 시간과 주의력으로 폭발적으로 증가하는 논문을 따라잡아야 하는 과제에 직면해 있습니다. 기존의 전문가가 작성한 서베이 논문은 깊이 있지만 많은 수작업이 필요하고 빠른 연구 진화에 적응하기 어렵습니다. 반면 자동화된 접근법은 도메인 특화 지식과 전문가 통찰력이 부족한 경우가 많습니다.

RDR은 이 두 가지 접근법의 간극을 메우고자 합니다. 체계적인 자동화와 의미 있는 전문가 기반 분석을 결합하여, 최고 수준의 연구자들이 새로운 트렌드를 추적하고 낯선 연구 영역에 진입하는 것을 지원합니다. 특히 학제간 탐색에 초점을 맞춰, 연구자들이 분야 간 교차점에서 유망한 협력 기회를 찾을 수 있도록 돕습니다.

### 2. Related Work

**Foundation Models 서베이**: 최근 여러 서베이 연구들이 다양한 도메인에서 foundation model을 체계적으로 리뷰했습니다. 하지만 이러한 서베이들은 방대한 수작업이 필요하고, foundation model의 빠른 발전으로 인해 빠르게 구식이 됩니다. RDR의 목표는 수천 편의 논문을 자동으로 분석하고 다양한 연구 영역에 대한 최신 이해를 제공하는 프레임워크를 설계하는 것입니다.

**과학 연구에서의 LLM**: 대규모 언어 모델은 아이디어 생성, 코딩, 논문 리뷰, 실험 결과 예측 등 과학 연구의 다양한 단계에 적용되어 왔습니다. 문헌 분석은 중심적인 역할을 하며, 논문 검색, 클러스터링, 토픽 트렌드 분석 등의 작업을 포함합니다. SciLitLLM은 지도 학습으로 과학 문헌 이해를 위한 특화 LLM을 구축하고, PaSa는 강화 학습으로 복잡한 학술 질의를 답할 수 있는 LLM 에이전트를 훈련시킵니다. 기존 연구가 주로 연구 질문 답변에 집중한 반면, RDR은 전체 연구 영역에 대한 더 넓고 체계적인 이해를 목표로 합니다.

**지식 구조화와 발견**: LLM이 문서를 클러스터링하고 잠재 토픽을 발견할 수 있다는 것이 입증되었습니다. Knowledge Navigator는 LLM과 클러스터링 기법을 결합하여 과학 문헌 검색을 위한 문서를 구조화하고, SciTopic은 문서 임베딩을 정제하여 토픽 구조 식별에서 LLM을 향상시킵니다. RDR은 LLM의 추론 능력과 foundation model의 임베딩 표현을 활용하여 더 정확하고 의미론적인 지식 구조화를 제공하는 새로운 접근법을 소개합니다.

### 3. Method

#### 3.1. Data Preparation

**Selection**: foundation model과 로봇공학의 통합을 체계적으로 조사하기 위해, 학계와 산업계의 최신 트렌드와 연구 우선순위에 초점을 맞춥니다. 최신 개발 사항을 포착하기 위해 컴퓨터 비전, 로봇공학, 머신러닝의 주요 학회에서 최근 출판물을 검토합니다. 구체적으로 웹 크롤링을 통해 주요 학회(CVPR, ECCV, ICCV, CoRL, RSS, ICRA, NeurIPS 등)와 산업 연구 플랫폼(Nvidia, Meta, OpenAI 등)에서 논문을 수집합니다.

**Area Filtering**: 수집된 논문 집합 $P$는 일반적으로 비전, 언어, 머신러닝, 로봇공학의 넓은 영역에 속하지만, 각 논문이 foundation model($D_f$)과 로봇공학($D_r$)이라는 특정 초점과 직접적으로 일치한다고 보장할 수 없습니다. 이를 해결하기 위해 효율적인 LLM과 큐레이션된 프롬프트를 활용하는 Area Filtering을 도입합니다.

필터링 후 결과 논문 집합 $P'$는 foundation model 도메인, 로봇공학 도메인, 또는 둘 다에 속하게 됩니다: $P' = {p | p \in D_f \cup D_r}$

#### 3.2. Content Reasoning

필터링된 논문 $P'$에 대해 심층 분석이 필요합니다. foundation model과 로봇공학의 도메인 전문가들의 지도로, 확립된 도메인 구조, 떠오르는 트렌드, 진화하는 지식과 일치하는 관점(perspectives)을 정의합니다.

**Foundation Model**: foundation model의 개발은 5가지 기본 관점으로 체계적으로 분석됩니다:

- **Input (I)**: 원시 데이터와 토큰화 절차 (이미지, 비디오, 오디오, LiDAR 등)
- **Modeling (M)**: 입력에서 중요한 지식을 추출하고, 추론하며, 출력 공간으로 디코딩
- **Output (O)**: 입력과 모델링에 따라 디코딩 공간 결정
- **Objective (W)**: 학습 목표로 모델 분포를 제약
- **Recipe (R)**: 모델 가중치를 조정하는 방법에 대한 쿡북

형식적으로: $D^{P'}_{f} = \bigcup_{p \in P'} F(p)$, where $F(p) = \text{LLM}(p | I, M, O, W, R)$

**Robotics**: 로봇공학 연구의 경우, 핵심 관점은 하드웨어와 실제 환경과의 상호작용을 강조하는 방향으로 전환됩니다:

- **Input Sensor (S)**: 물리량이나 환경 조건을 측정하는 하드웨어 장치
- **Physical Body (B)**: 환경과의 물리적 상호작용을 가능하게 하는 기계 구조
- **Action Space (A)**: 주어진 컨텍스트에서 로봇이 선택할 수 있는 모든 허용 가능한 행동
- **Joint Output (J)**: 실행된 모터 명령으로부터 발생하는 로봇 관절의 물리적 움직임
- **Environment (E)**: 로봇이 작동하는 물리적 공간

형식적으로: $D^{P'}_{r} = \bigcup_{p \in P'} F(p)$, where $F(p) = \text{LMM}(p | S, B, J, A, E)$

#### 3.3. Content Projection

추출된 콘텐츠를 정보가 풍부한 잠재 공간으로 투영하기 위해, nvidia/NV-Embed-v2와 같은 사전 학습된 임베딩 foundation model $G$를 사용합니다.

임베딩 절차: 모든 텍스트 조각 $x \in D$에 대해 $v_x = G(x) \in \mathbb{R}^d$

핵심 가정은 관점 인식 임베딩 프로세스를 통해 논문 콘텐츠를 투영하고 고차원 매니폴드에서 분석함으로써, 체계적인 시각화와 클러스터링 분석을 통해 의미 있는 패턴, 연구 트렌드, 문헌의 잠재적 격차를 발견할 수 있다는 것입니다.

#### 3.4. Embedding Analysis

임베딩 분석의 목표는 이전에 추출된 임베딩의 이해를 구조화하는 것입니다. 파이프라인은 세 가지 구성요소를 포함합니다:

1. **Clustering for Embeddings**: 모든 논문을 임베딩하여 벡터 표현 $V$를 얻고 말뭉치를 $k$개의 클러스터로 분할합니다. 각 클러스터에서 50개의 논문을 무작위로 샘플링하고 추론 기반 모델에 입력하여 클러스터의 핵심 테마를 포착하는 세 개의 간결한 키프레이즈를 반환받습니다.
    
2. **Structuring for Thoughts**: 클러스터된 임베딩과 관련 토픽 키워드를 배치한 후, o3 언어 모델을 활용하여 주어진 연구 영역에 대한 구조화된 서베이를 생성합니다. 클러스터링 결과를 프롬프트에 포함시켜 생성된 텍스트가 연구 환경의 실제 구조에 근거하도록 합니다.
    
3. **Citation Mapping**: 각 하위 주제에 대해 가장 관련성 높은 인용문을 포함하여 독자들이 더 탐색할 수 있는 직접적인 참조를 제공합니다.
    

### 4. Analysis

#### Embedding Analysis - General

임베딩 분석의 출력은 특정 연구 도메인에 맞춤화된 포괄적인 서베이입니다. 이 서베이는 주요 카테고리와 하위 카테고리로 구성되며, 각각 다루는 특정 주제를 상세히 설명합니다. 각 하위 주제에 대해 더 탐색을 위한 가장 관련성 있는 인용문을 포함합니다.

예를 들어, 로봇공학 도메인의 서베이는 다음과 같이 구성됩니다:

- **Perception & Mapping**: Multimodal sensor fusion, 3D reconstruction/occupancy, BEV mapping
- **Manipulation & Grasping**: Dexterous grasping, Generalist manipulation, Tactile-vision fusion
- **Locomotion & Navigation**: Legged locomotion control, Embodied VL navigation
- **Planning & Control**: Language/hierarchical planning, Diffusion/Transformer policies

#### Embedding Analysis - Perspective

도메인에 대한 명확한 개요를 확립한 후, 목표 관점을 통해 분석하여 구조와 문제 공식화를 노출합니다. 예를 들어, 로봇공학을 action space 관점에서 분석하면:

- **Continuous Low-Level Actuation**: Joint-space commands, Vehicle/body dynamics commands
- **Mid-Level Pose & Trajectory Control**: End-effector & gripper pose, Base/waypoint trajectories
- **High-Level Discrete Skills**: Manipulation skills, Locomotion & navigation skills, Interaction skills

#### Trend Analysis

각 도메인과 핵심 하위 관점을 이해한 후, 다음 단계는 토픽의 모멘텀을 평가하는 것입니다. 트렌드 분석은 최근 몇 년간 어떤 영역이 가속화되고 있고 어떤 영역이 철저히 탐구되었는지를 강조합니다.

로봇공학의 경우, 다음과 같은 트렌드가 관찰됩니다:

- **상승 중**: Teleoperation, Dexterous Manipulation, Low-Cost Open-Source Robotics
- **성숙 단계**: Traditional Reinforcement Learning, Skill-Based Manipulation

#### Knowledge Graph

개별 연구 영역 내의 트렌드 토픽을 식별하는 것 외에도, 학제간 테마를 발견하는 것이 중요합니다. Computer Vision, NLP, Machine Learning, Robotics 네 가지 주요 도메인 간의 교차점을 분석합니다.

Cross-Domain Topology Graph에서 각 색상은 특정 연구 도메인에 해당하고, 각 노드는 임베딩 기반 분석에서 도출된 고유한 토픽 클러스터를 나타냅니다. 노드 간의 엣지는 의미론적 또는 토픽적 관계, 특히 도메인 경계를 넘는 관계를 나타냅니다.

#### Retrieval Examples

목표 연구 토픽이 식별되면, 다음 단계는 구체적인 진입점을 정확히 찾는 것입니다. 이전에 추론된 학회 수준 임베딩을 활용하여 의미론적 검색을 실행하고 가장 관련성 높은 문헌을 검색합니다.

예를 들어, "dexterous manipulation generated data in 3D simulation and evaluated in real world"로 쿼리하면:

- Evaluating Real-World Robot Manipulation Policies in Simulation (2024, CoRL24, 127 citations)
- Lessons from Learning to Spin "Pens" (2024, CoRL24, 29 citations)
- General In-hand Object Rotation with Vision and Touch (2023, CoRL23, 134 citations)

### 5. Experiment

#### Dataset

공개적으로 이용 가능한 고영향력 학회들로부터 데이터셋을 큐레이션합니다. 2021-2025년의 논문을 포함하며, foundation model과 로봇공학에 초점을 맞춰 2024년 이후 foundation model 관련 4,424편, 로봇공학 관련 1,186편을 추가로 필터링했습니다.

#### Survey Quality

도메인 전문성을 가진 경험 많은 연구자들이 참여한 사용자 연구를 수행했습니다. 쌍별 비교 방법론을 채택하여, 각 비교마다 두 개의 서베이 출력을 제시하고 어느 것이 우수한 품질과 정확성을 보여주는지 판단하도록 했습니다.

결과: RDR은 평균 순위 1.30으로 모든 기준선을 능가하며 최고의 전체 성능을 달성했습니다. NLP(89.47), 로봇공학(77.78), foundation model output(94.74)과 같은 주요 도메인에서 선두를 차지했습니다.

#### Embedding Quality

임베딩의 효과를 평가하기 위해 고정된 표현 위에 학습된 단순한 선형 프로브를 사용했습니다. SciTopic이 소개한 실험 프로토콜을 따랐으며, 동일한 비지도 학습 및 평가 분할을 사용했습니다.

결과: RDR은 두 데이터셋 모두에서 최고 성능을 달성했습니다:

- AG News: 84.86% 정확도, 61.66 NMI, 65.24 ARI
- 20 News Groups: 52.91% 정확도, 56.57 NMI, 39.96 ARI

### 결론

Real Deep Research는 AI와 로봇공학 분야의 방대한 문헌을 체계적으로 분석하고, 연구 트렌드를 파악하며, 학제간 기회를 발견할 수 있는 강력한 도구입니다. 실험 결과는 RDR이 상용 LLM 도구들보다 우수한 서베이 품질과 임베딩 성능을 제공한다는 것을 보여줍니다. 이 프레임워크는 연구자들이 빠르게 변화하는 연구 환경을 탐색하고 새로운 기회를 식별하는 데 실질적인 도움을 제공할 것으로 기대됩니다.