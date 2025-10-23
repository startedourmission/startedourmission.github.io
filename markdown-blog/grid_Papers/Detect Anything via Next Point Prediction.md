---
date: 2025-10-22
tags:
  - 논문
  - 객체탐지
  - LLM
aliases:
image: "![[1-das.png]]"
description: |-
  LLM이 전통적인 컴퓨터 비전 태스크에 도전장을 내밉니다. 새로운 MLLM 객체 탐지 모델입니다. 원래는 효율과 정확도 문제로 쉽사리 정복하지 못한 분야죠. 
  Qwen과 대규모 영상 데이터셋을 갈아넣어 각종 벤치마크에서 뛰어난 성능을 보였습니다.
---

객체 검출은 오랫동안 YOLO, DETR, Grounding DINO와 같은 회귀 기반 모델이 주도해왔습니다. 최근 MLLM(Multimodal Large Language Model)을 활용한 시도들이 있었지만, 낮은 재현율, 중복 예측, 좌표 불일치 등의 문제에 직면했습니다. 이 논문은 이러한 격차를 해소하기 위해 Rex-Omni라는 3B 파라미터 MLLM을 제안합니다. Rex-Omni는 COCO와 LVIS 벤치마크에서 제로샷 설정으로 DINO, Grounding DINO와 같은 회귀 기반 모델과 비슷하거나 더 나은 성능을 달성합니다.

> Q. Jiang, J. Huo, X. Chen, Y. Xiong, Z. Zeng, Y. Chen, T. Ren, J. Yu, and L. Zhang, "Detect Anything via Next Point Prediction", arXiv preprint arXiv:2510.12798, 2025.

![[1-das.png|851x446]]
## 요약

**아키텍처**: Rex-Omni는 Qwen2.5-VL-3B를 기반으로 구축되었으며, 0부터 999까지의 양자화된 좌표를 나타내는 특수 토큰을 사용합니다. 마지막 1,000개의 어휘 토큰을 재사용하여 좌표를 표현합니다.

**태스크 정의**: 모든 시각 인식 태스크를 좌표 예측으로 통합합니다. 포인팅은 한 점, 검출은 두 점으로 바운딩 박스, 폴리곤은 네 개 이상의 점, 키포인트는 여러 의미적 점을 출력합니다.

**데이터 엔진**: 세 가지 전문 데이터 엔진을 구축했습니다.

- **Grounding Data Engine**: DINO-X로 약 300만 개의 이미지에 grounding 레이블 생성
- **Referring Data Engine**: Qwen2.5-VL-7B와 Molmo를 사용하여 약 300만 개의 referring 데이터 생성
- **기타 엔진**: Pointing(500만), OCR(200만) 데이터 생성

공개 데이터셋 890만 개와 합쳐 총 2,200만 개의 고품질 학습 데이터를 확보했습니다.

**학습 방법**: 2단계 학습 파이프라인을 채택합니다.

- **1단계 (SFT)**: 2,200만 개 데이터로 지도 학습 미세조정
- **2단계 (GRPO)**: 기하학적 인식 리워드를 사용한 강화학습 후처리

**평가 메트릭**: 전통적인 mAP 대신 Recall, Precision, F1 스코어를 사용합니다. IoU 임계값 0.5, 0.95, 평균(0.5~0.95)에서 평가합니다.

**주요 결과**:

- **COCO**: F1@IoU 0.5에서 72.0%, DINO-R50(60.6%)과 Grounding DINO(69.8%)를 능가
- **LVIS**: F1@IoU 0.5에서 64.3%, Grounding DINO(47.7%)를 크게 초과
- **Dense200**: F1@IoU 0.5에서 78.4%, 기존 MLLM들이 대부분 실패한 밀집 객체 검출에서 우수한 성능
- **Referring**: HumanRef에서 F1@mIoU 79.9%, SEED1.5-VL(81.6%)에 근접
- **GUI Grounding**: ScreenSpot V2에서 86.8%, 3B 모델 중 최고

# 논문 상세

## Introduction

객체 검출은 초기 CNN 기반 구조(YOLO, Faster R-CNN)에서 트랜스포머 기반 모델(DETR, DINO)로 발전했으며, 폐쇄형 검출에서 개방형 검출로 진화했습니다.

