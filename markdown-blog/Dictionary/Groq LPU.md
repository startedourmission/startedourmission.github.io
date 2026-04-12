---
type: hardware
tags:
  - 벤치마크
  - AI평가
aliases:
  - "LPU"
  - "Groq"
---

Groq LPU(Language Processing Unit)는 Groq이 개발한 초저지연 AI 추론 전용 프로세서이다. 온칩 SRAM 기반 아키텍처를 채택하여 외부 메모리 접근 없이 결정론적(deterministic) 연산을 수행한다.

## 주요 사양

- **아키텍처**: 온칩 SRAM 기반
- **Llama2-70B 추론**: 300 tok/s
- **7B 모델 추론**: 750 tok/s
- **TTFT (Time To First Token)**: sub-100ms
- **최적화 대상**: 초저지연 추론

## 특징

LPU는 GPU나 TPU와 근본적으로 다른 설계 철학을 가진다. HBM 대신 온칩 SRAM만을 사용하여 메모리 접근 지연을 최소화했으며, 이를 통해 예측 가능하고 일관된 성능을 제공한다. TTFT(첫 번째 토큰 생성까지의 시간)가 100ms 미만으로, 체감 응답 속도가 극히 빠르다.

Llama2-70B에서 300 tok/s, 7B 모델에서 750 tok/s의 추론 속도를 달성하며, 이는 동급 GPU 기반 시스템 대비 수 배 빠른 수치이다. 다만 훈련에는 적합하지 않으며, 추론 전용으로 설계되었다. 실시간 대화형 AI 서비스, 챗봇, 코드 생성 등 지연 시간이 중요한 워크로드에서 강점을 발휘한다.
