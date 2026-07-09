---
date: 2026-07-07
tags:
  - 논문
  - 에이전트
  - 오픈소스
description: "VLA와 WAM 모델을 이기종 로봇 에지 기기에서 실행하기 위한 C++ 5-레이어 추론 런타임. Python 스택 단편화 문제를 아키텍처적으로 해소하고, HY-VLA 100%, pi0.5 91% 태스크 성공률을 보고합니다."
image: "![[embodied-cpp-overview.png]]"
buzz: 45
---

> L. Xu, C. Han, B. Li, H. Wu, S. Jiang, T. Cao, C. Li, S. Zhong, and S. Wang, "Embodied.cpp: A Portable Inference Runtime of Embodied AI Models on Heterogeneous Robots," arXiv:2607.02501, 2026.

## 저자

프로젝트 리더는 Borui Li(Southeast University)와 Hao Wu(Nanjing University)입니다. 공저자로 Ling Xu, Chuanyou Li, Shuai Wang(SEU), Chuyu Han, Sheng Zhong(NJU), Shiqi Jiang(Microsoft Research), Ting Cao(AIR, Tsinghua)가 참여했습니다.

Southeast University PAISys 그룹이 주도하고 Nanjing University, Microsoft Research, Tsinghua AIR가 합류했습니다. SEU 측은 에지 디바이스 AI 추론(InfScaler, MobiLoRA)을 꾸준히 연구해 온 팀이며, Tsinghua AIR의 Ting Cao는 모바일 AI 추론 최적화를 연구해 온 연구자입니다. 실용 배포 문제를 중심에 두는 스타일의 그룹입니다.

## 배경

VLA(Vision-Language-Action) 모델과 WAM(World-Action Model)은 빠르게 다양화되고 있지만, 실제 배포는 여전히 단편화돼 있습니다. 체크포인트마다 모델별 Python 스택, 백엔드 가정, 로봇별 글루 코드를 따로 작성해야 합니다.

기존 추론 런타임(llama.cpp, ONNX Runtime, SGLang, vLLM-Omni)은 요청-응답 방식의 처리량 최적화에 맞춰 설계됐습니다. 가장 가까운 선행 작업인 vla.cpp는 7개 VLA 아키텍처를 하나의 C++ 런타임으로 통합했지만, VLA 전용입니다. 저자들이 Table 2에서 정리한 것처럼 기존 시스템 중 VLA와 WAM을 모두 지원하면서 에지 기기, 이기종 하드웨어, 로봇/시뮬레이터에 직접 연결할 수 있는 런타임은 없었습니다.

구현 소체화된 AI 배포의 런타임 계약은 세 가지로 정의됩니다. 첫째는 멀티레이트 실행(인식 인코더, 백본, 행동 헤드가 각기 다른 주기로 돌아야 함)이고, 둘째는 레이턴시 우선 배치-1 추론(클라우드 처리량 최적화가 아닌 로봇 제어 루프의 저지연·저지터 요구)이며, 셋째는 확장 가능한 인터페이스(카메라, 촉각, IMU 입력부터 행동 청크, 월드 예측 출력까지의 다양한 입출력)입니다.

## 아키텍처

![[embodied-cpp-overview.png]]

Embodied.cpp는 VLA 모델과 WAM 8개 서브타입(AR-Token VLA, VLM-Backboned VLA, Hierarchical VLA, Asynchronous VLA, Predict-then-Act WAM, Unified AR-Modeling WAM, Shared-Backbone WAM, Latent-space WAM)에서 공통 실행 경로를 추출해 5-레이어로 구성했습니다.

| 레이어 | 역할 |
| ------ | ---- |
| Input Adapters | 카메라·센서·데이터셋을 타입 지정 embodied 인터페이스로 흡수 |
| Sequence Builders | 멀티모달 입력을 backbone 입력 시퀀스로 조립 |
| Backbone Execution | 공유 트랜스포머 백본 실행 (모델 패밀리 무관) |
| Head Plugins | 행동 헤드·예측 브랜치·액션 전문가 플러그인 |
| Deployment Adapters | 런타임을 이기종 로봇 하드웨어·백엔드에 연결 |