**목표**: 임의의 객체와 개념을 식별할 수 있는 모델 개발

**기존 접근법의 한계**:

1. **개방 어휘 검출 모델(Grounding DINO 등)**
    
    - BERT나 CLIP 같은 텍스트 인코더 사용
    - 얕은 언어 이해로 복잡한 의미 설명 처리 어려움
    - 예: "빨간 사과" 입력에도 모든 사과 검출
2. **기존 MLLM 기반 접근법**
    
    - 좌표를 이산 토큰으로 표현하고 다음 토큰 예측으로 바운딩 박스 생성
    - 정확한 객체 위치 파악 어려움
    - 낮은 재현율, 좌표 드리프트, 중복 예측 문제

**성능 격차의 두 가지 근본 원인**:

### 1. 이산-연속 매핑의 어려움

MLLMs는 좌표 예측을 이산 분류 작업으로 다룹니다. 절대 좌표 값을 직접 생성하고 크로스엔트로피 손실을 사용합니다.

**문제점**:

- 회귀 기반 모델은 연속적이고 기하학적으로 인식하는 손실(L1, GIoU) 사용
- 작은 픽셀 오정렬도 불균형하게 큰 크로스엔트로피 손실 발생
- 예: GT가 (32, 66)이고 예측이 (34, 69)인 경우
    - 회귀 손실: L1(34, 32) + L1(69, 66) = 낮은 값
    - 분류 손실: CE(34, 32) + CE(69, 66) = 높은 값

### 2. Teacher Forcing의 한계

SFT(Supervised Fine-tuning)는 teacher forcing 방식을 사용합니다.

**문제점**:

- 학습 중에는 항상 정답 접두사를 조건으로 함
- 모델 자체의 불완전한 예측에 노출되지 않음
- 학습과 추론의 불일치
- 자율적 생성 시 구조 조절 실패
- 결과: 중복 예측이나 객체 누락 발생

## Rex-Omni의 핵심 설계

### 1. 태스크 정의

**좌표 표현 방식 선택**:

세 가지 패러다임 비교:

1. **직접 좌표 예측** (채택): 좌표를 LLM 어휘의 이산 토큰으로 처리
2. **검색 기반**: 추가 제안 모듈 사용, LLM이 후보 영역의 인덱스 예측
3. **외부 디코더**: LLM이 특수 토큰 예측, 임베딩을 외부 디코더에 전달

**좌표 형식 선택**:

세 가지 변형 비교:

1. **특수 토큰을 사용한 상대 좌표** (채택): 0~999로 양자화, 각 좌표를 특수 토큰으로 표현
2. **특수 토큰 없는 상대 좌표**: 1,000개 구간으로 양자화하지만 여러 원자 토큰 사용
3. **절대 좌표**: 1921을 (1, 9, 2, 1)로 토큰화

**채택 이유**:

- 상대 좌표: 1,000개 범주로 제한하여 학습 복잡도 감소
- 특수 토큰: 토큰 효율성 향상 (박스당 4토큰 vs 15토큰)

**입력 형식**:

텍스트 프롬프트 예시:

```
Please detect pigeon, person, truck, snow in this image. 
Return the output in box format.
```

비주얼 프롬프트 예시:

```
Here are some example boxes specifying the location of several objects 
in the image: "object1": ["<12><412><339><568>", "<92><55><179><378>"]. 
Please detect all objects with the same category and return their 
bounding boxes in [x0, y0, x1, y1] format.
```

**출력 형식**:

기본 구조:

```
<|object_ref_start|>PHRASE<|object_ref_end|><|box_start|>COORDS<|box_end|>
```

바운딩 박스:

```
<|object_ref_start|>person<|object_ref_end|><|box_start|>
<12><42><512><612>, <24><66><172><623>, ...<|box_end|>
```

포인트:

```
<|object_ref_start|>button<|object_ref_end|><|box_start|>
<100><150>,<200><250>, ...<|box_end|>
```

키포인트:

