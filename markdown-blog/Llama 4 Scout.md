---
date: 2026-04-11
tags:
  - 정보
  - LLM
  - 오픈소스
description: "Meta의 Llama 4 Scout — 17B 파라미터 오픈소스 멀티모달 MoE 모델. 단일 H100 GPU에서 10M 토큰 컨텍스트, Gemma 3와 Gemini Flash를 능가하는 성능."
---

# Meta Llama 4 Scout: 오픈소스 AI의 새로운 기준점

2025년 4월, Meta가 Llama 4 패밀리를 세상에 내놓았습니다. 그중에서도 가장 주목받는 모델이 바로 **Llama 4 Scout**입니다. "단일 GPU 하나에 올릴 수 있는 모델이 과연 얼마나 강력할 수 있을까?"라는 질문에 대해, Meta는 상당히 설득력 있는 답을 내놓았습니다. 17B 활성 파라미터, 16개의 전문가 네트워크, 그리고 업계 최장인 1,000만 토큰 컨텍스트 윈도우. 숫자만 놓고 보면 믿기 어려운 조합이지만, 실제 벤치마크 결과가 이를 뒷받침하고 있습니다.

이 글에서는 Llama 4 Scout의 아키텍처부터 실제 성능, 배포 전략, 그리고 Llama 4 패밀리 전체의 로드맵까지 꼼꼼히 살펴보겠습니다.

## Mixture-of-Experts: Llama 시리즈 최초의 MoE 아키텍처

Llama 4 Scout를 이해하려면 먼저 MoE(Mixture-of-Experts) 아키텍처를 알아야 합니다. 기존 Llama 3까지는 모든 파라미터가 매번 추론에 참여하는 밀집(dense) 구조였습니다. Llama 4 Scout는 이 전통을 깨고 **Llama 시리즈 최초로 MoE 구조를 채택**했습니다.

전체 파라미터 수는 약 **109B(1,090억)**에 달하지만, 토큰 하나를 처리할 때 실제로 활성화되는 파라미터는 **17B(170억)**에 불과합니다. 나머지 파라미터는 16개의 전문가 네트워크에 분산되어 있으며, 정교한 라우팅 메커니즘이 각 토큰을 가장 적합한 전문가에게 배분합니다.

이 설계의 핵심 이점은 명확합니다. 모델의 총 지식 용량은 109B급으로 유지하면서도, 실제 연산량은 17B급에 머무른다는 것입니다. 쉽게 비유하자면, 16명의 전문가로 구성된 팀이 있는데 매번 모든 전문가가 회의에 참석하는 대신, 안건에 맞는 전문가만 불러 빠르게 의사결정을 내리는 방식이라고 할 수 있습니다.

## 10M 토큰 컨텍스트 윈도우: 업계의 새로운 기준

Llama 4 Scout의 가장 인상적인 스펙은 단연 **1,000만(10M) 토큰 컨텍스트 윈도우**입니다. 직전 세대인 Llama 3의 컨텍스트 윈도우가 128K 토큰이었으니, 무려 **78배 이상** 확장된 셈입니다. 이는 발표 시점 기준으로 업계 최장 수준이었습니다.

1,000만 토큰이라는 숫자가 실제로 어느 정도인지 감을 잡아보겠습니다.

- **텍스트 기준**: 수천 페이지 분량의 문서를 한 번에 처리할 수 있습니다. 대규모 코드베이스 전체를 컨텍스트에 올려놓고 분석하는 것도 가능합니다.
- **비디오 기준**: 네이티브 멀티모달을 지원하므로, 약 **20시간 이상의 영상**을 컨텍스트에 담을 수 있습니다.
- **실무 활용**: 다수의 문서를 동시에 요약하거나, 방대한 사용자 활동 로그를 파싱해 개인화된 작업을 수행하거나, 대규모 코드베이스 전반에 걸친 추론을 수행하는 등의 시나리오가 열립니다.

물론 실제 운용 환경에서 10M 토큰 전체를 활용하려면 상당한 메모리와 인프라가 필요합니다. 하지만 이 정도 스케일의 컨텍스트 윈도우가 오픈소스 모델에서 제공된다는 사실 자체가 의미심장합니다.

## 네이티브 멀티모달: 텍스트, 이미지, 비디오를 하나의 백본으로

Llama 4 Scout는 단순한 텍스트 모델이 아닙니다. **네이티브 멀티모달(natively multimodal)** 모델로서, 텍스트, 이미지, 비디오 입력을 모두 처리할 수 있습니다. 여기서 "네이티브"라는 단어가 중요합니다.

기존의 많은 멀티모달 모델은 텍스트 처리용 트랜스포머와 시각 처리용 인코더를 별도로 두고, 이를 후처리 단계에서 결합하는 방식을 사용했습니다. 반면 Llama 4 Scout는 **얼리 퓨전(early fusion)** 메커니즘을 채택해, 시각 토큰과 언어 토큰을 **단일 트랜스포머 백본** 안에서 통합 처리합니다. 별도의 모달리티 전용 인코더를 두지 않는 것입니다.

