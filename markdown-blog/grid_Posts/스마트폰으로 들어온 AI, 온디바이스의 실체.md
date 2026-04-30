---
date: 2026-04-25
tags:
  - 정보
  - LLM
description: 여러분은 시리를 자주 사용하나요? 저는 거의 사용하지 않습니다. 불편하고 멍청합니다. 수 년 동안 그랬습니다. 하지만 이제는 분위기가 조금 달라질 수도 있습니다. Apple Intelligence부터 Phi 계열까지, 모바일에서 실제로 쓸 만한 LLM의 현주소를 알아봅니다.
---

온디바이스 LLM이 가능하다는 건 2~3년 전부터 이야기됐습니다. 하지만 "가능하다"와 "쓸 만하다"는 다릅니다. 모델이 너무 느리거나, 품질이 API에 비해 터무니없이 낮거나, 배터리를 금방 태워버리면 실제로 쓰는 사람은 없습니다. 그 간극이 2025년 들어 좁혀지기 시작했고, 2026년 현재 몇 가지 사용 시나리오에서는 클라우드가 필요 없다는 말이 과장이 아니게 됐습니다. 무엇이 달라졌는지 정리합니다.

## NPU가 진짜로 빨라졌다

온디바이스 추론의 병목은 항상 메모리 대역폭과 연산 능력이었습니다. CPU는 LLM 추론에 너무 느리고, 스마트폰 GPU는 AI 워크로드에 최적화되지 않았습니다. 그래서 NPU(Neural Processing Unit)가 중요합니다.

칩별 NPU 성능(TOPS, Tera Operations Per Second):

| 칩 | 제품 | NPU 성능 |
|---|---|---|
| Apple A17 Pro | iPhone 15 Pro | 35 TOPS |
| Apple A18 Pro | iPhone 16 Pro | ~45 TOPS |
| Apple M5 | MacBook Pro 2025 | Neural Accelerator 4배 향상 |
| Qualcomm Snapdragon 8 Elite | Galaxy S25 | 80 TOPS |
| Qualcomm Snapdragon X Elite | AI PC | 80 TOPS |
| MediaTek Dimensity 9400 | 플래그십 안드로이드 | 35+ TOPS |

Microsoft의 "Copilot+" 인증 기준이 NPU 45~50 TOPS인데, 2025년 출시된 플래그십 기기 대부분이 이 기준을 넘습니다. 숫자만 보면 감이 안 오는데, Qualcomm은 80 TOPS NPU로 **100억 파라미터 규모의 생성형 AI 모델**을 실시간 추론할 수 있다고 발표했습니다.

Apple의 M5와 A19 Pro 칩에 들어간 Neural Accelerator는 이전 세대 대비 AI 연산 성능이 4배 향상됐습니다. 텍스트 요약, Genmoji 생성, Visual Intelligence 같은 Apple Intelligence 기능 대부분이 이제 온디바이스에서 돌아갑니다.

## 소프트웨어 스택이 드디어 성숙했다

하드웨어가 준비됐어도 소프트웨어 스택이 없으면 개발자가 쓸 수 없습니다. 2025년에 이 생태계가 본격적으로 안정화됐습니다.

