---
type: model
description: Google Research의 동적 해상도 네이티브 비전 트랜스포머
tags:
  - 모델
  - 비전트랜스포머
  - 아키텍처
aliases:
  - NaViT
  - Native Resolution Vision Transformer
---

**NaViT**(Native Resolution Vision Transformer)는 Google Research의 비전 인코더 아키텍처로, 임의 해상도·종횡비의 이미지를 **원본 해상도 그대로** 처리할 수 있습니다.

NaViT의 핵심 혁신:
- **네이티브 해상도**: 입력 이미지를 고정 크기로 리사이즈하지 않고 원본 크기 유지
- **종횡비 유연성**: $2048 \times 28$ 같은 극도로 좁은 이미지도 처리 가능
- **토큰 효율성**: 고정 리사이즈 대비 중복 정보 감소
- **2D-RoPE**: 위치 인코딩을 2차원 회전 위치 임베딩으로 구현

[[MinerU2.5]]는 NaViT를 기초로 하며, 문서 한 줄을 고해상도로 크롭했을 때($2048 \times 28 \times 28$ 픽셀) 다양한 종횡비를 효율적으로 인코딩할 수 있습니다. 이는 Stage II (콘텐츠 인식) 단계에서 세밀한 텍스트·수식·표 인식에 필수적입니다.
