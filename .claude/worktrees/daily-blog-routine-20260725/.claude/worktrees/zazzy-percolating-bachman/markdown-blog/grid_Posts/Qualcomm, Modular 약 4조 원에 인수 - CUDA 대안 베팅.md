---
date: 2026-06-26
tags:
  - 정보
  - 반도체
  - 오픈소스
description: "Qualcomm이 Chris Lattner의 Modular를 약 39억 달러에 인수했습니다. 핵심 자산은 CUDA 없이 NVIDIA, AMD, Apple Silicon 어떤 하드웨어에서도 동일 코드로 AI 추론을 실행하는 MAX 런타임입니다."
image: "![[qualcomm-modular-acquisition.png]]"
---

> 이 글은 [Bloomberg](https://www.bloomberg.com)·[CNBC](https://www.cnbc.com) 2026-06-24 보도를 참고하여 작성했습니다.

Qualcomm이 2026년 6월 24일 Investor Day에서 Modular를 약 39억 달러 규모의 전량 주식 교환 방식으로 인수한다고 발표했습니다. 거래 완료는 2026년 하반기 예정입니다.

딜의 핵심은 [[Chris Lattner]]가 2022년 창업한 MAX 런타임입니다. MAX는 CUDA도, ROCm도, PyTorch도 없이 [[NVIDIA]], AMD, Apple Silicon에서 동일한 코드로 AI 추론을 실행합니다. Qualcomm이 단순히 스타트업을 삼킨 게 아니라, NVIDIA의 소프트웨어 해자를 정조준하는 수직 통합 스택을 확보한 것입니다.

## CUDA 해자

NVIDIA가 AI 칩 시장을 지배하는 건 하드웨어 성능 때문만이 아닙니다. CUDA 에코시스템 때문입니다. 개발자가 CUDA로 작성한 코드는 NVIDIA GPU에서만 돌고, 수십만 개의 모델, 프레임워크, 연구 코드가 CUDA에 묶여 있습니다. 이 고착 효과(lock-in)가 경쟁사 칩이 기술적으로 따라잡아도 시장을 뚫기 어렵게 합니다.

AMD는 ROCm, Intel은 oneAPI를 만들어 이 해자를 공략해왔습니다. 두 접근 모두 "CUDA 코드를 우리 칩에서도 돌게 하자"는 번역 전략입니다. MAX는 방향이 다릅니다. CUDA를 번역하는 게 아니라, 처음부터 어떤 칩에도 종속되지 않는 새 실행 레이어를 만드는 것입니다.

## MAX 런타임

MAX의 기반은 [[Chris Lattner]]가 만든 두 가지 컴파일러 기반시설입니다.

하나는 MLIR(Multi-Level Intermediate Representation)입니다. Google에서 Lattner가 설계한 컴파일러 인프라로, 하나의 중간 표현(IR)에서 다양한 하드웨어 백엔드로 코드를 내릴 수 있습니다. TensorFlow XLA, IREE, OpenXLA가 MLIR을 씁니다.

다른 하나는 Mojo입니다. Python 문법에 Rust 수준의 시스템 프로그래밍 성능을 결합한 AI 특화 언어로, C++ 없이도 커스텀 커널을 짤 수 있습니다. 2026년 컴파일러 오픈소스화가 예정돼 있습니다.

두 기술을 묶으면 다음과 같이 동작합니다. 개발자는 Mojo 또는 Python으로 모델을 작성하고, MAX가 MLIR을 통해 타깃 하드웨어에 맞게 최적화된 바이너리를 생성합니다. NVIDIA GPU면 NVIDIA 백엔드로, Qualcomm Snapdragon이면 HTP(Hexagon Tensor Processor) 백엔드로, Apple Silicon이면 Apple Neural Engine 백엔드로 컴파일됩니다. 개발자는 코드를 한 번만 씁니다.

## Qualcomm의 데이터센터 베팅

Qualcomm은 모바일 AP(Snapdragon) 시장에서 압도적 1위입니다. 문제는 AI 인프라 지출이 데이터센터에 집중되고 있다는 점입니다. 스마트폰 시장은 포화 상태이고, AI 추론 서버 시장은 연평균 30% 이상 성장 중입니다.

Qualcomm은 Snapdragon X Elite(PC용 NPU), Cloud AI 100(데이터센터 추론 카드)으로 서버 시장 진입을 시도해왔습니다. Cloud AI 100은 특정 모델에서 에너지 효율이 [[NVIDIA H100]] 대비 2~3배 높다는 수치를 제시했지만, 소프트웨어 지원 부재가 발목을 잡았습니다. 개발자가 CUDA 코드를 Qualcomm 칩에서 돌리려면 상당한 포팅 작업이 필요했습니다.

MAX가 이 문제를 해결합니다. 개발자는 기존 Python + Hugging Face 코드를 MAX로 감싸면 Qualcomm 칩에서 실행할 수 있게 됩니다. 포팅이 아니라 실행 레이어 교체입니다.

## Chris Lattner라는 신뢰

9억 달러(2023년)에서 16억 달러(2025년)를 거쳐 39억 달러로 2.5배 가치가 뛴 것은 기술 때문만이 아닙니다. [[Chris Lattner]]라는 이름이 가진 신뢰도 때문입니다.

LLVM은 현재 Apple, Google, Meta, NVIDIA를 포함한 거의 모든 대형 테크 기업의 컴파일러 인프라로 쓰입니다. Clang은 macOS와 iOS의 공식 C++ 컴파일러입니다. Swift는 Apple 전체 앱 생태계의 기반 언어입니다. MLIR은 AI 컴파일러 연구의 표준이 됐습니다.

이 네 가지를 단독 또는 주도적으로 만든 사람이 Modular를 창업하고 MAX를 설계했습니다. MAX가 단순한 스타트업 제품이 아니라 컴파일러 기반 위에 세워진 진지한 인프라라는 신호입니다. Apple에서 15년, Google Brain, SiFive, OpenAI를 거쳐 직접 회사를 세운 이력이 "또 다른 AI 추론 프레임워크"를 다르게 보이게 합니다.

## CUDA 대항마 전쟁

현재 CUDA를 대체하려는 시도는 네 갈래입니다.

| 접근 | 솔루션 | 전략 | 상태 |
|------|--------|------|------|
| AMD | ROCm | CUDA 코드 호환 번역 | 성숙, 호환 불완전 |
| Intel | oneAPI | 이기종 컴퓨팅 통합 | 성숙, 시장 침투 더딤 |
| Apple | MLX | Apple Silicon 전용 ML 프레임워크 | 빠른 성장, 폐쇄 생태계 |
| Qualcomm+Modular | MAX | 하드웨어 무관 실행 레이어 | 초기 단계 |

ROCm과 oneAPI는 번역 전략입니다. 호환성 갭이 남아있고, 새 모델이 나올 때마다 업데이트가 필요합니다. MLX는 Apple Silicon에서만 돌아 포지셔닝이 다릅니다.

MAX는 번역이 아닌 "컴파일 시점에 타깃 하드웨어로 최적화"하는 전략입니다. 이론상 어떤 새 칩이 나와도 컴파일러 백엔드만 추가하면 됩니다. 단, 그 백엔드를 누가 만드느냐가 핵심입니다. 오픈소스 기여자 생태계가 충분히 형성되느냐에 달려 있습니다.

Qualcomm이 39억 달러를 쓴 이유가 여기 있습니다. 자체 Cloud AI 100과 MAX를 묶으면 "Qualcomm 칩 + MAX 런타임"이 하나의 수직 통합 패키지로 데이터센터에 제시됩니다. NVIDIA의 GPU+CUDA 번들링 전략을 Qualcomm 방식으로 복사하는 것입니다. NVIDIA가 30년에 걸쳐 쌓은 해자를 컴파일러 기반의 크로스-하드웨어 레이어로 우회하는 것이 이 베팅의 핵심입니다.

---

이 글은 [Bloomberg](https://www.bloomberg.com)·[CNBC](https://www.cnbc.com) 2026-06-24 보도를 참고하여 작성했습니다.
