---
date: 2026-07-18
tags:
  - 정보
  - LLM
description: "Moonshot AI가 7월 16일 공개한 2.8조 파라미터 MoE 모델 Kimi K3를 분석합니다. 16개 활성 전문가 구조, 1M 컨텍스트, 오픈웨이트 공개 계획, 그리고 DeepSeek 이후 중국 오픈웨이트 AI의 현재 위치를 짚어봅니다."
image: "![[kimi-k3-thumb.png]]"
---

> 이 글은 Moonshot AI 공식 발표(2026-07-16)와 VentureBeat, Fortune, Bloomberg 보도를 바탕으로 작성했습니다.

Moonshot AI가 7월 16일 Kimi K3를 공개했습니다. 총 2.8조 파라미터, 100만 토큰 컨텍스트 창, 네이티브 멀티모달. 7월 27일에 가중치도 오픈소스로 공개 예정이어서 "역대 최대 오픈 모델"이라는 수식어가 이미 붙었습니다.

## Kimi K3의 MoE 구조

2.8조라는 숫자는 강렬하지만, 실제 추론에 쓰이는 파라미터는 그 일부입니다. Kimi K3는 Mixture-of-Experts(MoE) 아키텍처로, 896개 전문가(expert) 중 매 토큰마다 16개만 활성화됩니다.

MoE 구조의 핵심은 이렇습니다. 입력 토큰이 들어오면 게이팅 네트워크(router)가 가장 관련 있는 전문가 서브네트워크를 고릅니다. 코딩 질문엔 코드 쪽 전문가가, 수학 질문엔 수학 쪽 전문가가 활성화됩니다. 2.8T 파라미터 전부를 매번 돌리는 것이 아니라 약 $\frac{16}{896} \approx 1.8\%$만 씁니다.

이 방식은 연산 효율과 파라미터 규모를 동시에 얻습니다. 덕분에 추론 비용은 소형 Dense 모델 수준이면서 모델이 기억할 수 있는 지식의 총량은 수조 파라미터급입니다.

Kimi K2(2025년 7월, 1T/32B 활성)와 비교하면 K3는 총 파라미터를 2.8배 늘리되, 활성 파라미터 비율은 오히려 낮춰 토큰당 연산량을 억제했습니다.

## Moonshot AI와 Kimi 시리즈 흐름

Moonshot AI는 2023년 3월 칭화대·카네기멜런 출신 양즈린(Yang Zhilin)이 창업했습니다. 사명이 Pink Floyd 앨범 《The Dark Side of the Moon》에서 왔고, 창립일도 그 음반 50주년에 맞췄습니다.

초기 강점은 장문 컨텍스트였습니다. 2023년 11월 공개한 첫 Kimi는 128K 토큰 무손실 컨텍스트로 주목받았습니다. 이후 흐름은 다음과 같습니다.

| 버전 | 시점 | 핵심 |
|------|------|------|
| K1.5 | 2025-01 | 추론 특화, OpenAI o1 수준 수학·코딩 주장 |
| K2 | 2025-07 | 1T/32B 활성 MoE, 오픈웨이트, 384 전문가 |
| K2.5 | 2026-01 | 멀티모달 추가(MoonViT-3D), Agent Swarm(100 병렬 에이전트) |
| K3 | 2026-07 | 2.8T/활성 약 50B, 896 전문가, 1M 컨텍스트, 오픈웨이트 |

K2에서 K3 사이에 K2.5→K2.6→K2.7 Code가 이어졌습니다. Kimi K2.5 때 ByteDance Seed 인턴이었던 [[리신하오]](Xinhao Li)가 MoonViT-3D 비전 인코더를 설계한 것으로 알려져 있습니다. K3는 이 멀티모달 기반 위에 규모를 대폭 키운 버전입니다.

## 벤치마크에서 어디에 있나

GDPval-AA v2(44개 직업·9개 산업 실무 태스크 벤치마크) 기준:

| 모델 | GDPval-AA v2 |
|------|-------------|
| Claude Fable 5 Max | **1,815** |
| GPT-5.6 Sol Max | 1,747.8 |
| **Kimi K3** | **1,687** |
| Claude Opus 4.8 | 1,600 |

장기 에이전틱 태스크를 측정하는 AA-Briefcase에서는 2위(1,527)로 GPT-5.6 Sol Max(1,495)를 앞섰습니다.

가장 상위 프런티어 모델과 격차가 남아 있지만, "중국 오픈웨이트 모델이 프런티어 경쟁에 진입했다"는 주장은 수치로 뒷받침됩니다.

API 가격은 입력 $3/M 토큰, 캐시 히트 $0.3/M, 출력 $15/M입니다.

## DeepSeek 이후 중국 오픈웨이트 AI

DeepSeek-R1(2025년 1월)은 중국 오픈웨이트 AI가 소규모 연산으로도 프런티어 추론 성능을 낼 수 있다는 걸 처음으로 증명했습니다. 이후 Moonshot, 阿里 Qwen, 바이두, 바이트댄스가 오픈웨이트 경쟁에 뛰어들었습니다.

K3의 위치는 DeepSeek과 약간 다릅니다. DeepSeek-V3/R1이 "저비용 고효율"로 주목받았다면, K3는 파라미터 규모 자체를 끌어올리는 정공법을 택했습니다. 2.8T는 현재 공개된 오픈소스 모델 중 가장 큰 수치입니다. 2026년 5월 약 200억 달러 밸류에이션에 20억 달러를 조달한 Moonshot에게 이 규모 경쟁은 전략적 선택이기도 합니다.

오픈웨이트 공개 자체도 전략입니다. 연구자·기업이 모델 위에 파인튜닝·에이전트를 구축하면 생태계가 자사 모델을 중심으로 형성됩니다. Meta의 Llama 전략과 같은 계산입니다.

가중치 공개일(7월 27일) 이후 커뮤니티 실험 결과가 쌓이면 실제 성능 위치가 더 명확해질 것입니다.

> 출처: [VentureBeat - Kimi K3 release](https://venturebeat.com/technology/chinas-moonshot-ai-releases-kimi-k3-the-largest-open-source-model-ever-rivaling-top-u-s-systems), [Fortune](https://fortune.com/2026/07/16/moonshots-kimi-k3-pushes-chinese-ai-into-fable-level-territory/), [Bloomberg](https://www.bloomberg.com/news/articles/2026-07-17/china-s-powerful-new-moonshot-ai-model-closes-gap-with-us-rivals)