**[ExecuTorch](https://executorch.ai/)** — Meta가 만든 모바일 AI 추론 런타임. 2025년 10월에 1.0 GA(정식 배포)가 됐습니다. 런타임 자체 크기가 50KB에 불과하고, Apple Silicon, Qualcomm, Arm, MediaTek, Vulkan 등 12개 이상의 하드웨어 백엔드를 지원합니다. Meta는 이미 Instagram, WhatsApp, Messenger, Facebook 전체에 ExecuTorch를 배포해 수십억 사용자에게 서비스하고 있습니다.

**[llama.cpp](https://github.com/ggerganov/llama.cpp)** — CPU와 GPU에서 양자화된 LLM을 실행하는 C++ 라이브러리. 데스크톱과 프로토타이핑에 사실상 표준이 됐습니다.

**CoreML** — Apple Silicon에 최적화된 추론 프레임워크. ExecuTorch와 통합되어 iOS/macOS 앱에서 쓰기 쉬워졌습니다.

**GGUF 포맷** — 양자화된 모델을 배포하는 사실상 표준 포맷. HuggingFace에서 모델을 다운받으면 GGUF 파일로 제공되는 경우가 대부분입니다. llama.cpp, Ollama, LM Studio 모두 GGUF를 읽습니다.

## 양자화가 결정적이었다

모델이 작아야 기기에 들어갑니다. 7B 모델은 FP16 기준 약 14GB인데, 대부분의 스마트폰 RAM이 8~12GB입니다. 여기서 양자화가 핵심입니다.

표준 레시피는 이렇게 수렴했습니다: **16비트로 학습, 4비트로 배포.** GPTQ(2022)와 AWQ(2023) 논문이 4비트 양자화가 모델 품질을 대부분 보존하면서 메모리를 4배 줄인다는 걸 증명했고, 이제 이게 기본값입니다.

실제로 GGUF Q4_K_M 양자화를 적용하면 6GB 모델이 **1.88GB**로 줄어듭니다. 68% 압축입니다. 이 크기라면 스마트폰에서도 올릴 수 있습니다.

양자화 포맷 선택 기준:
- **Q4_K_M** — 대부분의 상황에서 최적. 속도와 품질의 균형이 좋습니다.
- **Q5_K_M** — 품질을 조금 더 높이고 싶을 때. 약간 느립니다.
- **Q8_0** — 원본에 가장 가까운 품질. 크기가 FP16의 절반 수준.

LLM 추론의 병목은 메모리 대역폭입니다. 연산보다 메모리에서 가중치를 읽어오는 속도가 한계를 정합니다. 4비트 양자화는 읽어야 할 데이터를 줄여서 이 병목을 직접 해결합니다. KV 캐시(추론 중 생성되는 중간 값)도 최근 FP8, KV8 포맷으로 압축해 런타임 RAM을 40% 이상 줄이는 기법이 나왔습니다.

## 지금 실용권에 있는 모델들

모두 스마트폰이나 노트북에서 실제로 돌릴 수 있는 모델들입니다.

**Apple Intelligence 온디바이스 모델 (~3B 파라미터)**
Apple이 직접 개발한 모델. A17 Pro 이상에서 동작합니다. Apple의 벤치마크에 따르면 Phi-3-mini, Mistral-7B, Gemma-7B, Llama-3-8B를 성능에서 앞섭니다. 파라미터 수가 적은데 성능이 좋은 이유는 Apple의 독자적인 fine-tuning과 어댑터 구조 덕분입니다. [Apple Machine Learning Research](https://machinelearning.apple.com/research/introducing-apple-foundation-models)에 상세가 공개되어 있습니다.

**Gemini Nano**
Google이 Android에 시스템 레벨로 내장한 LLM. AICore 서비스를 통해 관리되며, 안전 필터링과 NPU 가속 추론을 처리합니다. Pixel 시리즈에서 통화 요약, 메시지 답장 제안 등에 쓰입니다.

**Phi-4 mini (3.8B)**
Microsoft 연구팀이 만든 소형 모델. AIME 2025에서 80.6점, GPQA Diamond에서 75.3점으로 파라미터 수 대비 추론 성능이 뛰어납니다. 모바일과 엣지 배포를 명시적으로 타겟합니다.

**Llama 3.2 1B / 3B**
Meta의 공식 경량 모델. ExecuTorch를 통해 스마트폰에서 직접 돌릴 수 있고, 1B 모델은 서브-10ms 토큰 생성이 현실적입니다.

**Gemma 3n**
Google의 on-device 특화 버전. 270M 파라미터 버전도 있어서 메모리가 빡빡한 기기에서도 동작합니다.

**SmolLM2 (135M ~ 1.7B)**
Hugging Face가 만든 초경량 모델군. 135M짜리는 진짜로 마이크로컨트롤러에서도 돌아갑니다.

## 실제로 배포된 사례들

말이 아니라 이미 배포된 것들입니다.

**Apple Intelligence** — iPhone 16 Pro / M 칩 Mac에서 글쓰기 도우미, 사진 편집, Siri 강화가 온디바이스로 동작합니다. 처리 용량을 초과하면 Private Cloud Compute(PCC)로 넘어가는데, PCC는 Apple Silicon 서버 클러스터로 구성되어 사용자 데이터가 저장되거나 Apple에 공유되지 않습니다. 이 아키텍처 자체가 [공개 검증 가능](https://security.apple.com/blog/private-cloud-compute/)한 상태로 공개됐습니다.

**Meta 앱들** — Instagram, WhatsApp, Messenger, Facebook이 이미 ExecuTorch 기반의 온디바이스 모델을 수십억 사용자에게 서비스합니다. 스마트 답장, 콘텐츠 필터링 등이 여기 해당됩니다.

**Adobe Firefly** — NPU 탑재 기기에서 로컬로 생성형 이미지 도구를 실행합니다. 서버 비용을 줄이면서 응답 속도는 빨라졌습니다.

**LG유플러스 익시오** — 엑사원 3.5를 경량화한 온디바이스 sLM. NPU 기반으로 전력 소모 78%, 모델 크기 82% 감소를 달성했습니다.

## 프라이버시가 온디바이스의 진짜 가치다

클라우드 LLM 대비 온디바이스의 가장 큰 차이점은 데이터가 기기를 벗어나지 않는다는 겁니다. 텍스트, 사진, 음성이 API로 전송되지 않습니다. 기업 입장에서는 민감한 데이터를 외부 서버에 올리지 않아도 됩니다. 개인 입장에서는 오프라인에서도 동작하고, 무료입니다 — 모델을 한 번 다운받으면 추론 비용이 없습니다.

Apple의 Private Cloud Compute는 이 철학의 연장입니다. 온디바이스로 처리할 수 없는 작업이 있을 때 클라우드로 넘기되, 그 클라우드 자체가 애플 실리콘 서버이고 감사 가능한 아키텍처로 구성됩니다.

## 아직 한계인 것들

솔직하게 정리합니다.

**7B 이상은 여전히 느립니다.** 1B~3B 모델은 모바일에서 실용적인 속도가 나오지만, 7B를 스마트폰에서 돌리면 토큰 생성 속도가 너무 느려서 체감이 나쁩니다. 노트북 기준으로는 M3 Pro 이상에서 7B Q4가 실용권에 들어옵니다.

**컨텍스트 길이가 짧습니다.** 메모리 제약으로 KV 캐시를 많이 못 씁니다. 긴 문서를 처리하거나 긴 대화를 이어가는 시나리오는 여전히 클라우드가 유리합니다.

**배터리 소모가 있습니다.** NPU를 풀로 돌리면 발열과 배터리 소모가 눈에 띕니다. 짧은 작업에는 괜찮지만 장시간 추론은 부담입니다.

**최신 추론 능력은 격차가 있습니다.** GPT-4o, Claude 3.5 Sonnet급 추론이 필요한 작업에서 3B 모델은 당연히 부족합니다. 온디바이스는 요약, 분류, 간단한 질답에 맞고, 복잡한 추론은 여전히 클라우드를 써야 합니다.

## 실용권 진입이라는 판단의 근거

"진짜 실용권"의 기준을 이렇게 설정했습니다: 일반 사용자가 실제 쓰는 기능에서 클라우드 없이 동작하고, 속도와 품질이 불편하지 않은 수준.

이 기준에서 2025~2026년의 변화는 분명합니다. Apple Intelligence가 수억 명의 iPhone 사용자에게 온디바이스 AI를 기본 기능으로 배포했고, Meta의 ExecuTorch가 GA가 됐고, 3B 이하 모델에서 sub-10ms 토큰 생성이 현실화됐습니다. 개발자 입장에서도 GGUF + llama.cpp로 로컬에서 프로토타이핑하고, 검증이 끝나면 ExecuTorch로 모바일 프로덕션에 넣는 파이프라인이 구체화됐습니다.

클라우드 LLM을 대체하는 게 아닙니다. 온디바이스와 클라우드가 작업의 성격에 따라 나뉘는 시대가 시작됐다는 뜻입니다. 그 분기점이 2025년이었습니다.
