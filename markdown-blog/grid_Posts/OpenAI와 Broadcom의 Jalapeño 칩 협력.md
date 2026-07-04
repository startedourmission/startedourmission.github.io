---
date: 2026-06-27
tags:
  - 정보
  - 반도체
description: OpenAI가 Broadcom과 공동 설계한 첫 번째 자체 AI 추론 칩 Jalapeño. TSMC 3nm 공정, 8개 HBM 스택, 9개월 개발 주기로 설계됐습니다. GPU 대비 추론 비용 약 50% 절감을 목표로 2026년 하반기 소규모 배포를 시작합니다.
image: "![[openai-broadcom-jalapeno.png]]"
---
[[OpenAI]]가 2026년 6월 24일 첫 번째 자체 AI 추론 칩 Jalapeño를 공개했습니다. Broadcom과 공동 설계했고 TSMC 3nm 공정으로 제조합니다. ChatGPT가 탄생한 이후 [[OpenAI]]의 컴퓨트 전략에서 가장 큰 전환점입니다.

## 추론 칩이 필요한 이유

AI 칩 시장을 흔히 학습(training)과 추론(inference)으로 나눕니다. GPU가 지배하는 학습 단계는 대형 언어 모델을 처음 만드는 과정입니다. 추론 단계는 모델이 만들어진 뒤 사용자 요청에 실제로 응답하는 과정입니다. ChatGPT 대화 한 번, 코드 생성 요청 하나, 이미지 생성 작업 각각이 모두 추론입니다.

[[OpenAI]] 입장에서 추론은 가장 큰 운영 비용입니다. GPT-5 시리즈 출시 후 사용량이 폭발적으로 늘면서 추론을 위한 [[NVIDIA]] GPU 구매·임대 비용이 수익성의 최대 병목이 됐습니다. [[NVIDIA]] H100·H200은 범용 GPU라 학습과 추론을 모두 처리하도록 설계됐는데, 이는 추론만 최적화하면 될 경우 비효율입니다.

Jalapeño의 목표는 정확히 이 지점입니다. 학습은 포기하고 추론에만 집중해, 트랜스포머 아키텍처의 행렬 연산과 고대역폭 메모리 이동에 최적화된 전용 ASIC을 만드는 것입니다.

## Broadcom과의 역할 분담

[[OpenAI]]는 칩 팹리스(fabless) 회사가 아닙니다. 실리콘 설계 경험도, 제조 공정도 없었습니다. Broadcom이 이 공백을 채웁니다.

역할 분담은 명확합니다. [[OpenAI]]는 모델 아키텍처와 워크로드 특성을 제공했습니다. 어떤 연산이 반복되는지, 메모리 접근 패턴이 어떤지, 배치 크기가 얼마나 되는지 등 추론 워크로드의 실제 데이터입니다. Broadcom은 이 요구사항을 바탕으로 실리콘 설계와 고성능 네트워킹 통합을 담당했습니다. 칩을 묶어 서버를 구성하는 랙 조립은 Celestica가 맡고, 제조는 TSMC입니다.

주목할 것은 개발 속도입니다. Jalapeño는 설계 시작부터 테이프아웃(최종 설계 완성)까지 약 9개월이 걸렸습니다. 고성능 ASIC 개발에 통상 3~5년이 걸린다는 점을 감안하면 이례적입니다. [[OpenAI]]는 자사 AI 모델을 칩 설계 과정에 활용해 일부 최적화 작업을 가속했다고 밝혔습니다.

## 기술 구성

Jalapeño는 리티클 한계 크기(reticle-limited)의 대형 컴퓨트 다이를 중심으로 8개의 HBM(High-Bandwidth Memory) 스택을 배치한 구조입니다. 리티클 한계란 포토리소그래피 공정에서 한 번에 노광할 수 있는 최대 면적을 의미합니다. 이 크기를 꽉 채울수록 칩 면적당 연산량을 최대화할 수 있지만, 수율 관리가 어려워집니다.

8개 HBM 스택은 대역폭을 극대화하기 위한 선택입니다. 트랜스포머 추론에서 핵심 병목은 연산 속도가 아니라 가중치를 얼마나 빠르게 메모리에서 끌어올 수 있는지입니다. HBM 스택을 늘리면 이 대역폭 병목을 완화할 수 있습니다.

아키텍처는 시스톨릭 어레이(systolic array) 기반입니다. [[Google TPU v7 Ironwood|Google Ironwood TPU]]도 같은 방식을 씁니다. 행렬 곱셈 연산을 파이프라인처럼 흘려보내는 구조로, GPU의 CUDA 범용 컴퓨팅 모델보다 행렬 연산에 특화됐습니다.

