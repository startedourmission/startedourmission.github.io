---
date: 2026-04-03
tags:
  - 정보
  - LLM
  - 구글
  - Headliner
aliases:
image: "![[image.png]]"
description: Google DeepMind이 Gemma 4를 공개했습니다. Gemini 3의 연구와 기술을 기반으로 만든 오픈 모델 패밀리이며, 이번엔 Apache 2.0 라이선스입니다. E2B, E4B, 26B MoE, 31B Dense 네 가지 사이즈로 나왔고, 31B 모델은 Arena AI 텍스트 리더보드에서 오픈 모델 3위, 26B MoE는 6위를 기록했습니다. 자기보다 20배 큰 모델을 이기는 파라미터 대비 지능(intelligence-per-parameter) 효율을 강조하고 있습니다. Gemma 시리즈 출시 이후 누적 다운로드 4억 회, 커뮤니티 변형 모델 10만 개라는 숫자도 인상적입니다.
---
![[image.png]]
Google DeepMind이 Gemma 4를 공개했습니다. Gemini 3의 연구와 기술을 기반으로 만든 오픈 모델 패밀리이며, 이번엔 Apache 2.0 라이선스입니다. E2B, E4B, 26B MoE, 31B Dense 네 가지 사이즈로 나왔고, 31B 모델은 Arena AI 텍스트 리더보드에서 오픈 모델 3위, 26B MoE는 6위를 기록했습니다. 자기보다 20배 큰 모델을 이기는 파라미터 대비 지능(intelligence-per-parameter) 효율을 강조하고 있습니다. Gemma 시리즈 출시 이후 누적 다운로드 4억 회, 커뮤니티 변형 모델 10만 개라는 숫자도 인상적입니다.

Gemma 4는 네 가지 사이즈로 나뉩니다.

- **E2B / E4B**: "Effective" 파라미터 2B/4B. 모바일, IoT, 엣지 디바이스용. 오디오, 이미지, 비디오를 모두 처리하는 멀티모달 모델이며, 컨텍스트 윈도우 128K 토큰. Per-Layer Embeddings(PLE)로 파라미터 효율을 극대화했습니다. 완전 오프라인에서 거의 제로 레이턴시로 동작한다는 게 핵심입니다.
- **26B A4B (MoE)**: 총 26B 파라미터 중 추론 시 3.8B만 활성화. "A4B"의 A는 Active Parameters. 4B급 모델의 속도로 26B급 품질을 낸다는 포지셔닝. 컨텍스트 윈도우 256K 토큰.
- **31B Dense**: 순수 Dense 아키텍처 31B. 최고 품질을 추구하며, 파인튜닝 기반 모델로도 적합. bfloat16 기준 [[NVIDIA H100]] 한 장에 올라갑니다. 컨텍스트 윈도우 256K 토큰.

## 아키텍처 특징

Gemma 4의 아키텍처는 이전 버전들과 다른 오픈 모델에서 검증된 컴포넌트를 조합했습니다. 복잡하거나 결론이 불분명한 기법(예: Altup)은 제외하고, 라이브러리 호환성과 디바이스 범용성을 우선시한 설계입니다.

**주요 특징:**

- **하이브리드 어텐션**: 로컬 슬라이딩 윈도우 어텐션과 글로벌 풀 컨텍스트 어텐션을 번갈아 배치. 마지막 레이어는 항상 글로벌. 가벼운 모델의 속도와 긴 컨텍스트에 대한 깊은 이해를 동시에 달성하려는 설계입니다.
- **Unified Keys and Values**: 글로벌 레이어에서 KV를 통합해 긴 컨텍스트의 메모리 사용을 최적화.
- **Proportional [[RoPE]] (p-RoPE)**: 긴 컨텍스트 처리를 위한 위치 인코딩 최적화.
- **네이티브 시스템 프롬프트**: Gemma 4부터 system role을 네이티브로 지원합니다. 이전 Gemma 모델에서는 아쉬웠던 부분이죠.
- **Thinking 모드**: 내장된 추론 모드로 step-by-step 사고가 가능. `<|think|>` 토큰으로 활성화합니다.
- **140+ 언어 지원**: 단순 번역이 아닌 문화적 맥락까지 이해하는 멀티링구얼.

## 성능

Arena AI 텍스트 리더보드 기준:

- **31B Dense**: 추정 LMArena 점수 1452, 오픈 모델 3위
- **26B MoE**: 추정 LMArena 점수 1441 (4B 활성 파라미터만으로), 오픈 모델 6위

Hugging Face 블로그에 따르면, 이 수치는 자기보다 20배 큰 모델을 능가하는 결과입니다. 텍스트뿐 아니라 비전, 오디오에서도 비교적 좋은 성능을 보인다고 합니다.

