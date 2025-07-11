---
date: 2025-07-01
tags:
  - C++
aliases:
---

# 성능 최적화

C++ 성능 최적화는 프로그램의 실행 속도와 메모리 사용량을 개선하는 중요한 과정입니다. 다음은 주요 최적화 기법들입니다.

## 1. 컴파일러 최적화 활용

*   **최적화 옵션 사용**: `g++ -O2` 또는 `-O3`와 같은 컴파일러 최적화 플래그를 사용하여 컴파일러가 코드를 더 효율적으로 변환하도록 지시합니다. `-O2`는 인라이닝, 루프 최적화 등을 포함하며, `-O3`는 더 공격적인 최적화를 수행합니다.
*   **CPU 아키텍처 맞춤 최적화**: `-march=native` 플래그를 사용하여 현재 CPU 아키텍처에 최적화된 코드를 생성할 수 있습니다.
*   **프로파일 기반 최적화 (PGO)**: 실제 프로그램 실행 데이터를 기반으로 최적화를 수행하여 성능을 향상시킵니다.
*   **링크 타임 최적화 (LTO)**: 여러 소스 파일에 걸쳐 전체 프로그램을 대상으로 최적화를 수행합니다.

## 2. 알고리즘 및 자료구조 최적화

*   **최적의 알고리즘 선택**: 시간 복잡도를 고려하여 문제에 가장 적합한 알고리즘을 선택하는 것이 최적화의 가장 큰 효과를 가져옵니다.
*   **적절한 컨테이너 선택**: `std::vector`와 `std::list` 등 각 컨테이너의 특성을 이해하고 상황에 맞는 것을 사용합니다.
*   **캐시 친화적인 데이터 구조 설계**: 캐시 미스를 최소화하도록 데이터에 순차적으로 접근하고, 캐시 지역성을 높이는 데이터 구조를 사용합니다.

## 3. 메모리 최적화

*   **불필요한 복사 연산 제거**:
    *   함수 인자로 값을 전달할 때 `const &` 참조를 사용합니다.
    *   C++11부터 도입된 `std::move`를 활용한 이동 의미론(move semantics)을 사용하여 불필요한 복사를 피합니다.
*   **동적 할당 최소화**:
    *   `new`, `delete`와 같은 동적 메모리 할당/해제는 비용이 높으므로 최소화합니다.
    *   `std::vector::reserve()`를 사용하여 미리 메모리를 할당하여 재할당 횟수를 줄입니다.
    *   스택 할당을 선호합니다. 스택 할당은 힙 할당보다 빠릅니다.
    *   메모리 풀(Memory Pool)이나 객체 재사용 기법을 활용하여 동적 할당 비용을 줄일 수 있습니다.
*   **스마트 포인터 활용**: `std::unique_ptr`, `std::shared_ptr` 등을 사용하여 메모리 누수를 방지하고 안전하게 메모리를 관리합니다. `unique_ptr`는 비용 패널티가 거의 없어 최적화에 유리합니다.

## 4. 코드 레벨 최적화

*   **함수 호출 최소화**:
    *   반복 호출되는 함수는 변수에 저장하여 사용하거나, 인라인 함수(`inline`)를 사용하여 함수 호출 오버헤드를 줄입니다.
    *   가상 함수 호출은 일반 함수 호출보다 느리므로, 필요할 때만 `virtual`을 사용합니다.
*   **루프 최적화**:
    *   루프 언롤링(Loop Unrolling)을 통해 루프 제어문의 오버헤드를 줄입니다.
    *   루프 내에서 불필요한 계산을 제거합니다.
*   **계산 제거 및 단순화**:
    *   불필요한 계산을 제거하고, 가능한 경우 더 빠른 연산(예: 부동 소수점 연산 대신 정수 연산, 곱셈/나눗셈 대신 비트 연산)을 사용합니다.
    *   2의 멱수로 곱셈, 나눗셈을 할 때 시프트 연산(`>>`, `<<`)을 활용합니다.
*   **`register` 변수 사용**: 자주 접근하는 변수에 `register` 키워드를 사용하여 CPU 레지스터를 활용하도록 컴파일러에 힌트를 줄 수 있습니다. (단, 컴파일러가 최적화 여부를 결정하며, 현대 컴파일러에서는 큰 효과가 없을 수 있습니다.)
*   **`const` 올바른 사용**: `const`를 사용하여 불필요한 복사를 방지하고 컴파일러가 최적화할 수 있도록 돕습니다.
*   **지역 변수 최소화 및 범위 제한**: 지역 변수의 수를 줄이고, 가장 안쪽 스코프에 선언하여 메모리 사용을 효율화합니다.
*   **초기화 선호**: 대입보다는 초기화를 사용하여 불필요한 기본 생성자 호출을 피합니다.
*   **SIMD 명령어 활용**: SIMD(Single Instruction, Multiple Data) 명령어를 사용하여 여러 데이터 요소에 대해 동시에 연산을 수행하여 성능을 향상시킵니다.

## 5. 측정 및 프로파일링

*   **코드 프로파일링**: 프로파일링 도구를 사용하여 성능 병목 현상을 식별하고, 최적화가 필요한 부분을 정확히 파악합니다.
*   **벤치마킹**: 다양한 구현이나 설정의 성능을 비교하여 최적의 방법을 찾습니다.
*   **성급한 최적화 피하기**: "성급한 최적화는 모든 악의 근원이다(Premature optimization is the root of all evil)."라는 격언처럼, 실제로 병목이 되는 부분을 측정하고 최적화하는 것이 중요합니다.

이러한 기법들을 통해 C++ 프로그램의 성능을 효과적으로 최적화할 수 있습니다.

---
### C++ 기본

- [[C++ - 개요 및 C 언어와의 차이점]]
- [[C++ - 기본 문법]]
- [[C++ - 컴파일과 링크]]
- [[C++ - IDE 및 개발 환경]]

### 객체 지향 프로그래밍 (OOP)

- [[C++ - 클래스와 객체]]
- [[C++ - 생성자 및 소멸자]]
- [[C++ - 캡슐화]]
- [[C++ - 상속]]
- [[C++ - 다형성]]
- [[C++ - 추상화]]

### 메모리 관리

- [[C++ - 동적 메모리 할당]]
- [[C++ - 스마트 포인터]]

### 고급 C++ 기능

- [[C++ - 포인터]]
- [[C++ - 참조]]
- [[C++ - 템플릿]]
- [[C++ - 예외 처리]]
- [[C++ - 표준 라이브러리 (STL)]]
- [[C++ - 파일 입출력]]
- [[C++ - 현대 C++]]

### 실무 C++

- [[C++ - 빌드 시스템]]
- [[C++ - 테스트 프레임워크]]
- [[C++ - 디버깅 기법]]
- [[C++ - 성능 최적화]]
- [[C++ - 디자인 패턴]]
- [[C++ - 실무에서 사용하는 C++의 변형]]