이 설계 덕분에 텍스트와 이미지가 인터리브(interleaved)된 입력 시퀀스도 자연스럽게 처리할 수 있습니다. 예를 들어, 문서 중간중간에 삽입된 차트나 다이어그램을 텍스트 맥락과 함께 이해하는 식의 작업이 가능합니다.

다국어 지원도 충실합니다. 영어를 포함해 아랍어, 프랑스어, 독일어, 힌디어, 인도네시아어, 이탈리아어, 포르투갈어, 스페인어, 타갈로그어, 태국어, 베트남어 등 12개 언어를 공식 지원합니다.

## 벤치마크 성능: Gemma 3, Gemini Flash, Mistral을 넘어서다

모델의 가치는 결국 성능으로 증명됩니다. Meta에 따르면, Llama 4 Scout는 **Gemma 3 27B, Gemini 2.0 Flash-Lite, Mistral 3.1**을 폭넓은 벤치마크에서 능가합니다.

특히 두드러지는 영역은 다음과 같습니다.

- **추론(Reasoning)**: MoE 아키텍처의 전문가 라우팅이 복잡한 추론 과제에서 빛을 발합니다. 여러 비교 분석에서 Scout는 추론 카테고리에서 일관되게 높은 점수를 기록했습니다.
- **컨텍스트 활용**: 10M 토큰 컨텍스트 윈도우는 단순한 스펙 수치가 아니라 실제 긴 문서 처리 과제에서 우위를 점하는 데 기여합니다.
- **멀티모달 이해**: 이미지와 텍스트를 결합한 과제에서도 경쟁 모델 대비 강력한 성능을 보여줍니다.
- **응답 속도**: 벤치마크 비교에서 Llama 4 Scout는 약 0.33초의 응답 시간을 기록해, Gemini 2.0 Flash(0.34초)와 대등한 수준의 레이턴시를 달성했습니다.

다만, 이후 Google이 [[Gemma 4]]를 출시하면서 추론, 수학, 코딩, 비전 영역에서 격차를 좁혔다는 점도 언급해둘 필요가 있습니다. AI 모델 경쟁은 그만큼 치열하고 빠르게 움직이고 있습니다.

## 단일 H100 GPU 배포와 NVIDIA 가속 생태계

Llama 4 Scout의 실용적 매력 중 하나는 **단일 [[NVIDIA H100]] GPU에서 구동 가능**하다는 점입니다. BF16 가중치로 릴리스되었으며, **on-the-fly Int4 양자화**를 적용하면 [[NVIDIA H100|H100]] 한 장의 메모리에 적재할 수 있습니다.

NVIDIA는 Llama 4 Scout와 Maverick에 대한 추론 가속을 적극 지원하고 있습니다. 주요 내용을 정리하면 다음과 같습니다.

- **TensorRT-LLM 최적화**: Llama 4 모델은 NVIDIA TensorRT-LLM에 최적화되어 높은 처리량을 달성합니다.
- **[[NVIDIA [[NVIDIA B200|B200]]|Blackwell]] B200 GPU**: 최신 Blackwell B200에서는 초당 40,000 토큰 이상의 처리 속도를 기록합니다.
- **NVFP4 양자화**: Blackwell 아키텍처에서는 NVFP4 양자화를 통해 추가적인 메모리 절약과 처리량 향상이 가능합니다. NVIDIA는 `Llama-4-Scout-17B-16E-Instruct-NVFP4`라는 이름으로 Hugging Face에 양자화 모델을 공개하기도 했습니다.
- **NIM 마이크로서비스**: Llama 4 모델은 NVIDIA NIM 마이크로서비스로 패키징되어, GPU 가속 인프라 어디에서든 간편하게 배포할 수 있습니다. 클라우드, 데이터센터, 엣지 환경 간의 원활한 스케일링을 지원합니다.

엣지 디바이스 배포와 관련해서는 한 가지 현실적인 고려가 필요합니다. MoE 모델은 매번 활성화되는 파라미터만 연산에 사용하지만, 전체 전문가 파라미터(109B)는 메모리에 상주해야 합니다. 따라서 데이터센터 환경에서는 매우 효율적이지만, 리소스가 제한된 엣지 디바이스에서의 배포는 여전히 기술적 도전 과제로 남아 있습니다. 다만 양자화 기술의 발전과 NVIDIA NIM 같은 배포 프레임워크의 성숙에 따라 점차 진입 장벽이 낮아질 것으로 예상됩니다.

## Llama 4 패밀리 전체 그림: Maverick와 Behemoth

Llama 4 Scout는 단독 모델이 아니라 **Llama 4 패밀리**의 일원입니다. 전체 라인업을 이해하면 Scout의 포지셔닝이 더 명확해집니다.

### Llama 4 Maverick

Maverick는 Scout의 상위 모델입니다. **17B 활성 파라미터에 128개의 전문가**, 총 파라미터 수 약 **400B**으로 Scout보다 훨씬 큰 규모입니다. 컨텍스트 윈도우는 100만(1M) 토큰으로, Scout의 10M에는 미치지 못하지만 여전히 상당한 수준입니다. 이미지와 텍스트 이해에서 업계 최고 수준의 성능을 제공하며, 역시 단일 H100 호스트에서 구동 가능합니다.