한편, Trending Topics의 분석에서는 중국 경쟁 모델들(Qwen, DeepSeek 등) 대비 여전히 뒤처진다는 지적도 있습니다. 이 부분은 아직 벤치마크 세부 비교가 필요해 보입니다.

## 아키텍처 + TurboQuant

Gemma 4가 "소비자 하드웨어에서 프론티어급 AI"를 가능하게 하는 건 단순히 모델 크기가 작아서가 아닙니다. 아키텍처 레벨에서 KV 캐시를 줄이는 최적화가 여러 겹으로 쌓여 있고, 여기에 TurboQuant까지 결합되면서 메모리 사용량이 극적으로 줄어듭니다.

### 1단계: 아키텍처 자체의 KV 캐시 최적화

**Shared KV Cache** — Gemma 4에서 가장 주목할 만한 효율화 기법입니다. 마지막 N개 레이어가 자체 Key/Value 프로젝션을 계산하지 않고, 앞선 레이어의 KV 텐서를 재사용합니다. E2B 모델의 경우 35개 레이어 중 20개가 KV를 공유합니다. 실제 KV 캐시를 생성하는 레이어는 15개뿐입니다. KV를 공유하는 레이어는 대신 MLP를 2배 넓게(hidden=12,288 vs 6,144) 해서 표현력을 보상합니다.

**하이브리드 어텐션의 이중 구조** — Gemma 3에서 시작된 슬라이딩 윈도우/글로벌 어텐션 인터리빙이 Gemma 4에서 한 단계 진화했습니다. 두 어텐션 타입이 구조적으로 다릅니다:

- 슬라이딩 윈도우 레이어: `head_dim=256`, KV 헤드 많음 → 세밀한 로컬 어텐션
- 글로벌 어텐션 레이어: `head_dim=512`, KV 헤드 적음 → 강력한 장거리 어텐션

글로벌 레이어에서는 V 프로젝션을 아예 제거하고(K=V weight sharing) Key 값을 Value로도 씁니다. 이게 어텐션 출력을 안정화시키면서 메모리를 절반으로 줄입니다.

**Per-Layer Embeddings (PLE)** — E2B/E4B 모델에서 사용. 총 파라미터는 5B/8B이지만, 레이어별 임베딩 테이블은 CPU에서 처리하고 실제 가속기(GPU) 메모리에는 코어 트랜스포머 가중치(~2B/~4B)만 올립니다. 결과적으로 E2B는 약 2GB, E4B는 약 3GB의 가속기 메모리로 동작합니다.

**구체적 수치:**

- 26B MoE: KV 캐시가 31B Dense의 1/4 수준. INT4 + 128K 컨텍스트에서 A6000 한 장에 올라감 (31B에서는 불가능)
- E2B: KV 공유 덕분에 128K 컨텍스트를 노트북 GPU에서 처리 가능

### 2단계: TurboQuant로 KV 캐시 추가 압축

여기에 TurboQuant를 적용하면 KV 캐시가 한 번 더 4~6배 줄어듭니다. 이미 아키텍처 레벨에서 최적화된 KV 캐시를 3.5비트로 양자화하는 거라, 효과가 곱해집니다.

**MLX에서 바로 사용 가능합니다:**

```bash
mlx_vlm.generate \
  --model "mlx-community/gemma-4-26B-A4B-it" \
  --prompt "Your prompt here" \
  --kv-bits 3.5 \
  --kv-quant-scheme turboquant
```

Hugging Face 블로그에 따르면, 이 조합으로 비압축 베이스라인과 동일한 정확도를 유지하면서 활성 메모리를 약 4배 줄이고, 전체적인 속도도 빨라집니다. Apple Silicon에서 긴 컨텍스트 추론이 실용적이 됩니다.

**llama.cpp에서도 통합이 진행 중입니다.** PR #21089에서 TurboQuant KV 캐시 타입(tbq3_0, tbq4_0)이 ggml 타입 시스템에 추가되는 작업이 진행 중입니다. CPU 구현은 이미 18/18 테스트를 통과했고, CUDA 커널도 작성 완료 상태입니다. Gemma를 포함한 5개 아키텍처에서 자동 head_dim 매핑이 동작합니다.

### 실질적 영향: 무엇이 달라지나

이 조합의 실질적 의미를 정리하면:

- **8B 모델 + 32K 컨텍스트**: 기존에 KV 캐시만 ~4.6GB 차지 → TurboQuant 적용 시 ~1GB 이하로. 16GB GPU에서 OOM 나던 16K+ 컨텍스트가 가능해짐
- **Gemma 4 26B MoE**: 이미 KV 캐시가 31B의 1/4인데, TurboQuant까지 적용하면 128K 컨텍스트를 소비자 GPU(RTX 4090 수준)에서 실제로 쓸 수 있는 영역에 들어옴
- **E2B on Edge**: 2GB 가속기 메모리 + KV 공유 + TurboQuant면, 라즈베리 파이나 Jetson Nano에서 의미 있는 컨텍스트 길이로 에이전트 작업이 가능

한 분석가가 이런 표현을 썼습니다. "48GB GPU가 필요하던 모델이 8GB VRAM에서 돌아갈 수 있다." 다소 과장이 섞여 있지만, 방향성은 맞습니다. 모델 가중치 양자화(GPTQ, AWQ)와 KV 캐시 양자화(TurboQuant)는 서로 보완적이라, 둘을 동시에 적용하면 메모리 절감이 곱해집니다.

## 에코시스템과 실행 환경

오픈 모델의 가치는 결국 "얼마나 쉽게 돌릴 수 있는가"에 달려 있습니다. 이 점에서 Gemma 4의 Day 0 지원은 압도적입니다.

- **추론 프레임워크**: Hugging Face Transformers, vLLM, llama.cpp, MLX, Ollama, NVIDIA NIM/NeMo, SGLang, LM Studio, mistral.rs 등 Day 1 지원
- **하드웨어**: NVIDIA RTX GPU, AMD Instinct/Radeon/Ryzen AI, Google AI Edge, Raspberry Pi, Jetson Nano
- **양자화**: Unsloth 기준으로 26B MoE는 4-bit에서 18GB RAM, 31B Dense는 4-bit에서 20GB RAM이면 실행 가능

Android에서는 AICore Developer Preview를 통해 바로 테스트할 수 있고, Gemini Nano 4의 기반이 될 모델이라 향후 안드로이드 생태계와의 통합도 기대됩니다.

## 고찰

**긍정적인 부분:**

- Apache 2.0 라이선스 전환은 의미가 큽니다. 이전 Gemma의 제한적 라이선스가 기업 도입의 걸림돌이었거든요.
- MoE와 Dense를 동시에 제공해서 속도 vs 품질 트레이드오프를 사용자가 선택할 수 있게 한 점도 좋습니다.
- 에코시스템 Day 0 지원의 폭이 넓습니다. AMD, NVIDIA, 모바일까지.

**아쉬운 부분:**

- 기술 보고서(technical report)가 아직 공개되지 않았습니다. Gemini 3의 연구에서 왔다고 하지만, 구체적으로 어떤 학습 데이터를 썼는지, 학습 방법론의 디테일은 알 수 없습니다. 오픈 모델이라면 이 부분의 투명성도 필요합니다.
- Arena AI 리더보드 순위를 강조하고 있지만, 리더보드 점수와 실제 사용 품질 사이의 갭은 늘 존재합니다. 특히 한국어 성능에 대한 벤치마크는 별도로 확인이 필요합니다.
- E2B/E4B의 "에지 디바이스에서 동작" 주장은 실제 배터리 소모, 발열, 지속적 추론 시나리오에서 검증이 필요합니다. 구글은 이전 세대보다 4배 빠르고 배터리 60% 절감이라고 하지만, 독립적인 벤치마크는 아직 없습니다.

Gemma 4는 "파라미터 대비 성능" 경쟁에서 구글의 본격적인 답변으로 보입니다. Apache 2.0 전환, 다양한 사이즈 라인업, 광범위한 에코시스템 지원까지. 오픈 모델 시장에서 Qwen, Llama, Mistral과의 경쟁이 더 치열해질 것 같습니다.

개인적으로 가장 주목하는 건 26B MoE입니다. 4B 활성 파라미터로 26B급 품질을 낸다면, 로컬 에이전트 시나리오에서 매우 실용적인 선택지가 될 수 있습니다. TurboQuant 같은 KV 캐시 최적화 기법과 결합하면, 256K 컨텍스트를 소비자 GPU에서 실제로 활용할 수 있는 시대가 올 수도 있겠네요.

---

**참고 자료:**

- [Google Blog: Gemma 4](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/)
- [Google DeepMind: Gemma 4](https://deepmind.google/models/gemma/gemma-4/)
- [Hugging Face Blog: Welcome Gemma 4](https://huggingface.co/blog/gemma4)
- [Model Card](https://ai.google.dev/gemma/docs/core/model_card_4)
- [Android Developers Blog: Gemma 4 in AICore](https://android-developers.googleblog.com/2026/04/AI-Core-Developer-Preview.html)