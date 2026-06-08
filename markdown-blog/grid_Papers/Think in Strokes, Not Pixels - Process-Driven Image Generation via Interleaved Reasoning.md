---
date: 2026-04-10
tags:
  - 논문
aliases: ""
image: "![[Pasted image 20260411132458.png]]"
description: 메타는 이미지의 세밀한 속성을 표현하기 위해 이미지 생성을 한 번에 하지 않고, 계획-스케치-검수-수정의 반복 루프로 분해합니다.
---
이미지 생성 모델은 프롬프트 하나 받고 단 한 번의 순전파로 전체 이미지를 찍어냅니다. 복잡한 공간 관계나 세밀한 속성은 이 "원샷" 방식으로는 한계가 있을 수밖에 없습니다.

Meta Superintelligence Labs, UC San Diego, Northwestern 연구진은 이 문제를 건드립니다. 이미지 생성을 4단계 반복 루프로 분해하는 "Process-Driven Image Generation"을 제안하였습니다. Plan → Sketch → Inspect → Refine. 텍스트 추론과 시각적 생성이 번갈아 가며 서로를 보정하는 구조입니다.

![[Pasted image 20260411132458.png]]

> [1] L. Zhang, J. Tian, Z. Fan, K. Li, J. Wang, W. Chen, M. Georgopoulos, F. Juefei-Xu, Y. Bao, J. McAuley, M. Li, and Z. He, "Think in Strokes, Not Pixels: Process-Driven Image Generation via Interleaved Reasoning," arXiv:2604.04746, Apr. 2026.

## 요약

**기술 스펙**: BAGEL-7B 기반 통합 멀티모달 모델. 텍스트 토큰은 Cross-Entropy Loss, 시각 토큰은 Rectified Flow (MSE Loss)로 학습. 62K 규모 데이터셋으로 SFT. 추론 시 평균 2.62 reasoning steps, 총 131 sampling steps.

**핵심**: 이미지 생성 과정을 "생각과 행동의 교차 궤적(interleaved reasoning trajectory)"으로 재정의합니다. 기존 접근이 생성 전(pre-planning) 또는 생성 후(post-refinement)에만 텍스트 추론을 적용한 것과 달리, 생성 도중에 텍스트와 비전이 서로를 실시간으로 보정합니다.

## 논문 상세

### 원샷 생성의 한계

"곰이 은색 숟가락 위에 떠 있는 이미지"를 생성해보겠습니다. 기존 모델은 곰을 숟가락 옆에 세워 놓습니다. 공간 관계를 한 번에 맞추기 어렵기 때문입니다. 텍스트 CoT(Chain-of-Thought)를 붙여도 마찬가지입니다. 텍스트만으로는 지금 이미지가 어떤 상태인지 볼 수 없습니다. 시각적 피드백 없는 추론은 본질적으로 눈을 감고 그림을 그리는 것과 같습니다.

기존 시도들도 있었습니다. 외부 VLM으로 사후 검증(PARM), GPT를 플래너로 쓰는 방식 등이 그것입니다. 하지만 이런 접근들은 생성과 추론이 분리되어 있습니다. 논문의 핵심 주장은 간단합니다. "추론과 생성이 동시에 진행되어야 한다."

### Plan-Sketch-Inspect-Refine

4단계 사이클이 핵심입니다.

**Stage I (Plan)**: 프롬프트와 지금까지의 맥락을 바탕으로, 다음에 무엇을 그릴지 텍스트로 지시합니다. `<ins>`(증분 지시)와 `<des>`(전체 장면 기술) 두 가지를 생성합니다.

**Stage II (Sketch)**: Plan에서 나온 지시를 조건으로 중간 이미지를 생성합니다. 아직 완성된 결과물은 아닙니다.

**Stage III (Inspect)**: 두 가지를 점검합니다. (1) 텍스트 지시가 원래 프롬프트와 일관적인지, (2) 생성된 스케치가 텍스트 지시에 부합하는지.

**Stage IV (Refine)**: 불일치가 발견되면 `<refine>` 지시를 생성하고, 수정된 이미지를 만듭니다.

이 4단계는 필요한 만큼 반복됩니다. 모델이 스스로 복잡도에 따라 반복 횟수를 결정합니다. 단순한 프롬프트는 적게, 복잡한 프롬프트는 많이.

### 데이터 구축: Scene Graph 기반 궤적 생성

중간 상태를 감독하는 것이 가장 어려운 부분입니다. "아직 안 그린 것"과 "잘못 그린 것"을 어떻게 구분할 수 있을까요?

세 가지 데이터셋을 구축하였습니다.

**Multi-Turn Generation (32K)**: 프롬프트를 씬 그래프(scene graph)로 분해합니다. 객체 노드, 속성 노드, 관계 엣지로 구성됩니다. 서브그래프를 순차적으로 확장하면서 각 단계의 중간 이미지와 지시를 생성합니다. Flux-Kontext로 생성하고 GPT로 필터링합니다. 추가로 GPT를 통해 "제거", "속성 변경", "교체" 같은 다양한 편집 지시도 생성하였습니다.