### Llama 4 Behemoth

패밀리의 최상위 모델인 Behemoth는 말 그대로 "거대한 존재"입니다. **288B 활성 파라미터에 16개의 전문가**, 총 파라미터 수 **약 2조(2T)**에 달합니다. GPT-4.5, Claude Sonnet 3.7, Gemini 2.0 Pro를 여러 STEM 벤치마크에서 능가하는 성능을 보여주었습니다.

Behemoth는 발표 시점에 아직 학습이 진행 중인 상태로, **프리뷰 형태**로 공개되었습니다. 흥미로운 점은 Behemoth가 **교사 모델(teacher model)**로도 활용된다는 것입니다. Scout와 Maverick의 학습 과정에서 Behemoth가 생성한 데이터를 활용해 성능을 끌어올리는 [[Distilling the Knowledge in a Neural Network|지식 증류]](knowledge distillation) 전략이 적용되었습니다. Meta는 FP8 정밀도와 32,000개의 GPU를 사용해 Behemoth를 학습시켰으며, GPU당 390 TFLOPs의 효율을 달성했다고 밝혔습니다.

세 모델의 학습 데이터는 공통적으로 **30조 토큰 이상의 멀티모달 데이터**로 구성되어 있으며, 이는 Llama 3 학습 데이터의 두 배 이상입니다. 텍스트, 이미지, 비디오 데이터가 다양하게 포함되었고, 학습 데이터 컷오프는 2024년 8월입니다.

## 오픈 웨이트: 누구나 접근 가능한 최전선 AI

Llama 4 Scout가 주는 가장 큰 의미 중 하나는 이것이 **오픈 웨이트(open-weight)** 모델이라는 사실입니다. 모델 가중치는 다음 경로에서 누구나 다운로드할 수 있습니다.

- **llama.com**: Meta 공식 사이트
- **Hugging Face**: `meta-llama/Llama-4-Scout-17B-16E` 및 `meta-llama/Llama-4-Scout-17B-16E-Instruct`
- **GitHub Models**: Azure ML을 통한 배포 지원
- **NVIDIA NIM**: 즉시 배포 가능한 마이크로서비스 형태
- **주요 클라우드 플랫폼**: Oracle Cloud, Cloudflare Workers AI 등 다수의 플랫폼에서 즉시 사용 가능

오픈 웨이트 모델은 연구자와 개발자에게 투명성을 제공합니다. 모델의 동작을 검증하고, 특정 도메인에 맞게 파인튜닝하고, 자체 인프라에서 독립적으로 운용할 수 있습니다. 이는 API 호출에만 의존하는 폐쇄형 모델에서는 불가능한 자유도입니다.

Meta가 이 수준의 모델을 오픈 웨이트로 공개한다는 것은, 오픈소스 AI 생태계 전체에 강력한 신호를 보내는 것이기도 합니다. GPT-4급 성능을 단일 GPU에서 구동할 수 있는 오픈 모델이 존재한다는 사실은, AI 접근성의 민주화라는 관점에서 의미가 큽니다.

---

Llama 4 Scout는 MoE 아키텍처, 네이티브 멀티모달, 10M 토큰 컨텍스트 윈도우, 단일 GPU 배포라는 네 가지 축을 하나의 오픈 웨이트 모델에 집약시켰습니다. 물론 AI 모델 경쟁은 멈추지 않습니다. Gemma 4가 등장했고, 다른 경쟁자들도 빠르게 움직이고 있습니다. 하지만 Llama 4 Scout가 "오픈소스 모델도 이 정도는 된다"는 새로운 기준선을 만들었다는 점은 분명합니다. 앞으로 Behemoth의 완전한 공개와 함께 Llama 4 패밀리가 어떤 파급력을 보여줄지 지켜볼 만합니다.

Sources:
- [Meta AI Blog - The Llama 4 herd](https://ai.meta.com/blog/llama-4-multimodal-intelligence/)
- [Llama 4 Official - llama.com](https://www.llama.com/models/llama-4/)
- [Hugging Face - Llama 4 Scout](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E)
- [NVIDIA Technical Blog - Llama 4 Acceleration](https://developer.nvidia.com/blog/nvidia-accelerates-inference-on-meta-llama-4-scout-and-maverick/)
- [PromptLayer - Llama 4 Scout Overview](https://blog.promptlayer.com/llama-4-scout-17b-16e-instruct-open-source-powerhouse-with-moe-multimodality-10m-token-memory/)
- [NVIDIA NIM - Llama 4 Scout Model Card](https://build.nvidia.com/meta/llama-4-scout-17b-16e-instruct/modelcard)
- [Embedl - Llama 4 on the Edge](https://www.embedl.com/knowledge/llama-4-on-the-edge-overcoming-limitations-of-deploying-mixture-of-experts-on-edge-devices)
