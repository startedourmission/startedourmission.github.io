---
type: hardware
tags:
  - 벤치마크
  - AI평가
aliases:
  - "Maia 200"
---

Microsoft Maia 200은 Microsoft가 자체 설계한 2세대 AI 가속기이다. TSMC 3nm 공정으로 제조되며, 140억 개 이상의 트랜지스터를 집적하여 대규모 AI 워크로드를 처리한다.

## 주요 사양

- **공정**: TSMC 3nm
- **트랜지스터**: 140B+ (1,400억 개 이상)
- **메모리**: 216GB HBM3e
- **성능 비교**: [[Amazon Trainium3|Trainium3]] 대비 FP4 3배, [[Google TPU v7 Ironwood|TPU v7]] 대비 FP8 상회

## 특징

Maia 200은 Microsoft가 NVIDIA GPU 의존도를 줄이기 위해 개발한 커스텀 AI 칩이다. 216GB HBM3e 메모리를 탑재하여 대규모 모델의 추론과 훈련을 모두 지원한다. FP4 연산에서 [[Amazon Trainium3]] 대비 약 3배의 성능을 제공하며, FP8 연산에서도 Google TPU v7을 상회하는 것으로 알려져 있다.

주목할 점은 Intel 18A 공정을 활용한 Maia 2 제조 계약이다. 이는 TSMC 외의 파운드리로 공급망을 다변화하려는 전략적 움직임이며, Intel의 첨단 공정 수주에도 중요한 의미를 갖는다. Azure 데이터센터에 배치되어 Copilot 및 Azure AI 서비스의 인프라로 활용될 전망이다.
