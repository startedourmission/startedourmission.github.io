---
date: 2025-08-27
tags:
aliases:
  - AlexNet
image:
---
2012년, 토론토 대학의 Alex Krizhevsky, Ilya Sutskever, Geoffrey Hinton이 발표한 이 논문은 딥러닝의 시대를 연 전환점으로 평가받습니다. 흔히 **AlexNet**이라 불리며, 컴퓨터 비전 분야의 혁신을 가져왔습니다. 

---

## **1. 배경**

- 이전까지 이미지 인식은 SIFT, HOG 같은 **수작업 특징 추출**과 전통적 머신러닝에 의존.
- 하지만 **ImageNet**(1,500만 장 이상, 22,000 카테고리)의 대규모 데이터셋이 등장하면서, 더 큰 모델 학습이 가능해짐.
- GPU 발전 덕분에 **대규모 딥러닝 학습**이 현실화.

---

## **2. AlexNet 구조**

- **8개의 학습 레이어**:
    
    - 5개 Convolution layer + 3개 Fully-connected layer
        
    - 마지막은 1000-way softmax
        
    
- **파라미터 수**: 약 6천만 개
    
- **주요 특징**
    
    1. **ReLU 활성화 함수** → 학습 속도 비약적으로 향상
        
    2. **GPU 병렬 학습** (2개 GPU 활용)
        
    3. **Local Response Normalization (LRN)** → 일반화 성능 향상
        
    4. **Overlapping Pooling** → 과적합 감소
        
    5. **Dropout** (Fully-connected 층에 적용) → 과적합 방지
        
    6. **Data Augmentation** (랜덤 크롭, 색상 변화) → 데이터 다양성 확보
        
    

---

## **3. 성능 결과**

- **ILSVRC 2010**
    
    - Top-1 error: **37.5%**
        
    - Top-5 error: **17.0%** (기존 SOTA 대비 큰 폭 개선)
        
    
- **ILSVRC 2012**
    
    - Top-5 error: **15.3%** (2등 팀의 26.2%보다 압도적으로 우수)
        
    
- 이 성과로 2012 ImageNet 챌린지 **우승**
    

---

## **4. 의의**

- AlexNet은 단순한 성능 향상을 넘어 **딥러닝이 컴퓨터 비전의 주류로 자리잡는 계기**가 되었음.
    
- 이후 VGG, GoogLeNet, ResNet 등 수많은 아키텍처 발전의 기반이 됨.
    
- 오늘날의 **AI 붐**을 촉발한 역사적 연구로 평가.
    

---
**한 줄 정리**

AlexNet은 GPU, ReLU, Dropout, Data Augmentation을 결합해 대규모 데이터셋에서 딥러닝이 실질적으로 통한다는 것을 처음 증명한 논문입니다.