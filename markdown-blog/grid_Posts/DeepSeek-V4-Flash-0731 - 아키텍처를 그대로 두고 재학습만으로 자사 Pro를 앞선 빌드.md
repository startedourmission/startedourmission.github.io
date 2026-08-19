---
date: 2026-08-01
tags:
  - 정보
  - Headliner
  - LLM
  - 에이전트
  - 벤치마크
description: 파라미터 수와 아키텍처를 프리뷰와 동일하게 유지한 채 학습과 포스트트레이닝만 갈아끼워 Terminal-Bench 2.1을 61.8에서 82.7로, DeepSWE를 7.3에서 54.4로 끌어올린 빌드입니다.
image: "![[deepseek-v4-flash-0731-thumb.png]]"
---

[[DeepSeek]]이 2026년 7월 31일 V4-Flash의 공개 베타를 냈습니다. 빌드명은 V4-Flash-0731입니다.

릴리스에서 회사가 명시적으로 못 박은 문장이 하나 있습니다. 프리뷰와 아키텍처도 파라미터 수도 같습니다. 바뀐 것은 학습과 포스트트레이닝뿐입니다.

## 무엇이 올랐나

DeepSeek이 공개한 아홉 개 에이전트·코딩 벤치마크 점수입니다.

| 벤치마크 | V4-Flash-0731 |
| --- | --- |
| Terminal-Bench 2.1 | 82.7 |
| Cybergym | 76.7 |
| Toolathlon (verified) | 70.3 |
| DSBench-FullStack | 68.7 |
| DSBench-Hard | 59.6 |
| DeepSWE | 54.4 |
| NL2Repo | 54.2 |
| Agent Last Exam | 25.2 |
| Automation Bench (Public) | 25.1 |

프리뷰 빌드와 비교하면 Terminal-Bench 2.1이 61.8에서 82.7로, DeepSWE가 7.3에서 54.4로 올랐습니다. 두 번째 숫자는 7배가 넘습니다.

그리고 회사가 공개한 아홉 개 전부에서 자사 상위 모델인 V4-Pro-Preview를 앞섭니다.

## 대조군이 생겼다

이 릴리스가 흥미로운 이유는 점수가 아니라 실험 설계입니다.

보통 새 모델이 나오면 아키텍처, 데이터, 파라미터 수, 포스트트레이닝 레시피가 한꺼번에 바뀝니다. 그래서 성능이 올랐을 때 무엇이 기여했는지 밖에서는 알 수 없습니다. 벤치마크 점수가 모델 능력을 재는 것인지 레시피를 재는 것인지 구분할 방법이 없었습니다.

이번에는 아키텍처와 파라미터가 고정된 대조군이 생겼습니다. 284B 총 파라미터에 13B 활성, 컨텍스트 1M, 최대 출력 384K. 프리뷰와 같습니다. 달라진 것은 학습 파이프라인뿐입니다.

그 조건에서 DeepSWE가 7.3에서 54.4로 갔습니다. 이 숫자를 읽는 방법은 둘입니다.

하나는 포스트트레이닝에 아직 이만큼이 남아 있다는 해석입니다. 같은 가중치 구조로 에이전트 태스크 성능을 7배 올릴 수 있다면, 지금 프런티어 모델들의 점수 중 상당 부분은 아키텍처가 아니라 레시피의 몫입니다.

다른 하나는 프리뷰 빌드가 에이전트 태스크에서 덜 익은 상태로 나왔다는 해석입니다. DeepSWE 7.3은 사실상 바닥입니다. 바닥에서 출발하면 배수는 크게 나옵니다. 이 경우 54.4가 절대적으로 어느 수준인지를 따로 봐야 합니다.

두 해석 중 어느 쪽인지는 제3자 검증이 나와야 갈립니다.

## Flash가 Pro를 앞선다

제품 라인 쪽 함의가 더 직접적입니다.

| | V4-Flash-0731 | V4-Pro (Preview) |
| --- | --- | --- |
| 총 파라미터 | 284B | 1.6T |
| 활성 파라미터 | 13B | 49B |
| 컨텍스트 | 1M | 1M |
| 캐시 미스 입력 (100만 토큰) | $0.14 | $0.435 |
| 출력 (100만 토큰) | $0.28 | $0.87 |

Flash가 Pro의 6분의 1 크기이고 3분의 1 가격인데, 회사가 공개한 아홉 개 에이전트 벤치마크에서 Pro를 앞섭니다.

티어 이름이 성능 순서를 보장하지 못하게 됐습니다. Flash는 원래 "빠르고 싸지만 덜 똑똑한" 자리였는데, 학습 레시피 세대가 다르면 그 관계가 뒤집힙니다. 사용자 입장에서는 모델을 고를 때 티어 이름이 아니라 빌드 날짜를 봐야 한다는 뜻입니다.

Pro는 아직 프리뷰이고 정식 출시가 예고돼 있습니다. 같은 레시피가 Pro에 적용되면 순서는 다시 정상화될 가능성이 큽니다. 지금 상태는 과도기입니다.

## 이 숫자를 어디까지 믿을 것인가

아홉 개 점수는 전부 DeepSeek 자체 평가 하네스에서 나왔고, 2026년 7월 31일 기준 제3자 검증이 없습니다.

에이전트 벤치마크는 하네스에 특히 민감합니다. 같은 모델이라도 툴 호출 규약, 재시도 정책, 컨텍스트 관리 방식에 따라 점수가 크게 흔들립니다. Terminal-Bench나 DeepSWE 같은 벤치마크는 모델 단독 능력이 아니라 모델과 하네스의 조합을 잽니다. 자사 하네스에서 자사 모델 둘을 비교한 숫자라면, 두 모델 사이의 상대 비교로는 유효하지만 다른 회사 모델과의 절대 비교로 쓰기는 어렵습니다.

Artificial Analysis의 독립 측정에서는 V4 Flash 0731(Reasoning, Max Effort)이 Intelligence Index 50입니다. Opus 4.8급이라는 표현이 돌지만, 그 주장이 성립하는 범위는 에이전트·코딩 태스크에 한정해서 읽는 편이 안전합니다.

가격은 확실합니다. 입력 100만 토큰당 $0.14, 출력 $0.28. 캐시 히트 입력은 $0.0028입니다. 에이전트 워크로드처럼 같은 컨텍스트를 반복해서 넣는 경우 캐시 히트 가격이 실질 비용을 결정하는데, 이 자리에서는 격차가 훨씬 큽니다.

## 정리

포스트트레이닝만 바꾼 대조군이 공개된 것이 이 릴리스의 실질입니다. 벤치마크 점수 중 어디까지가 모델이고 어디까지가 레시피인지 물을 수 있는 사례가 하나 생겼습니다.

다만 아홉 개 숫자 전부가 자체 하네스에서 나왔고 검증이 없습니다. 제3자 재현이 붙기 전까지는 DeepSeek 내부의 두 빌드를 비교하는 용도로만 쓰는 편이 맞습니다.

---

- [DeepSeek V4 Flash 0731 Intelligence, Performance and Price Analysis (Artificial Analysis)](https://artificialanalysis.ai/models/deepseek-v4-flash)
- [DeepSeek Retrained V4-Flash Beats Its Flagship Pro on Nine Agent Benchmarks (TechTimes)](https://www.techtimes.com/articles/322513/20260731/deepseek-retrained-v4-flash-beats-its-flagship-pro-nine-agent-benchmarks.htm)
- [DeepSeek V4 Flash 0731 Official Release, Agent Benchmarks](https://www.digitalapplied.com/blog/deepseek-v4-flash-0731-official-release-agent-benchmarks)
