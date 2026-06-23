---
type: person
description: 화중과기대(HUST) Vision Lab 연구원. 이미지 인페인팅 분야. PixelHacker(2504.20438)·Moebius(2606.19195) 공동 제1저자.
tags:
  - 인물
  - 컴퓨터비전
  - 확산모델
last_active: 2026
papers:
  - Moebius - 0.2B Lightweight Image Inpainting Framework with 10B-Level Performance
  - PixelHacker - Image Inpainting with Structural and Semantic Consistency
star: 0
---

## 개요

두안 캉성(Duan Kangsheng, 段康生)은 [[화중과학기술대학교]](HUST) [[HUST Vision Lab]] 소속 연구원입니다. 이미지 인페인팅(image inpainting), 즉 손상되거나 마스킹된 이미지 영역을 자연스럽게 복원하는 기술을 핵심 연구 분야로 삼고 있습니다. 동료 연구원 [[Ziyang Xu]]와 함께 PixelHacker(2025)와 Moebius(2026) 두 편의 논문을 공동 제1저자로 발표하며 짧은 기간 안에 두드러진 연구 성과를 냈습니다.

두 연구 모두 HUST Vision Lab의 [[Xinggang Wang]] 교수가 교신저자를 맡고 있습니다. PixelHacker는 대규모 데이터셋과 카테고리 기반 가이던스로 인페인팅 품질을 높이는 방향을, Moebius는 0.2B 파라미터의 경량 아키텍처로 10B급 성능을 달성하는 효율화 방향을 각각 탐구하며 서로 보완적인 연구 흐름을 형성하고 있습니다.

## 생애

두안 캉성은 화중과학기술대학교에서 학업을 이어 오며 HUST Vision Lab에 합류했습니다. [[Xinggang Wang]] 교수가 이끄는 Vision Lab은 객체 검출, 시각적 표현 학습, 생성 모델 등 컴퓨터비전 전반을 다루는 연구 그룹으로, 두안 캉성은 그 안에서 이미지 복원 및 생성 모델 분야에 집중해 왔습니다.

연구 경력은 상대적으로 초기 단계이지만, 2025년과 2026년 연속으로 arXiv에 게재되며 주목을 받고 있습니다. 공동 제1저자로 함께 작업한 [[Ziyang Xu]]와의 협업이 두드러지며, 두 사람은 PixelHacker에서 Moebius로 이어지는 인페인팅 연구 시리즈를 함께 이끌고 있습니다.

## 업적

두안 캉성의 첫 번째 대표 작업은 PixelHacker(arXiv 2504.20438)입니다. 이 연구는 잠재 카테고리 가이던스(Latent Categories Guidance, LCG) 패러다임을 제안하며, 전경 116개 카테고리와 배경 21개 카테고리를 포함한 1,400만 장 규모의 이미지-마스크 데이터셋을 구축해 공개했습니다. Places2, CelebA-HQ, FFHQ 등 주요 벤치마크에서 당시 최고 성능(state-of-the-art)을 달성하며 구조적·의미적 일관성을 동시에 확보했습니다.

두 번째는 Moebius(arXiv 2606.19195)로, 경량 인페인팅 프레임워크입니다. 10B급 산업용 기반 모델의 성능을 0.2B 모델로 재현하는 것을 목표로, Local-lambda Mix Interaction(LlMI) 블록을 도입해 공간 맥락과 전역 의미 정보를 고정 크기 선형 행렬로 요약합니다. 추론 비용을 획기적으로 낮추면서도 품질 손실을 최소화한 점이 핵심 기여입니다.

## 여담

PixelHacker에서 Moebius로 이어지는 연구 흐름은 단순한 논문 연속 발표가 아니라 규모(scale)와 효율(efficiency)이라는 두 축을 동시에 탐색하는 연구 전략처럼 보입니다. 대형 모델로 먼저 품질 상한선을 높인 뒤, 그 성능을 훨씬 작은 모델로 전이하는 방식은 산업 배포를 염두에 둔 실용적 접근입니다.

Moebius라는 이름은 수학의 뫼비우스 띠에서 따온 것으로, 양면이 하나로 이어지는 위상 기하학적 구조를 연상시킵니다. 경량 모델과 대형 모델 성능 사이의 경계를 허문다는 연구 의도를 이름에 담은 셈입니다.

## 주요 논문

- PixelHacker: Image Inpainting with Structural and Semantic Consistency (arXiv 2504.20438, 2025)
- Moebius: 0.2B Lightweight Image Inpainting Framework with 10B-Level Performance (arXiv 2606.19195, 2026)
