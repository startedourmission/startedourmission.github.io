---
ready: true
type: ai-model
description: "카카오가 만드는 한국어·영어 이중언어 모델 시리즈. 2.1B부터 155B MoE까지 확장됐고 상당수가 오픈웨이트로 공개됐다"
tags:
  - LLM
  - 오픈소스
aliases:
  - 카나나
---

# Kanana

Kanana는 카카오가 개발하는 한국어·영어 이중언어 언어모델 시리즈입니다. 이름은 카카오의 캐릭터에서 왔고, 기술 보고서에서는 스스로를 compute-efficient bilingual language models로 소개합니다.

## 계보

- **Kanana 1.x** (2025): 2.1B(nano)부터 32.5B까지. 2.1B 모델을 공개해 한국어 모델 연구용 기준선으로 썼습니다. 15.7B-A3B 같은 MoE 변형도 함께 나왔습니다.
- **Kanana-o** (2025): 텍스트·음성·이미지를 하나로 묶은 통합 멀티모달 모델입니다.
- **Kanana 2** (2026): 에이전트 용도를 겨냥해 도구 호출, 복잡한 지시 수행, 추론을 강화했습니다. 아키텍처가 [[MLA]]와 MoE 조합으로 바뀌었고, 30B-A3B 계열이 오픈웨이트로 공개됐습니다.
- **Kanana-2-155B-A17B**: 총 155B·활성 17B의 최상위 MoE 모델입니다. [[Muon]] 옵티마이저와 MuonClip으로 학습 불안정을 억제했고, 10조 토큰 규모 1단계 사전학습을 마쳤습니다.

## 학습 방법론 공개

카카오는 Kanana를 만들며 얻은 학습 레시피를 논문으로 따로 내는 편입니다. 155B 모델의 학습률을 스윕 없이 예측한 방법은 COLM 2026 논문 `Let's Scale Step by Step: Compute-Efficient Hyperparameter Transfer for Large-Scale Mixture-of-Experts`에 정리돼 있습니다.