제조 공정은 TSMC 3nm(N3)입니다. 현재 양산 가능한 최선단 노드 중 하나로, 같은 다이 면적에서 더 많은 트랜지스터를 집적하고 전력 효율을 높일 수 있습니다.

## 경쟁 구도

[[OpenAI]]가 처음은 아닙니다. 자체 칩을 만들어 [[NVIDIA]] 의존도를 줄이려는 흐름은 하이퍼스케일러 전반에 걸쳐 진행 중입니다.

| 칩 | 기업 | 노드 | 특화 |
|---|---|---|---|
| [[Google TPU v7 Ironwood|TPU v7 Ironwood]] | Google | TSMC 3nm | 추론, 192GB HBM3e |
| [[Amazon Trainium3|Trainium3]] | Amazon | TSMC 3nm | 학습+추론, 144GB HBM3e |
| [[Microsoft Maia 200|Maia 200]] | Microsoft | TSMC 5nm | 학습 |
| Jalapeño | OpenAI | TSMC 3nm | 추론 특화 |

Google Ironwood TPU와 비교하면 포지션이 명확해집니다. Ironwood는 Google Cloud 고객 전체를 위한 범용 추론 플랫폼입니다. 훈련과 추론 양쪽을 수용하도록 설계됐습니다. Jalapeño는 [[OpenAI]] 자사 모델만 돌립니다. 특정 모델 아키텍처와 추론 패턴에 완전히 최적화할 수 있다는 점에서 더 공격적인 전문화가 가능합니다.

[[Amazon Trainium3]]는 학습과 추론 양쪽을 커버합니다. AWS 생태계 고객이 타겟입니다. 외부에 서비스로 제공되는 칩이라는 점에서 내부 전용인 Jalapeño와 성격이 다릅니다.

## OpenAI의 계산

Broadcom CEO 혹 탄(Hock Tan)은 인터뷰에서 Jalapeño가 현재 AI GPU 대비 킬로와트당 비용이나 토큰당 비용에서 약 50% 절감을 달성한다고 밝혔습니다. 이 수치는 내부 주장이고 독립 벤치마크로 검증된 것은 아닙니다. 공식 성능 수치는 아직 공개되지 않았습니다.

배포 일정은 단계적입니다. 2026년 하반기에 소규모 프로토타입 배포, 2027년부터 Microsoft 등 파트너와 함께 기가와트 규모 데이터센터로 확장, 2028년까지 총 약 10기가와트 용량을 목표로 합니다. 현재는 GPT-5.3-Codex-Spark 모델을 프로덕션 목표 주파수로 내부 테스트 중입니다.

[[OpenAI]]의 전략적 동기는 비용 절감만이 아닙니다. [[NVIDIA]]에 대한 공급망 의존은 단가 협상력과 생산 배정 우선순위 모두에서 [[OpenAI]]를 수동적인 위치에 놓습니다. 자체 칩이 생기면 인프라 확장 속도를 스스로 결정할 수 있습니다. Sam Altman이 거듭 강조해온 "풀 스택을 직접 구축"한다는 표현의 하드웨어 버전입니다.

아직 해결해야 할 것도 있습니다. 칩을 만드는 것과 실제로 잘 돌리는 것은 다릅니다. Google은 TPU를 수십억 달러 규모의 TensorFlow·JAX 소프트웨어 생태계와 함께 수년에 걸쳐 최적화했습니다. [[OpenAI]]가 Jalapeño 위에서 모델 성능을 끌어내려면 컴파일러, 메모리 관리, 배치 스케줄링 전 계층에서 독자 소프트웨어 스택을 다듬어야 합니다. 9개월 개발이 빠른 건 사실이지만, 그 다음이 더 긴 여정입니다.

> 출처: [OpenAI and Broadcom unveil LLM-optimized inference chip | OpenAI](https://openai.com/index/openai-broadcom-jalapeno-inference-chip/), [OpenAI unveils first custom AI inference chip, Jalapeño | VentureBeat](https://venturebeat.com/infrastructure/openai-unveils-first-custom-ai-inference-chip-jalapeno-with-broadcom-and-its-development-was-sped-up-with-openais-own-models), [Broadcom and OpenAI unveil Jalapeño | Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/broadcom-and-openai-unveil-custom-built-jalapeno-inference-processor-openais-first-chip-is-a-massive-reticle-sized-asic-built-in-an-ultra-fast-nine-month-development-cycle)