```json
{"person1": {"box": <0><123><42><256>, 
"keypoints": {"left eye": <32><43>, "right eye": <66><55>, ...}}}
```

**모델 아키텍처**:

Qwen2.5-VL-3B-Instruct 기반으로 최소한의 수정:

- 어휘의 마지막 1,000개 토큰을 0~999 좌표를 나타내는 특수 토큰으로 재사용
- 추가 파라미터 없음
- 네이티브 해상도 ViT 사용

### 2. 학습 데이터

**공개 데이터셋**: 약 890만 샘플

- Object Detection: APTv2, BDD100K, O365, COCO 등
- Referring: RefCOCOg, HumanRef
- OCR: HierText, ICDAR2013/2015, TextOCR 등
- GUI Grounding: Os-Atlas, UI-Ref Exp, ShowUI
- Keypointing: COCO-Keypoint, MPII, CrowdPose 등

**Grounding Data Engine**: 약 300만 이미지

1. **이미지 캡셔닝**: Qwen2.5-VL-7B로 설명 생성
2. **구문 추출**: SpaCy로 명사구 추출
3. **구문 필터링**: 형용사 등 속성 포함 구문 제거 (예: "green lemon" 제거, "lemon" 유지)
    - 이유: 현재 grounding 모델들이 속성 이해 부족
4. **구문 grounding**: DINO-X로 바운딩 박스 생성

**Referring Data Engine**: 약 300만 이미지

1. **표현 생성**: Qwen2.5-VL-7B로 referring expression 생성
2. **포인팅**: Molmo로 각 표현의 공간 포인트 생성
3. **마스크 생성**: SAM으로 각 GT 박스의 마스크 생성
4. **포인트-박스 연결**: Molmo의 포인트가 마스크 내에 있으면 박스와 referring expression 연결

**기타 데이터 엔진**:

- **Pointing**: 약 500만 샘플. SAM으로 마스크 생성, 회전 사각형의 대각선 교점을 포인트로 사용
- **OCR**: 약 200만 샘플. PaddleOCR로 텍스트 영역과 전사 추출

**총 데이터**: 2,200만 고품질 주석 이미지

### 3. 학습 파이프라인

#### 1단계: Supervised Fine-tuning (SFT)

**온라인 대화 데이터 구성 전략**:

- 다양한 질문 템플릿 사용
- 이미지당 1~N개의 구문 무작위 샘플링
- 비주얼 프롬프팅 훈련 포함

**학습 설정**:

- 8노드 × 8 A100 GPU
- 약 8일 학습
- 모든 파라미터 업데이트
- 학습률: Vision Encoder 2e-6, Projection & LLM 2e-5
- AdamW 옵티마이저
- 입력 픽셀: 16×28×28 ~ 2560×28×28

#### 2단계: GRPO 기반 강화학습 후처리

**SFT의 한계**:

1. **기하학적 이산화 문제**
    
    - 좌표를 범주 토큰(<0>~<999>)으로 표현
    - GT가 <33>이고 예측이 <32>면 픽셀 차이는 무시할 수 있지만 CE 손실은 완전히 틀린 것으로 처리
    - GT가 <0><0><100><100>이고 예측이 <0><0><100><1000>이면 하나의 토큰만 틀렸지만 박스는 심각하게 잘못됨
2. **행동 조절 결핍**
    
    - Teacher forcing으로 박스 수가 GT와 동일하게 고정
    - 모델이 자율적으로 객체 수 학습 못함
    - 추론 시: (1) 예측 박스 부족 또는 (2) 과도한 예측 (동일/약간 이동한 좌표 반복)

**GRPO 작동 방식**:

이미지와 질문 $(I, x)$가 주어지면:

1. 현재 정책 $\pi_\theta$에서 $G$개의 완전한 응답 샘플링
2. 각 출력 $o_i$에 대해 스칼라 리워드 $r_i$ 계산
3. 그룹 전체에서 정규화하여 상대적 이점 계산:

$$A_i = \frac{r_i - \text{mean}(r_1, \ldots, r_G)}{\text{std}(r_1, \ldots, r_G)}$$

4. GRPO 목적 함수:

$$\mathcal{J}_{\text{GRPO}}(\theta) = \frac{1}{G} \sum_{i=1}^{G} \frac{1}{|o_i|} \sum_{t=1}^{|o_i|} [\min(\rho_{i,t} \hat{A}_{i,t}, \text{clip}(\rho_{i,t}, 1-\epsilon, 1+\epsilon) \hat{A}_{i,t}) - \beta D_{KL}[\pi_\theta | \pi_{\text{ref}}]$$

**기하학적 인식 리워드**:

1. **Box IoU Reward** (검출, grounding, referring, OCR)
    - GT 박스와 예측 박스 매칭
    - 카테고리 일치하면 IoU를 리워드로, 아니면 0
    - Recall, Precision, F1 계산:

$$\text{Recall} = \frac{\sum_{j=1}^{n} r_j}{n}, \quad \text{Precision} = \frac{\sum_{j=1}^{n} r_j}{m}, \quad r_{\text{IoU}} = \frac{2 \cdot \text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall} + \epsilon}$$

2. **Point-in-Mask Reward** (포인팅 태스크)
    
    - SAM으로 GT 박스의 마스크 추출
    - 예측 포인트가 마스크 내부이고 카테고리 일치하면 1, 아니면 0
3. **Point-in-Box Reward** (GUI Grounding)
    
    - 예측 포인트가 GT 박스 내부면 1, 아니면 0

**학습 설정**:

- SFT 데이터셋에서 66K 샘플 사용
- 8 A100 GPU, 약 24시간
- Rollout 크기: 8
- KL 페널티 $\beta$: 0.01
- 배치 크기: 64

## 벤치마크 결과

### Common Object Detection (COCO)

**평가 설정**:

- 5,000개 테스트 이미지, 80개 카테고리
- Rex-Omni-SFT: SFT만 거친 모델
- Rex-Omni: SFT + GRPO 모델
- Temperature 0으로 평가

**주요 결과**:

- **F1@IoU 0.5**: Rex-Omni 72.0% > DINO-R50 60.6%, Grounding DINO 69.8%
- **F1@IoU 0.95**: Rex-Omni 15.9%, DAB-DETR 13.4%를 약간 상회
- **F1@mIoU**: Rex-Omni 52.9% > Grounding DINO 48.1%

**의미**:

- MLLM 기반 검출이 제로샷으로 회귀 기반 모델 능가 가능
- IoU 0.95에서는 회귀 모델에 약간 뒤처짐 (정밀한 박스 위치에서는 한계)
- GRPO 후처리로 큰 성능 향상 (SFT 68.2% → GRPO 72.0%)
![[2-das.png|874x429]]
### Long-tailed Object Detection (LVIS)

**벤치마크**: 1,203개 카테고리, 19,626개 테스트 이미지

**주요 결과**:

- **F1@IoU 0.5**: Rex-Omni 64.3% > Grounding DINO 47.7%
- **F1@mIoU**: Rex-Omni 46.9% > Grounding DINO 31.9%

**의미**:

- MLLM의 강력한 언어 이해가 저빈도 카테고리에서 우수한 일반화
- mIoU에서 최고 성능 달성 (정밀한 박스 위치)
![[3-das.png|874x429]]

### Dense and Tiny Object Detection

**벤치마크**:

- **VisDrone**: 1,610개 항공 교통 이미지, 평균 박스 크기 30.7×32.4
- **Dense200**: 200개 이미지, 평균 91.2개 박스/이미지, 평균 크기 66.8×64.5

**주요 결과**:

- **Dense200**: Rex-Omni F1@0.5 78.4% >> 대부분 MLLM < 30%
- **VisDrone**: Rex-Omni F1@0.5 61.6% >> 대부분 MLLM < 40%

**실패 모드 분석**:

1. **Large-box prediction**: 여러 인접 객체를 하나의 큰 박스로 커버
2. **Structured duplicate predictions**: 최소 오프셋으로 좌표 반복

**GRPO의 효과**:

- SFT-only 모델은 이러한 문제 심각
- GRPO 후처리로 중복 예측 거의 사라짐
![[4-das.png|874x429]]
### Referring Object Detection

**벤치마크**:

