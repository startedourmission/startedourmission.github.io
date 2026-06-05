---
date: 2026-05-15
tags:
  - 정보
  - LLM
  - 오픈소스
description: |-
  Cactus Compute : Needle

  - 26M 파라미터, 14MB INT4의 tool-calling 모델
  - Gemini 3.1 Flash Lite에서 distill된 결과를 FFN 없는 SAN 구조로 압축
  - 폰·스마트워치 같은 작은 기기에서 6000 tok/s prefill, 1200 tok/s decode

  가중치, 학습 파이프라인, 로컬 fine-tune 플레이그라운드까지 모두 MIT 라이선스로 공개됐습니다.
---
[Cactus Compute](https://cactuscompute.com)가 2026년 5월 13일 [Needle](https://github.com/cactus-compute/needle)을 공개했습니다. 한 줄 요약: 26M 파라미터, 14MB INT4 풋프린트로 폰이나 시계 같은 기기에서 [[Gemini]] 3.1 Flash Lite 수준의 single-shot function calling을 수행하는 모델입니다. 가중치, 학습 파이프라인, 로컬 fine-tune 플레이그라운드 모두 MIT 라이선스로 공개됐습니다.

흥미로운 지점은 어떻게 그 크기로 함수 호출이 되느냐 입니다. 답은 transformer에서 FFN/MLP를 통째로 들어낸 새로운 구조, **Simple Attention Network(SAN)** 입니다. 이 글은 SAN 아이디어와 Needle의 학습, 배포 디테일을 차례로 풀어 봅니다.

## FFN을 빼도 되는 이유

표준 트랜스포머는 어텐션과 FFN 한 쌍을 블록으로 쌓습니다. FFN의 역할은 어텐션이 모은 정보를 비선형 변환하고, 사전학습 시점에 외운 지식을 꺼내는 두 가지로 흔히 설명됩니다. 모델 크기의 대부분(파라미터 수)이 사실 FFN에 있죠.

Cactus의 관찰은 단순합니다.

> "Function calling은 외부 도구 목록에 의존한다. 모델이 무엇을 외워둘 필요가 없다면, FFN이 필요한가?"

함수 호출 작업은 다음 세 단계로 분해됩니다.

1. Match — 쿼리에 맞는 도구 이름 매칭
2. Extract — 인자 값 추출
3. Assemble — JSON 어셈블

이 세 작업은 어텐션 만으로 충분합니다. 도구 이름과 인자 위치를 추적하는 일은 retrieval-and-assembly 패턴이고, 모델이 외운 지식을 꺼낼 필요가 없습니다.

이 가설을 검증한 결과가 SAN입니다. FFN을 모두 제거하고, encoder-decoder 구조로 다음과 같이 짭니다.

- **Encoder** — FFN 없는 어텐션 12개 레이어
- **Decoder** — masked self-attention + cross-attention 조합 8개 레이어
- **Hidden dim** — 512
- **Attention heads** — 8 (그 중 4개가 KV head, GQA 구조)
- **Vocab** — 8,192 BPE
- **Positional** — RoPE
- **공유** — encoder 임베딩과 output projection 가중치 공유

이 구조로 파라미터 수가 26M까지 떨어집니다. 표준 트랜스포머에서 FFN이 차지하던 70~80%가 사라진 결과입니다.

## 학습, 200B 사전학습 + 2B 후학습

학습 레시피도 의외로 짧습니다.

**사전학습**

- 200B 토큰
- 16개 TPU v6e
- 27시간

**후학습 (function calling 특화)**

- 2B 합성 function-calling 토큰
- 45분

[[Gemini]] 3.1 Flash Lite를 teacher로 두고 distillation한 결과입니다. teacher의 function calling 분포를 student가 그대로 학습하는 방식이라, 모든 도메인을 다 외울 필요가 없습니다. 함수 호출 패턴만 학습합니다.

후학습 45분이라는 숫자가 인상적입니다. 자기 도메인의 함수 스키마(예: 본인 회사 API)를 넣고 Mac이나 PC에서 45분이면 본인용 모델로 튜닝 가능하다는 것이 [공개된 fine-tune playground](https://github.com/cactus-compute/needle)의 핵심 메시지입니다.

## 성능, 14MB로 무엇이 가능한가요

INT4 양자화 후 **14MB**. 폰이나 스마트워치 메모리에 그대로 올라갑니다. Cactus 자체 런타임에서 다음 처리량을 보고합니다.

- **Prefill** — 6000 tok/s
- **Decode** — 1200 tok/s

Single-shot function calling 벤치에서 Needle이 다음 모델들을 능가한다고 합니다.

- FunctionGemma-270M (10배 큼)
- Qwen-0.6B (23배 큼)
- Granite-350M (13배 큼)
- LFM-2.5-350M (13배 큼)

비교 대상이 모두 function-calling 특화 소형 모델이라는 점이 핵심입니다. 26M이 270M~600M을 이긴다는 건 작업을 좁힐수록 distillation의 효율이 폭발적으로 커진다는 신호입니다.

## 어디에 쓸 수 있을까요

14MB, 26M이라는 크기는 지금까지 LLM이 못 들어가던 자리를 엽니다.

**스마트워치** — Apple Watch, Galaxy Watch에 RAM이 2GB 정도 있습니다. 시스템과 앱이 쓰고 남은 자투리 메모리로도 충분히 굴러갑니다. "시리야 캘린더에서 다음 회의 옮겨" 같은 자연어를 시계가 직접 도구 호출로 변환할 수 있게 됩니다.

**가전, IoT** — 라즈베리 파이 Zero급에서도 INT4로 돌아가는 크기입니다. 클라우드 왕복 없는 음성 명령 처리에 직접 적용 가능합니다.

**오프라인 모바일 앱** — Apple Intelligence, [[Gemini]] Nano, Phi-3 같은 수십억 파라미터급 on-device LLM 흐름에서 Needle은 수십 메가급으로 또 한 자릿수 내려간 위치입니다. 함수 호출만 필요한 시나리오(예: 오프라인 가계부 앱이 음성을 받아 카테고리 분류)에 직접 적용됩니다.

**자체 도메인 함수 튜닝** — 한국 스타트업이 본인 회사 API 스키마를 45분짜리 fine-tune으로 모델에 넣고, 서버 부담 없이 클라이언트에서 굴리는 시나리오. SaaS 제품의 모든 사용자 기기에 모델을 분산시키는 데 적합한 크기입니다.

## 한계

자랑 일색은 아닙니다. 페이지가 명시적으로 짚는 한계도 있습니다.

- **Single-shot only** — Needle은 한 번에 한 도구 호출만 합니다. "먼저 X를 부르고 결과를 보고 Y를 부른다" 같은 multi-step planning은 안 됩니다. 그런 시나리오에는 더 큰 모델이 필요합니다.
- **외부 지식 부재** — FFN을 들어냈으니 모델이 외부에 도구 목록을 가지고 있어야 합니다. 도구 목록을 시스템 프롬프트로 매번 주입해야 하며, 도구가 자주 바뀌면 컨텍스트 토큰이 큽니다.
- **언어 커버리지** — distillation 학습 데이터의 언어 분포에 종속됩니다. 한국어, 일본어 같은 비영어 함수 호출 정확도는 별도 검증이 필요합니다.

## 정리

- **FFN을 통째로 들어낸 SAN 구조** 가 작업이 외부 지식에 의존할 때 통할 수 있음을 26M, 14MB라는 극단적 크기로 증명한 사례입니다.
- 200B 사전학습 + 2B 후학습 + 45분 fine-tune이라는 학습 비용이 Mac에서 자기 도메인 튜닝까지 내려옵니다. on-device LLM 흐름의 새로운 카테고리입니다.
- 모든 가중치, 학습 파이프라인, 튜닝 도구가 MIT 라이선스로 공개된 점이 가장 큽니다. 한국 스타트업이 본인 API 스키마에 바로 붙여 쓸 수 있는 starter kit이라, 시도해 볼 가치가 분명합니다.

[GitHub](https://github.com/cactus-compute/needle) · [Hugging Face](https://huggingface.co/Cactus-Compute/needle) · [HN 토론](https://news.ycombinator.com/item?id=48111896)
