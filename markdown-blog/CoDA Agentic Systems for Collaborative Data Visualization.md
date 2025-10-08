---
date: 2025-10-01
tags:
  - 논문
  - 데이터분석
  - LLM
aliases:
  - 데이터 시각화까지 넘보는 LLM
image: "![[1-coda1.png]]"
description: 저는 예전부터 데이터 시각화가 어려웠습니다. 함수 이름이랑 파라미터도 잘 안 외워지고 어떤 그래프가 가장 효과적인가 판단하는 것이 쉽지 않습니다. 구글에서 시각화 시스템을 제안한 논문을 발표한 것은 굉장히 재밌습니다. 아마 Opal과 관련이 있지 않을까요?
---
개인적으로 데이터 분석 분야에서 시각화가 제일 어렵습니다. 시각화 작업은 현업 데이터 과학자도 많은 시간을 소모하는 작업이라고 하네요. LLM은 자연어 쿼리를 통한 자동화가 가능합니다. 가능은 하지만 아무래도 시각화가 사람이 이해하기 쉽고 만족할 만한 결과를 내야 의미가 있어서 한계가 명확했죠. 기존 시스템은 특히 복잡한 데이터셋 처리와 반복적 개선을 어려워했습니다. 이 논문은 전문화된 다중 에이전트 협업을 통해 이 문제를 해결하는 CoDA(Collaborative Data-visualization Agents) 시스템을 제안합니다.

> Z. Chen, J. Chen, S. Ö. Arık, M. Sra, T. Pfister and J. Yoon, "CoDA: Agentic Systems for Collaborative Data Visualization", arXiv:2510.03194, 2025.


![[1-coda1.png]]
## 요약

**아키텍처**: 다중 에이전트 시스템 (Query Analyzer, Data Processor, VizMapping Agent, Search Agent, Design Explorer, Code Generator, Debug Agent, Visual Evaluator)

**사용 모델**: Gemini-2.5-Pro (백본 LLM)

**데이터셋**:

- MatplotBench (100개 쿼리)
- Qwen Code Interpreter Benchmark (163개 시각화 예제)
- DA-Code Benchmark (78개 소프트웨어 엔지니어링 태스크)

**평가 매트릭**:

- EPR (Execution Pass Rate): 코드 실행 성공률
- VSR (Visualization Success Rate): 시각화 품질 점수
- OS (Overall Score): 코드와 시각화 품질의 종합 점수

**핵심 성과**:

- MatplotBench에서 OS 79.5% 달성 (MatplotAgent 대비 24.5% 향상)
- Qwen Code Interpreter에서 OS 89.0% 달성 (VisPath 대비 7.4% 향상)
- DA-Code에서 OS 39.0% 달성 (DA-Agent 대비 19.77% 향상)

**훈련 방법**: Fine-tuning 없이 전문화된 프롬프트 엔지니어링을 통한 다중 에이전트 협업 구현

## 논문 상세

### Introduction

데이터 분석가들은 전체 작업 시간의 2/3 이상을 낮은 수준의 데이터 준비와 시각화 작업에 소비합니다. LLM의 등장으로 자연어를 통한 시각화 자동화가 가능해졌지만, 기존 접근법들은 세 가지 핵심 과제에 어려움을 겪고 있습니다:

1. 대규모 데이터셋 처리
2. 다양한 전문 지식(언어학, 통계, 디자인) 조율
3. 반복적 피드백을 통한 출력 개선

기존 시스템들의 한계는 다음과 같습니다:

- **규칙 기반 시스템** (Voyager, Draco): 사전 정의된 템플릿에 국한되어 자연어 쿼리 처리 어려움
- **LLM 기반 방법** (CoML4VIS): 원시 데이터를 직접 입력하여 토큰 제한, 환각, 다중 소스 데이터 처리 실패
- **다중 에이전트 프레임워크** (VisPath, MatplotAgent): 메타데이터 분석 부족으로 데이터 처리에 과적합, 반복적 편집에 취약

### Method

#### 협업 다중 에이전트 패러다임

CoDA는 시각화를 단일 단계 프로세스가 아닌 협업 문제 해결 과정으로 재정의합니다. 각 에이전트는 전문 영역(메타데이터 추출, 코드 디버깅 등)에 집중하며, 공유 상태를 통해 동적으로 적응합니다.

핵심 설계 원칙:

- **전문화된 깊이**: 각 에이전트를 특정 역할(계획 vs. 실행)에 할당
- **메타데이터 중심 전처리**: 전체 데이터 로딩 없이 데이터 구조를 사전 요약
- **반복적 성찰**: 이미지 분석을 통한 인간과 유사한 출력 평가
- **모듈식 확장성**: 에이전트를 교체 가능한 모듈로 설계

#### CoDA 아키텍처

![[1-coda2.png]]

CoDA는 자연어 쿼리와 데이터 파일을 입력받아 정제된 시각화를 생성하는 8개의 전문화된 에이전트로 구성됩니다:

**1. Query Analyzer**