- **RefCOCOg**: 4,889 val, 9,577 test expressions
- **HumanRef**: 5,000개 이미지, 6개 서브셋 (속성, 위치, 상호작용, 추론, 유명인)

**주요 결과**:

- **HumanRef**: Rex-Omni F1@mIoU 79.9%, SEED1.5-VL 81.6%에 근접
- **RefCOCOg val**: Rex-Omni F1@0.5 86.6% > Grounding DINO 52.9%
- **RefCOCOg test**: Rex-Omni F1@0.5 86.8% > Grounding DINO 53.8%

![[5-das.png|874x429]]
### Visual Prompting

**평가**:

- **FSC147**: 1,190개 이미지, 객체 카운팅 데이터셋
- **COCO, LVIS, Dense200**: 각 카테고리당 하나의 박스를 비주얼 프롬프트로 샘플링

**주요 결과**:

- 전통 전문가 모델 T-Rex2에는 미치지 못하지만 강력한 성능
- 특히 밀집 장면과 롱테일 시나리오에서 우수

### Object Pointing

**평가**: COCO, LVIS, Dense200, VisDrone, RefCOCOg, HumanRef에서 포인트 예측

**주요 결과**:

- **COCO**: Rex-Omni 80.5% > Molmo-7B 77.3%, SEED1.5-VL 78.2%
- **LVIS**: Rex-Omni 70.8%, SEED1.5-VL 70.7%
- **Dense200**: Rex-Omni 82.5% >> SEED1.5-VL 72.1%
- **HumanRef**: Rex-Omni 83.8% > SEED1.5-VL 83.1%

모든 벤치마크에서 최고 F1 스코어 달성

### GUI Grounding

**벤치마크**:

- **ScreenSpot-V2**: 모바일, 데스크톱, 웹 시나리오, 1,272개 이미지
- **ScreenSpot-Pro**: 초고해상도 인터페이스, 1,581개 이미지

**주요 결과**:

- **ScreenSpot-V2 평균**: Rex-Omni 86.8%, 3B 모델 중 최고
- **ScreenSpot-Pro 평균**: Rex-Omni 55.9%, 3B 모델 중 최고

### 기타 태스크

**Layout Grounding** (DocLayNet, M6Doc):

- Rex-Omni가 다른 MLLM 크게 능가
- Closed-set 모델과는 격차 있지만 개방형 일반화 능력으로 장점

**OCR** (HierText, ICDAR2015, TotalText, SROIE):

- BBOX 형식: PaddleOCRv5와 비슷하거나 우수
- POLY 형식: ICDAR2015에서 최고 성능

**Spatial Pointing** (RefSpatial-Bench):

- Location: Rex-Omni 54.0% > Molmo-72B 45.8%
- Placement: Rex-Omni 50.0% > Molmo-72B 14.7%
- Unseen: Rex-Omni 36.4% > Molmo-72B 21.2%

**Keypoint** (COCO, AP10K):

- AP10K에서 Rex-Omni 30.1% >> X-Pose 17.0%
- 크로스 도메인 일반화 우수

## 심층 분석

### GRPO가 작동하는 이유

#### 1. 학습 역학

**SFT 단계**: 꾸준하고 점진적인 개선 **GRPO 단계**: 적은 단계로 급격한 성능 향상

해석: SFT 모델은 이미 강력한 잠재 능력을 보유하지만 충분히 활용되지 않음. GRPO가 행동 인식 리워드와 시퀀스 레벨 피드백으로 이를 해제.

#### 2. 행동 교정

**중복 예측 제거 실험**:

- SFT: COCO +1.23%, LVIS +1.38%, VisDrone +15.3% 개선
- GRPO: COCO +0.08%, VisDrone +0.1% 개선

→ GRPO가 중복 예측을 효과적으로 억제

**Large-box 예측 제거 실험** (Dense200):

- SFT: 20.5%가 large box, 제거 시 F1@mIoU 44.9→56.7
- GRPO: 3.5%만 large box, 제거 시 F1@mIoU 58.3→60.0

→ GRPO가 과도하게 큰 박스 예측 억제

#### 3. 좌표 정밀도 개선?