세 가지 런타임 서브시스템이 레이어를 지원합니다. 모듈형 멀티레이트 실행은 명시적 실행 단위와 설정 가능한 새로고침 정책을 노출해 각 컴포넌트가 독립 주기로 동작하게 합니다. 레이턴시 우선 융합 실행은 그래프 재실행, 버퍼 재사용, 오퍼레이터 융합, 백엔드별 디스패치를 통해 CPU/GPU/NPU에서 소형 배치 추론을 안정적으로 수행합니다. embodied AI 커널 웨어하우스는 재사용 가능한 연산자와 모델별 커널을 수집합니다.

## 결과

HY-VLA(Hunyuan-VL 백본)와 pi0.5(PaliGemma 백본) 두 VLA 모델, 그리고 LingBot-VA WAM 단일 블록 마이크로벤치마크로 평가했습니다.

| 모델 | 태스크 성공률 | 스텝 레이턴시(ms) | 추론 레이턴시(ms) | VRAM(MiB) |
| ---- | ------------ | ---------------- | ---------------- | --------- |
| HY-VLA | **100.0%** [83.9, 100.0] | 735.9 | 1340.3 | 6850 |
| pi0.5 | **91.0%** [86, 94] | 56.85 | 266.6 | 6546 |

HY-VLA는 Hunyuan-VL 백본, 3-뷰 입력, 비디오 히스토리를 사용해 레이턴시가 높습니다. pi0.5는 더 가벼운 PaliGemma 백본과 50-프레임 행동 청크를 통해 스텝당 비용을 낮췄습니다. 두 모델 모두 C++ 경로에서 태스크 동작이 보존됩니다.

LingBot-VA WAM 단일 블록 마이크로벤치마크에서는 BF16 Python 원본과 Q4_K C++ 블록을 비교했습니다.

| 구현 | 블록당 레이턴시(ms) | 블록당 메모리(MiB) | MAE | 코사인 유사도 |
| ---- | ------------------ | ----------------- | --- | ------------ |
| Python BF16 | 3.236 | 312.2 | 0 | 1 |
| Embodied.cpp Q4_K | **3.171** | **88.1** | $< 3.3 \times 10^{-2}$ | $> 9.997 \times 10^{-1}$ |

Q4_K 양자화로 블록 메모리가 312.2 MiB에서 88.1 MiB로 줄었습니다. MAE와 코사인 유사도는 출력 드리프트가 매우 작음을 보여줍니다.

## 회고

저자들이 명시한 한계입니다. WAM 전체 폐루프 결과가 포함되지 않았습니다. LingBot-VA 전체 모델을 제한된 에지 기기에서 안정적으로 실행하지 못해 단일 블록 마이크로벤치마크만 제공합니다. 현재 버전은 초기 시스템 설계 검증 단계이며, 전체 WAM 폐루프와 더 다양한 이기종 하드웨어 조합에서의 평가는 후속 작업입니다.

또한 8개 아키텍처가 공통 실행 경로를 공유한다는 분석은 현재 공개된 대표 모델 집합을 기준으로 한 것이며, 새 모델 패밀리가 이 구분에 맞지 않는 방식으로 등장할 수 있습니다.

## 정리

- VLA와 WAM의 공통 실행 경로를 5-레이어 C++ 런타임으로 추상화해, 모델별로 Python 스택을 재작성하지 않고 에지 기기에 배포할 수 있게 합니다.
- HY-VLA 100%, pi0.5 91% 태스크 성공률로 C++ 경로의 정확도 보존을 확인했고, WAM 블록 양자화에서 $3.5\times$ 메모리 감소($312.2 \to 88.1$ MiB)와 $3.3 \times 10^{-2}$ 이하의 MAE를 달성했습니다.
- WAM 전체 폐루프 결과와 더 다양한 하드웨어 환경 검증이 남은 과제입니다.
