---
date: 2026-04-23
tags:
  - 정보
  - LLM
  - 오픈소스
description: "DeepSeek V4가 4월 말 출시 예정입니다. 1조 파라미터 MoE, 화웨이 Ascend 칩, CUDA 완전 배제. 중국 AI가 엔비디아 없이 프론티어를 달릴 수 있는지 실증하는 첫 사례가 될 것입니다."
---

DeepSeek V4가 4월 말 출시 예정입니다. 로이터가 4월 3일 "향후 몇 주 내"라고 보도한 이후, 4월 21일 기준으로 아직 공식 출시는 없습니다. 하지만 이 모델을 둘러싼 정황은 출시 직전 단계임을 시사합니다. V4-Lite가 이미 API 노드에서 라이브 테스트 중이라는 보고가 있습니다.

수치보다 먼저 봐야 할 맥락이 있습니다. **이 모델은 화웨이 칩으로만 돌아갑니다.**

---

## 화웨이 칩으로 프론티어 모델을 만든다는 것

2023년 미국이 NVIDIA H100을 중국 수출 금지 리스트에 올렸을 때, 업계의 통념은 이랬습니다. "중국이 AI에서 뒤처질 것이다." CUDA 생태계가 없이는 실용적인 프론티어 모델 학습이 불가능하다는 논리였습니다.

DeepSeek V4는 이 전제를 정면으로 테스트합니다.

Reuters에 따르면 V4는 화웨이의 **Ascend 950PR 칩**에서 동작합니다. DeepSeek 팀은 수개월에 걸쳐 Huawei, Cambricon Technologies와 협력해 V4의 핵심 코드를 화웨이의 **CANN 아키텍처**에 맞게 재작성했습니다. NVIDIA CUDA에 의존하는 코드를 완전히 걷어낸 겁니다.

Alibaba, ByteDance, Tencent가 화웨이 차세대 칩을 수십만 개 단위로 선주문한 것도 이 흐름과 무관하지 않습니다.

---

## 알려진 스펙

공식 발표 전이라 모든 수치는 리크와 커뮤니티 분석 기반입니다. 그 점을 전제하고 보면:

| 항목 | 내용 |
|---|---|
| 아키텍처 | Mixture-of-Experts (MoE) |
| 총 파라미터 | ~1조 (1T) |
| 활성 파라미터 (토큰당) | ~370억 (37B) |
| 컨텍스트 | 1M 토큰 (미확인) |
| 멀티모달 | 텍스트, 이미지, 비디오 |
| 입력 가격 | ~$0.30/MTok (리크) |
| 오픈소스 | 예정 |

1조 파라미터이지만 토큰당 37B만 활성화되는 구조입니다. 추론 비용이 모수 규모에 비해 훨씬 낮습니다. 이전 DeepSeek V3도 같은 MoE 전략을 써서 비용 효율로 업계를 놀라게 했습니다.

SWE-bench 점수 81%가 언급되는데, 이건 공식 수치가 아닙니다. GPT-5.4의 SWE-bench Pro 57.7%와 단순 비교하면 안 됩니다. 벤치마크 버전이 다를 수 있습니다.

---

## 왜 이 출시가 중요한가

DeepSeek V3는 NVIDIA H800 칩으로 훈련됐습니다. H800은 H100의 수출 규제 우회 버전입니다. V4는 그마저도 없앤 버전입니다.

만약 V4가 실제로 서방 프론티어 모델과 경쟁할 만한 성능을 화웨이 칩으로 낸다면, "엔비디아 없이는 AI 프론티어 불가능"이라는 전제가 흔들립니다.

이전에 이 블로그에서 엔비디아 독주가 흔들리기 시작했다고 썼습니다. AMD와 커스텀 실리콘이 추론 워크로드를 잠식한다고. DeepSeek V4는 그 맥락에 새로운 데이터 포인트를 추가합니다. 미국 제재를 받은 중국이 자국 칩으로 1T 파라미터 MoE를 돌린다. 이건 기술적 실증이기도 하고, 지정학적 메시지이기도 합니다.

---

## 오픈소스로 공개된다면

DeepSeek 시리즈는 모델 가중치를 공개해왔습니다. V4도 오픈소스 공개가 예정돼 있습니다.

1조 파라미터 오픈소스 모델이 나오면 무슨 일이 생기는지, 그리고 그것이 화웨이 칩에서 학습됐다면 미국 AI 생태계에 어떤 의미인지 — 이 질문들은 V4 출시 이후에 다시 다뤄야 할 것 같습니다.

---

## 지금은 기다리는 중

리크된 수치들은 인상적이지만, 공식 발표 전까지는 보류가 맞습니다. DeepSeek는 과거에도 조용히 출시하고 결과로 말하는 방식을 택했습니다. 이번도 그럴 것 같습니다. 출시되면 다시 뜯어보겠습니다.

---

**참고:**
- [DeepSeek V4 will run on Huawei chips | Reuters via Investing.com](https://www.investing.com/news/stock-market-news/deepseeks-v4-model-will-run-on-huawei-chips-the-information-reports-4597099)
- [DeepSeek V4: 1T Parameters, Open Source, Huawei Chips | Remio](https://www.remio.ai/post/deepseek-v4-is-coming-1-trillion-parameters-open-source-and-running-on-huawei-chips)
- [DeepSeek V4 specs | NxCode](https://www.nxcode.io/resources/news/deepseek-v4-release-specs-benchmarks-2026)