- 쿼리 의도 해석 (예: "지역별 판매 트렌드 시각화")
- 글로벌 TODO 리스트 생성 (데이터 필터링, 집계, 차트 선택 등)
- 하위 에이전트를 위한 가이드라인 생성

**2. Data Processor**

- pandas 등 경량 도구를 사용한 메타데이터 요약 추출 (스키마, 통계, 패턴)
- 토큰 제한 회피하며 인사이트 및 잠재적 변환 식별
- 원시 데이터 파일 업로드 없이 처리

**3. VizMapping Agent**

- 쿼리 의미를 시각화 기본 요소에 매핑
- 적절한 차트 유형 선택 (예: 트렌드용 라인 차트)
- 데이터-비주얼 바인딩 정의 및 메타데이터 기반 호환성 검증

**4. Search Agent (도구)**

- Matplotlib 라이브러리 등에서 관련 코드 예제 검색
- 검색 쿼리 생성 및 관련성 기준 결과 순위 지정

**5. Design Explorer**

- 미학적 개념 생성 (색상, 레이아웃 등)
- 사용자 경험을 위한 디자인 요소 최적화
- 디자인 품질 평가

**6. Code Generator**

- 명세를 통합한 실행 가능한 Python 코드 합성
- 모범 사례 및 문서화 보장

**7. Debug Agent**

- 타임아웃으로 코드 실행
- 오류 진단 (검색된 솔루션 활용 가능)
- 수정 적용 및 시각화 이미지 출력

**8. Visual Evaluator**

- 다차원 품질 메트릭으로 출력 이미지 평가 (명확성, 정확성, 미학, 레이아웃, 정확성)
- TODO 완료 검증 및 개선 제안

에이전트들은 공유 메모리 버퍼를 통해 구조화된 메시지를 교환하며, 피드백 루프가 자기 성찰을 유발합니다. 품질 점수가 임계값 미만이면 이슈가 상위 에이전트로 라우팅됩니다 (예: 낮은 미학 → Design Explorer로 복귀).

### Experiments

#### 벤치마크

- **Qwen Code Interpreter Benchmark**: 163개 시각화 예제, 숫자 데이터 처리 및 패턴 인식 강조
- **MatplotBench**: 100개 matplotlib 기반 쿼리, 다양한 도메인 포괄
- **DA-Code**: 78개 저장소 기반 소프트웨어 엔지니어링 태스크

#### 베이스라인

- **MatplotAgent**: matplotlib 코드 합성에 집중한 단일 에이전트 시스템
- **VisPath**: 다중 솔루션 계획 기반 접근법
- **CoML4VIS**: 구조화된 파이프라인을 따르는 워크플로우 중심 프레임워크

#### 주요 결과

**MatplotBench**:

- CoDA: EPR 99.0%, VSR 79.8%, OS 79.5%
- MatplotAgent: EPR 97.0%, VSR 56.7%, OS 55.0%
- VisPath: EPR 75.0%, VSR 37.3%, OS 38.0%
- CoML4VIS: EPR 76.0%, VSR 69.7%, OS 53.0%

**Qwen Code Interpreter**:

- CoDA: EPR 93.3%, VSR 95.4%, OS 89.0%
- MatplotAgent: EPR 81.6%, VSR 79.7%, OS 65.0%
- VisPath: EPR 86.5%, VSR 94.3%, OS 81.6%
- CoML4VIS: EPR 87.1%, VSR 90.9%, OS 79.1%

**DA-Code**:

- CoDA (Gemini-2.5-Pro): OS 39.0%
- DA-Agent (Gemini-2.5-Pro): OS 19.23%

#### 효율성 분석

CoDA는 MatplotAgent 대비 17.6% 적은 총 토큰(50,219 vs. 60,969)과 3.9% 적은 LLM 호출을 사용하면서도 훨씬 높은 정확도를 달성했습니다.

### Ablation Study

**반복 횟수 영향**:

- 1회 반복: OS 75.6%
- 3회 반복 (기본): OS 79.5%
- 5회 반복: OS 80.1% (미미한 개선)

**글로벌 TODO 리스트**:

- TODO 없음: OS 75.1% (-4.4%)
- TODO 있음: OS 79.5%

**Search Agent**:

- 검색 없음: OS 76.0% (-3.5%), EPR 90.0%
- 검색 있음: OS 79.5%, EPR 99.0%

### Conclusion

CoDA는 자연어 쿼리를 전문화된 작업 분해(이해, 계획, 생성, 자기 성찰)를 통해 처리하며, MatplotBench와 Qwen 벤치마크에서 베이스라인 대비 최대 41.5%의 정확도 향상을 달성했습니다. 메타데이터 중심 전처리와 자기 성찰 개선을 통해 입력 토큰 제한을 극복하고, 복잡한 다중 파일 데이터를 강건하게 관리합니다. 주요 한계는 다중 턴 에이전트 통신으로 인한 계산 오버헤드이며, 향후 에이전트 증류 또는 멀티모달 입력 적응이 연구 과제로 제시됩니다.