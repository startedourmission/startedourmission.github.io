---
type: person
description: 화중과기대(HUST) 박사과정 연구원. 이미지 인페인팅 특화. PixelHacker(2504.20438), Moebius(2606.19195) 제1저자.
tags:
  - 컴퓨터비전
  - 확산모델
last_active: 2026
papers:
  - Moebius - 0.2B Lightweight Image Inpainting Framework with 10B-Level Performance
  - PixelHacker - Image Inpainting with Structural and Semantic Consistency
star: 0
---

## 개요

쉬 즈양(Xu Ziyang, 徐子阳)은 [[화중과학기술대학교]](HUST) [[HUST Vision Lab]] 소속 박사과정 연구원입니다. 지도 교수는 [[Xinggang Wang]]이며, 이미지 인페인팅 분야를 주력 연구 주제로 삼고 있습니다. 2025년 PixelHacker, 2026년 Moebius를 제1저자로 발표하며 빠른 성장을 보여 주고 있습니다.

두 논문 모두 동료 연구원 [[Kangsheng Duan]]과 공동 제1저자 체제로 작성되었으며, 이미지 복원의 품질과 효율이라는 두 방향을 나누어 탐구하는 연구 흐름을 함께 만들어 가고 있습니다. Moebius에서는 사실상 프로젝트 리더 역할을 맡아 논문 전반을 이끌었습니다.

## 생애

쉬 즈양은 화중과학기술대학교에서 학사 과정을 마친 뒤 동 대학원에 진학해 [[Xinggang Wang]] 교수 지도 아래 박사 과정을 밟고 있습니다. HUST Vision Lab은 객체 검출, 추적, 생성 모델 등 컴퓨터비전 폭넓은 분야를 다루는 그룹으로, 쉬 즈양은 그 안에서 이미지 복원 및 확산 모델 경량화에 집중해 왔습니다.

박사 과정 초반부터 arXiv에 연속으로 논문을 올리며 성과를 냈다는 점에서, HUST Vision Lab이 박사생에게 주도적인 연구 역할을 부여하는 환경임을 엿볼 수 있습니다. PixelHacker 발표 당시 공저자 목록에는 Wang 교수 외에도 Xiaolei Shen, Zhifeng Ding, Wenyu Liu, Xiaohu Ruan, Xiaoxin Chen 등이 포함되어 있어 실험실 내 다양한 구성원이 협력하는 방식으로 연구가 진행되었습니다.

## 업적

쉬 즈양의 첫 주요 성과는 PixelHacker(arXiv 2504.20438)입니다. 이 연구는 잠재 카테고리 가이던스(Latent Categories Guidance, LCG) 패러다임을 새롭게 제안해, 전경 116개 및 배경 21개 카테고리 정보로 인페인팅 과정을 안내합니다. 1,400만 장 규모의 이미지-마스크 쌍 데이터셋을 구축해 공개했으며, Places2, CelebA-HQ, FFHQ 벤치마크에서 구조적 및 의미적 일관성 면에서 당시 최고 성능을 기록했습니다.

두 번째 성과는 Moebius(arXiv 2606.19195)입니다. 0.2B 파라미터만으로 10B급 대형 모델 수준의 인페인팅 성능을 재현하는 것이 핵심 목표로, Local-lambda Mix Interaction(LlMI) 블록을 핵심 구성 요소로 도입해 공간 맥락과 전역 의미 정보를 고정 크기 선형 행렬로 압축합니다. 산업 배포에 직결되는 추론 비용 절감을 실현했다는 점에서 실용적 의의가 높습니다.

## 여담

PixelHacker에서 Moebius로 이어지는 연구 흐름은 두 편 모두 동일한 주제(이미지 인페인팅)를 다루지만 해결하려는 문제의 축이 다릅니다. PixelHacker는 대규모 데이터와 카테고리 가이던스로 품질을 극한까지 밀어붙였고, Moebius는 그 품질을 훨씬 작은 모델로 옮겨 내는 효율화에 집중했습니다. 이 두 방향은 산업 응용에서 함께 필요한 것으로, 연구 시리즈의 일관성이 잘 드러납니다.

뫼비우스 띠에서 이름을 따온 Moebius라는 제목도 흥미롭습니다. 대형 모델과 경량 모델의 경계를 연속적으로 연결한다는 의미를 담고 있어, 논문 제목 자체가 연구 의도를 함축하고 있습니다.

## 주요 논문

- PixelHacker: Image Inpainting with Structural and Semantic Consistency (arXiv 2504.20438, 2025)
- Moebius: 0.2B Lightweight Image Inpainting Framework with 10B-Level Performance (arXiv 2606.19195, 2026)
