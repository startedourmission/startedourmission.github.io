---
date: 2026-06-29
tags:
  - 정보
  - LLM
description: "NVIDIA Dynamo: PyTorch 동적 그래프를 정적 연산으로 최적화하는 컴파일러"
image: "![[NVIDIA Dynamo-thumb.png]]"
---

[[NVIDIA]] Dynamo는 [[PyTorch]]의 동적 특성을 보존하면서도 그래프를 정적화해서 성능을 높이는 [[JIT 컴파일러]]입니다. 2023년 공개되었고, PyTorch 2.0의 핵심 구성요소가 되었습니다.

## 문제: 동적 vs 정적 그래프

### 동적 그래프 (Dynamic Graph)

[[PyTorch]]는 "define-by-run" 모델입니다. 코드를 직접 실행하면서 계산 그래프를 구성합니다.

```python
def forward(x, mask):
    if mask > 0:
        x = x * 2
    else:
        x = x + 1
    return x
```

이 코드는 입력 `mask`의 값에 따라 다른 연산을 수행합니다. [[PyTorch]]는 매번 실행할 때마다 이 분기를 평가합니다.

**장점**: 자유도가 높고 디버깅이 쉽습니다. 파이썬의 제어 흐름을 그대로 쓸 수 있습니다.
**단점**: 모든 중간값이 메모리에 구체화되고, [[반복]]이나 [[컨트롤 플로우]]에서 오버헤드가 많습니다.

### 정적 그래프 (Static Graph)

[[TensorFlow]], [[ONNX]] 같은 프레임워크는 먼저 계산 그래프를 완성한 다음 최적화합니다.

```
x → Linear → ReLU → Linear → Output
```

**장점**: 그래프 전체를 보고 최적화할 수 있습니다. [[커널 융합]], 메모리 재할용, 연산 순서 조정 등이 가능합니다.
**단점**: 동적 로직을 표현하기 어렵습니다. 모든 분기를 사전에 선언해야 합니다.

## Dynamo의 접근: 선택적 그래프화(Graph Extraction)

Dynamo는 "양쪽 장점을 취하자"는 전략입니다.

### 핵심 아이디어

1. **Python 코드를 추적(trace)합니다** — 입력을 통과시키면서 어떤 연산이 실행되는지 기록합니다.
2. **연산들을 그래프로 변환합니다** — [[FX]](Function Effects) 또는 [[TorchScript]]를 거쳐 중간 표현(IR)을 만듭니다.
3. **그래프를 최적화합니다** — 커널 융합, 메모리 할당 최적화 등을 적용합니다.
4. **다시 실행 가능한 코드로 생성합니다** — [[CUDA 커널]], 또는 더 간단한 [[PyTorch]] 연산으로 컴파일합니다.

### 예시

```python
import torch
from torch._dynamo import optimize

def model(x):
    y = torch.nn.functional.linear(x, weight=W)
    z = torch.relu(y)
    return z

# Dynamo로 최적화
optimized = optimize(model)

# 사용
x = torch.randn(batch_size, input_dim)
output = optimized(x)  # 컴파일된 버전 실행
```

내부적으로는:
1. `model`의 실행을 추적
2. linear → relu 연산을 그래프로 표현
3. 어떤 커널이 두 연산을 합칠 수 있는지 판단
4. 융합된 커널 호출로 변환

## 실제 메커니즘

### Bytecode 레벨 추적

Dynamo는 [[CPython]] 바이트코드를 직접 분석합니다. 이렇게 하면 [[Python 컨트롤 플로우]](if, for 등)를 캡처할 수 있습니다.

```python
def forward(x, steps):
    for i in range(steps):
        x = x + 1  # 반복
    return x
```

Dynamo는 이 반복을 "무표하나 선택적으로" 펼칩니다(unroll). 만약 `steps`가 컴파일 시점에 알려지면 정적으로 펼치고, 동적이면 [[런타임 가드]](guard)를 설정합니다.

### 백엔드

Dynamo는 그래프 IR을 여러 백엔드로 컴파일할 수 있습니다:

- **TorchInductor**: NVIDIA [[Triton]] 또는 [[cuBLAS]] 호출로 컴파일. [[H100]], [[A100]]에서 최적화.
- **ONNX Runtime**: [[ONNX]] 포맷으로 변환 후 최적화. 다양한 하드웨어 지원.
- **TensorRT**: [[NVIDIA]] TensorRT로 컴파일. 프로덕션 서빙용.

## 성능: 실제 수치

공식 벤치마크 (PyTorch 2.0, H100 GPU):

| 모델 | 원본 | Dynamo | 향상도 |
|------|------|--------|-------|
| [[ResNet]]-50 | 1.0x | 1.25x | +25% |
| [[BERT]] | 1.0x | 1.35x | +35% |
| [[GPT-2]] (추론) | 1.0x | 1.18x | +18% |
| [[Vision Transformer]] | 1.0x | 1.42x | +42% |

향상도는 모델과 배치 크기에 따라 다릅니다. 작은 배치에서는 컴파일 오버헤드 때문에 이득이 적고, 큰 배치에서는 최적화 이득이 큽니다.

### LLM 추론에서의 성능

[[vLLM]]과 Dynamo를 함께 사용하면:
- **Prefill 단계**: 1.2~1.5배 속도 향상 (많은 연산, 그래프화 이득 큼)
- **Decode 단계**: 0.9~1.1배 (작은 배치, 컴파일 오버헤드 커짐)

따라서 실제 서빙에서는 주로 prefill을 Dynamo로 최적화합니다.

## 장점과 한계

### 장점

- **점진적 도입 가능**: 기존 PyTorch 코드에 `@torch.compile` 데코레이터만 추가하면 됩니다.
- **동적 코드 지원**: 조건부, 반복, 함수 호출 같은 동적 로직이 섞여 있어도 대부분 처리합니다.
- **다양한 백엔드**: 같은 코드로 다양한 하드웨어에 배포 가능합니다.

### 한계

1. **컴파일 시간**: 처음 호출할 때 몇 초 ~ 분 정도 걸립니다. 이를 "warmup"이라고 부르며, 프로덕션에서는 사전 컴파일이 필요합니다.
2. **메모리 오버헤드**: 컴파일된 코드 캐시, 중간 표현, 최적화 정보 등이 메모리를 차지합니다.
3. **일부 연산 미지원**: [[동적 shape]](shape이 런타임에 결정) 같은 경우 Dynamo가 제대로 처리하지 못할 수 있습니다.
4. **디버깅 어려움**: 컴파일된 코드는 [[스택 트레이스]]가 복잡해집니다.

## 실제 배포 사례

### [[HuggingFace]] Transformers

최신 버전(4.40+)은 Dynamo 지원을 기본으로 제공합니다:

```python
from transformers import AutoModelForCausalLM
import torch

model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b")
model = torch.compile(model)

# 사용
output = model(input_ids=inputs)  # 첫 호출: 컴파일 + 실행
# 이후 호출: 컴파일된 버전 사용
```

### [[TensorRT]]와의 협력

Dynamo-TensorRT 통합을 통해 엔터프라이즈급 최적화를 제공합니다. [[NVIDIA]]는 이를 "TensorRT-LLM" 프레임워크로 패키징했습니다.

## 미래: Dynamo 2.0과 AutoTune

현재 개발 중인 것들:

1. **동적 shape 완벽 지원**: 가변 배치 크기, 시퀀스 길이를 더 잘 처리.
2. **자동 하이퍼파라미터 튜닝**: 컴파일 옵션, 커널 선택 등을 자동화.
3. **분산 학습·추론 지원**: [[FSDP]](Fully Sharded Data Parallel), [[Tensor Parallel]] 통합.

Dynamo는 PyTorch가 "동적 + 최적화"를 동시에 달성하기 위한 핵심 투자입니다. LLM 추론이 점점 더 복잡해지면서(프롬프트 길이, 배치 크기 변동), Dynamo 같은 적응형 컴파일이 더욱 중요해질 것으로 예상됩니다.
