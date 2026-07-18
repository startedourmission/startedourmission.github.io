---
date: 2026-07-03
tags:
  - 정보
  - 멀티모달
  - 도구
description: "구글이 6월 30일 Nano Banana 2 Lite($0.034/장, 4초)와 Gemini Omni Flash(대화형 영상 편집, $0.10/초)를 동시 공개했습니다. Gemini API와 AI Studio에서 즉시 사용 가능합니다."
image: "![[Google Nano Banana 2 Lite + Gemini Omni Flash — 이미지 4초, 대화형 영상 편집-thumb.png]]"
---

> 이 글은 [Google 공식 블로그](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni-flash-nano-banana-2-lite/) 및 [Google Cloud 블로그](https://cloud.google.com/blog/products/ai-machine-learning/nano-banana-2-lite-and-gemini-omni-flash-available/)를 참고하여 작성했습니다.

[[Google]]이 6월 30일 이미지 생성 모델 Nano Banana 2 Lite와 영상 생성 모델 Gemini Omni Flash를 동시에 공개했습니다. 둘은 별개의 모델이지만 출시 맥락이 겹칩니다. 하나는 이미지 생성의 속도·비용 문턱을 낮추고, 다른 하나는 영상 편집 방식을 자연어 기반으로 전환합니다. 두 모델 모두 Google AI Studio, Gemini API, Gemini Enterprise Agent Platform에서 바로 사용할 수 있습니다.

## Nano Banana 2 Lite

API 모델 ID는 `gemini-3.1-flash-lite-image`입니다. 이름에서 알 수 있듯 Gemini 3.1 계열이고, 이전 세대인 `gemini-2.5-flash-image`(Nano Banana 초기 버전)의 후속입니다.

핵심 수치는 두 가지입니다. 텍스트에서 이미지를 생성하는 데 약 4초가 걸리고, 비용은 이미지 한 장당 $0.034입니다. 1,000장을 돌려도 $34입니다. 구글 이미지 생성 라인업 중 가장 빠르고 가장 저렴한 모델로 설계됐습니다.

품질 측면에서는 세 가지를 강조합니다. 프롬프트 충실도, 동일 캐릭터를 여러 장에 걸쳐 일관되게 유지하는 캐릭터 일관성, 이미지 안에 텍스트를 읽을 수 있게 렌더링하는 능력입니다. A/B 테스트용 광고 이미지 수백 장을 짧은 시간 안에 뽑아야 하거나, 소셜 앱처럼 사용자 요청이 폭발적으로 몰리는 환경이 주요 사용처입니다.

구글은 이 모델을 소비자 제품에도 순차 적용할 계획입니다. AI Mode in Search, Gemini 앱, NotebookLM, Google Photos, Google Ads 순서로 롤아웃됩니다.

보안 기능으로는 C2PA 콘텐츠 자격 증명과 SynthID 워터마크가 기본 활성화됩니다. SynthID는 사람 눈에 보이지 않지만 Gemini 앱, Chrome, Search에서 AI 생성 여부를 검증할 수 있는 구글의 워터마킹 기술입니다.

## Gemini Omni Flash

API 모델 ID는 `gemini-omni-flash-preview`입니다. 현재 공개 프리뷰 단계입니다.

Nano Banana 2 Lite가 이미지 전용인 것과 달리, Gemini Omni Flash는 영상 생성과 편집 양쪽을 처리합니다. 한 번 요청으로 최대 10초 분량의 영상을 생성할 수 있습니다. 입력은 텍스트, 이미지, 짧은 영상 세 가지를 조합해서 넣을 수 있고, 출력 영상에는 별도 작업 없이 오디오가 자동으로 생성됩니다.

가격은 영상 출력 1초당 $0.10입니다. 10초 클립 하나에 $1.00입니다.

## 대화형 편집

Gemini Omni Flash에서 구글이 강조하는 기능은 대화형 편집(conversational editing)입니다. 기존 영상 편집 방식과의 차이가 분명합니다.

전통적인 타임라인 편집 도구에서 특정 클립의 배경을 바꾸려면 마스킹, 레이어 분리, 색상 키잉, 합성 순서가 필요합니다. Gemini Omni Flash에서는 "이 씬의 조명을 저녁 노을로 바꿔줘"라고 입력하면 됩니다. 모델이 원본 오디오 트랙과 영상 트랙을 유지한 채 지시한 변경만 적용합니다.

지원되는 편집 유형은 다음과 같습니다.

| 유형 | 예시 |
|------|------|
| 캐릭터 교체 | "주인공을 고양이로 바꿔줘" |
| 조명 변경 | "씬을 야외 자연광으로 리라이팅해줘" |
| 앵글 변경 | "카메라를 측면에서 보는 시점으로 전환해줘" |
| 텍스트 오버레이 | "화면 오른쪽 아래에 제품명 텍스트를 넣어줘" |
| 스타일 변환 | "전체 영상을 애니메이션 스타일로 바꿔줘" |

텍스트와 그래픽을 영상 동작과 동기화하는 기능도 있습니다. 화면 속 움직임에 맞춰 설명 텍스트나 키네틱 타이포그래피를 자동으로 배치합니다. 이 기능은 제품 설명 영상이나 교육용 콘텐츠 제작에서 반복적으로 사람이 하던 작업을 자동화합니다.

한계도 있습니다. 오디오 레퍼런스 입력과 씬 연장은 아직 API에서 지원되지 않습니다. 3초 이상의 영상 레퍼런스는 입력을 받지만 현재 정상 처리가 되지 않습니다. 씬 전환 시 캐릭터 일관성 유지가 불완전한 경우도 있습니다. 공개 프리뷰 단계의 한계입니다.

## 경쟁 구도

영상 생성 API 시장에서 현재 주요 플레이어는 OpenAI(Sora), Runway, [[Kling Team|Kling]]입니다. 가격 구조를 직접 비교하면 다음과 같습니다.

| 모델 | 가격 |
|------|------|
| Gemini Omni Flash | $0.10/초 |
| Runway Gen-3 Alpha | 약 $0.10~0.15/초 |
| Sora | 구독 기반, API 공개 제한적 |
| Kling | 크레딧 기반, 초당 환산 시 $0.07~0.10 수준 |

가격만 보면 큰 우위는 없습니다. 구글의 포지셔닝은 가격보다는 생태계 연동에 있습니다. Gemini API를 이미 쓰는 개발자라면 같은 인증과 인프라로 영상 생성을 추가할 수 있습니다. Gemini Enterprise Agent Platform과의 연동, Google Cloud의 기업 규모 처리량(Provisioned Throughput) 지원도 이 방향의 연장입니다.

Nano Banana 2 Lite 쪽은 이미지 생성 API 시장에서 $0.034/장이 상당히 공격적인 가격입니다. 다른 주요 모델들이 $0.04~0.08/장 수준임을 고려하면, 속도(4초)와 비용을 동시에 낮춰 대량 워크플로우 시장을 겨냥하고 있습니다.

## 앞으로 추가될 기능

구글이 Gemini Omni Flash의 로드맵으로 공개한 항목입니다.

- 오디오 레퍼런스 지원
- 영상 레퍼런스 정상 처리
- 라스트 프레임(Last frame) 지원 — 영상 끝 장면을 지정해 연속성 있는 클립 생성
- 씬 연장(Scene extension)
- 더 높은 해상도 출력

Nano Banana 2 Lite는 GA 단계이므로 별도 로드맵 공개는 없고, 기업 대상 Provisioned Throughput은 현재 사용 가능합니다.

---

이 두 모델의 동시 출시는 이미지와 영상 생성을 같은 API 생태계 안에서 처리하겠다는 방향을 보여줍니다. [[Gemini]] API 하나로 텍스트, 이미지, 영상 생성을 모두 커버하는 구도가 되면, 개발자 입장에서 공급처를 분산할 이유가 줄어듭니다. 실제 서비스 품질이 로드맵대로 채워지는지가 앞으로 판단 기준이 됩니다.

이 글은 [Google 공식 블로그](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni-flash-nano-banana-2-lite/)의 관점에서 작성되었습니다.