**제어 실험**: 두 모델이 모두 GT 매칭에 성공한 경우만 비교

- COCO: SFT 63.0% → GRPO 63.5% (미미한 향상)
- LVIS: SFT 56.6% → GRPO 56.9% (미미한 향상)

→ GRPO의 주요 이점은 좌표 정밀도 향상이 아니라 행동 결함 교정

#### 4. 올바른 예측의 가능성 향상

**고온 샘플링 실험**:

- **SFT-Sampling-Best**: 8회 전체 데이터셋 테스트 중 최고 F1
- **SFT-Sampling-Vote**: 각 샘플마다 8개 출력 중 최고 선택

**결과**:

- COCO: SFT-Sampling-Vote 72.6% > GRPO 72.0% (SFT가 잠재 능력 보유)
- LVIS/Dense200: SFT-Sampling은 GRPO에 미치지 못함

→ GRPO는 간단한 데이터셋에서는 샘플링 일관성 향상, 복잡한 태스크에서는 본질적으로 더 정확한 예측 가능

### 추론 효율성과 속도

**토큰화 효율성**:

- **COCO**: Rex-Omni 7.6 tokens/box vs SEED1.5-VL 148.8 tokens/box
- **Dense200**: Rex-Omni 5.1 tokens/box vs SEED1.5-VL 74.5 tokens/box

**추론 속도** (A100 GPU, vLLM, BF16):

- 0-29 박스: < 2초
- 410-419 박스: > 16초

속도는 예측 객체 수에 선형 비례. 현재 MLLM 기반 검출기는 전통 최적화된 검출기보다 느리지만, 양자화나 증류로 개선 가능.

## 관련 연구

### Regression-based Object Detection

CNN 기반 초기 모델(YOLO, SSD, Faster R-CNN)에서 앵커 프리 접근법(CornerNet, CenterNet, FCOS)을 거쳐 트랜스포머 기반 검출기(DETR, Deformable DETR, DINO)로 진화했습니다.

지속적 개선을 위한 혁신들:

- 아키텍처: FPN
- 손실 함수: Focal Loss
- 데이터 증강: MixUp, Mosaic

### Open-set Object Detection

텍스트 프롬프트를 사용한 개방 어휘 검출:

- GLIP: 구문 grounding 데이터로 학습
- Grounding DINO: DINO와 GLIP 결합
- DINO-X: 확장된 개방 어휘 검출

### MLLM-based Object Detection

직접 좌표 예측:

- Pix2Seq: 상대 좌표를 특수 토큰으로
- GPT4RoI: ROI 특징 사용
- Shikra, Ferret, Qwen2.5-VL: 다양한 좌표 표현

검색 기반:

- KOSMOS-2: 개체를 텍스트로 연결
- Osprey: 마스크 기반 제안
- VistaLLM: 영역 특징과 LLM 정렬

외부 디코더:

- LLaVA-Grounding: 바운딩 박스 생성 모듈
- VisionLLM: 다양한 비전 중심 작업
- PSALM: 세그멘테이션 기반 검출

## 결론

Rex-Omni는 MLLM 기반 객체 검출의 문제를 체계적으로 해결합니다.

**핵심 기여**:

1. **효율적인 좌표 토큰화**: 특수 토큰으로 학습 복잡도 감소 및 효율성 향상
2. **대규모 데이터 생성**: 맞춤형 엔진으로 2,200만 개 고품질 데이터 확보
3. **2단계 학습 파이프라인**: SFT + GRPO로 정확한 위치 파악과 깊은 언어 이해 달성
4. **행동 교정**: GRPO가 SFT 유도 결함(중복 예측, large-box 예측) 효과적으로 교정

**실험 검증**:

- 다양한 시각 인식 태스크에서 최고 또는 경쟁력 있는 제로샷 성능
- GRPO의 필수성 입증

**한계와 향후 과제**:

- 추론 속도: 모델 가속화 및 고급 리워드 기반 샘플링 필요
- MLLM의 행동 및 기하학적 한계 극복 가능성 입증

Rex-Omni는 다재다능하고 언어 인식 능력을 갖춘 차세대 인식 시스템으로 가는 중요한 단계입니다.

