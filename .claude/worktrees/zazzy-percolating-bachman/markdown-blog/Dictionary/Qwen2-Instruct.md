---
type: model
description: Alibaba Qwen 시리즈의 경량 언어 모델, 명령어 튜닝 버전
tags:
  - 모델
  - LLM
  - 오픈소스
aliases:
  - Qwen2-Instruct
  - qwen2-instruct
---

**Qwen2-Instruct**는 Alibaba의 Qwen2 시리즈 중 명령어 튜닝된 오픈소스 언어 모델입니다. Qwen2는 다양한 크기(0.5B부터 72B)로 제공되며, -Instruct 버전은 대화형 작업·지시 따르기에 최적화되어 있습니다.

Qwen2-Instruct의 특징:
- **경량 옵션**: 0.5B부터 시작하는 작은 크기로 엣지 디바이스 배포 가능
- **다국어 지원**: 중국어·영어·다언어 처리
- **오픈소스**: Hugging Face에 공개, 상용 사용 가능
- **명령어 튜닝**: 질문·지시 따르기에 최적화

[[MinerU2.5]]는 0.5B Qwen2-Instruct를 언어 모델 백본으로 선택하여, 1.2B 전체 파라미터에서 대규모 언어 모델의 의존도를 낮춤으로써 도메인 특화 데이터의 가치를 극대화했습니다. 문서 파싱 작업에서 언어 모델 크기가 성능에 미치는 영향은 제한적이므로, 경량 Qwen2-Instruct가 효율적 선택입니다.