**Instruction-Intermediate Conflict (15K)**: SFT 모델에서 중간 궤적을 self-sampling합니다. GPT가 원래 프롬프트와의 일관성을 판단하고, 충돌이 있으면 분석과 수정 지시를 생성합니다. 핵심은 "모델 자신의 실패 패턴"을 학습하게 만드는 것입니다.

**Image-Instruction Alignment (15K)**: 생성된 이미지가 단계별 지시와 부합하는지 판단합니다. Positive 5K, Negative 10K. 시각적 수준에서의 정합성을 학습합니다.

총 62K 샘플로, PARM의 688K 대비 11배 적은 규모입니다.

### 학습

BAGEL-7B를 백본으로 사용합니다. 통합 멀티모달 모델이므로 텍스트 이해와 이미지 생성을 하나의 프레임워크에서 수행합니다. 학습 목적함수는 텍스트 CE Loss와 이미지 MSE Loss의 가중합입니다.

$$L_{total} = \lambda_{CE} \cdot L^{text}_{CE} + L^{image}_{MSE}$$

시각 토큰은 Rectified Flow 패러다임을 따릅니다. `<|vision_start|>`와 `<|vision_end|>` 특수 토큰으로 모달리티 전환을 명시합니다.

### 결과

**GenEval (구성적 정합성)**:

- BAGEL-7B 기본: 0.77 → Process-Driven: **0.83** (+5%)
- 특히 Position 0.51→0.72 (+21%), Color Attributes 0.56→0.69 (+13%)
- 12B FLUX.1-dev(0.82)를 7B 모델로 넘어섰습니다

**WISE (세계 지식 추론)**:

- BAGEL-7B 기본: 0.70 → Process-Driven: **0.76** (+6%)
- Time 0.69→0.82 (+13%), Chemistry 0.58→0.78 (+20%)

**PARM 대비 효율성**:

- 정확도: 0.83 vs 0.77 (GenEval)
- 학습 데이터: 62K vs 688K (11배 적음)
- 추론 비용: 131 steps vs ~1000 steps (8배 빠름)

**외부 모델 활용 비교**:

- GPT-4o를 플래너로 사용: 23% 성능 하락. 베이스 모델이 multi-step 지시를 안정적으로 따르지 못합니다.
- GPT-4o를 검수자로 사용: 미미한 개선에 그칩니다. 언어적 피드백을 시각적 수정으로 변환하는 능력이 없으면 효과가 없습니다.

## 생각

### 잘한 점

"시맨틱 파티셔닝"이라는 아이디어가 깔끔합니다. PARM은 디퓨전 잠재 공간(latent space)의 흐릿한 중간 상태를 감독합니다. 반면 이 논문은 "이 단계에서 고양이를 벤치 위에 올린다"처럼 구체적인 시맨틱 단위로 분해합니다. 사람이 이해할 수 있는 중간 상태를 만들었다는 점에서 해석 가능성(interpretability)이 높습니다.

Self-sampling critique도 인상적입니다. 외부 symbolic correction보다 모델 자신의 실패 패턴에서 학습한 critique가 +6% 더 효과적이라는 ablation 결과가 있습니다. 모델이 자기 분포(distribution) 안에서 만든 오류를 교정하는 것이 더 자연스럽다는 의미입니다.

62K 데이터로 688K 대비 더 좋은 성능을 낸 것도 데이터 효율성 측면에서 주목할 만합니다.

---

추론 비용이 줄긴 했지만, 여전히 원샷 대비 2.62배의 반복이 필요합니다. 실시간 생성에는 적합하지 않습니다. 논문도 이 점은 인정하고 있습니다.

Scene graph 기반 분해가 모든 프롬프트에 적용 가능한지는 의문입니다. "노을이 지는 해변의 분위기"처럼 객체-관계로 분해하기 어려운 프롬프트에서는 어떨까요? 벤치마크가 GenEval과 WISE 위주라서, 미적 품질(aesthetics)이나 추상적 프롬프트에 대한 평가는 부족합니다.

중간 이미지 생성에 Flux-Kontext를 사용하고 GPT로 필터링한다는 것은, 데이터 파이프라인 자체가 상당히 무겁다는 의미이기도 합니다. 데이터 구축의 재현 가능성은 제한적일 수 있습니다.

"생성 도중에 추론한다"는 아이디어가 중요합니다. TwiG, IRG, DraCo 같은 최근 연구들이 비슷한 방향을 탐색하고 있는데, 이 논문은 구체적인 시맨틱 단위 분해 + self-sampling critique + 효율적 학습이라는 조합으로 실질적 성능 향상을 보여주었습니다.

다만 현재는 정적 이미지에 한정됩니다. 논문 자체도 비디오와 3D로의 확장을 언급하고 있습니다. Process-driven 패러다임이 시간적/공간적 일관성이 더 중요한 비디오 생성에서 얼마나 효과적일지가 다음 관심사입니다.
