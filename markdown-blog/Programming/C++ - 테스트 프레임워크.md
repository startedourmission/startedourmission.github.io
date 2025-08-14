---
date: 2025-07-01
tags:
  - C++
aliases:
---

# 테스트 프레임워크 (Google Test)

Google Test (또는 gtest)는 Google에서 개발한 C++용 오픈 소스 테스팅 프레임워크입니다. C++ 코드를 위한 단위 테스트를 작성하는 데 도움을 줍니다.

## 주요 특징:

*   **xUnit 프레임워크 기반**: Google Test는 JUnit, NUnit과 같은 xUnit 아키텍처를 기반으로 합니다.
*   **다양한 플랫폼 지원**: Linux, Windows, Mac 등 다양한 운영체제에서 작동하며, 여러 컴파일러(GCC, Clang, MSVC 등)와 함께 사용할 수 있어 이식성이 뛰어납니다.
*   **자동 테스트 검색**: 정의된 테스트를 자동으로 검색하고 실행하므로, 모든 테스트를 수동으로 다시 나열할 필요가 없습니다.
*   **풍부한 어설션**: 부울 조건, 값 비교, 문자열 값, 부동 소수점 값 등을 확인할 수 있는 다양한 어설션 매크로를 제공합니다.
    *   `ASSERT_*` 버전은 실패 시 치명적인 오류를 발생시키고 현재 함수를 중단합니다.
    *   `EXPECT_*` 버전은 실패하더라도 현재 함수를 계속 실행합니다.
*   **테스트 픽스처 (Test Fixtures)**: 관련 테스트를 테스트 스위트로 그룹화하고, 여러 테스트에서 공유 데이터를 설정하고 해체하는 데 사용할 수 있는 테스트 픽스처를 제공합니다.
*   **죽음 테스트 (Death Tests)**: 프로세스가 특정 방식으로 종료되는지 확인하는 테스트를 작성할 수 있습니다.
*   **매개변수화된 테스트**: 값 매개변수화된 테스트와 타입 매개변수화된 테스트를 지원하여 다양한 입력에 대해 동일한 테스트 로직을 재사용할 수 있습니다.
*   **XML 테스트 보고서 생성**: 테스트 결과를 XML 형식으로 생성할 수 있습니다.

## Google Test 사용법

Google Test를 사용하여 테스트를 작성하는 기본적인 단계는 다음과 같습니다:

### 1. Google Test 설치 및 설정

Google Test는 소스 코드를 다운로드하여 직접 빌드하거나, CMake와 같은 빌드 시스템을 통해 프로젝트에 통합할 수 있습니다. (설치 과정은 복잡하므로 여기서는 생략합니다. 공식 문서를 참조하세요.)

### 2. 테스트 작성

`TEST()` 매크로를 사용하여 테스트 함수를 정의하고 이름을 지정합니다. 테스트 함수 내에서 Google Test 어설션을 사용하여 값을 확인합니다.

```cpp
#include "gtest/gtest.h"

// 두 정수를 더하는 간단한 함수 (테스트 대상)
int Add(int a, int b) {
    return a + b;
}

// TEST 매크로를 사용하여 테스트 케이스 정의
// 첫 번째 인자: Test Suite 이름 (논리적으로 관련된 테스트 그룹)
// 두 번째 인자: Test Case 이름 (Test Suite 내의 개별 테스트)
TEST(AddFunctionTest, HandlesPositiveInput) {
    // EXPECT_EQ: 두 값이 같은지 확인하는 어설션
    EXPECT_EQ(3, Add(1, 2));
    EXPECT_EQ(5, Add(2, 3));
}

TEST(AddFunctionTest, HandlesNegativeInput) {
    EXPECT_EQ(-3, Add(-1, -2));
    EXPECT_EQ(-1, Add(1, -2));
}

// 테스트 픽스처 사용 예시
class MyClass {
public:
    int value;
    MyClass() : value(0) {}
    void increment() { value++; }
};

// 테스트 픽스처 정의
class MyClassTest : public ::testing::Test {
protected:
    MyClass obj; // 각 테스트 케이스마다 새로 생성됨

    void SetUp() override {
        // 각 테스트 케이스 실행 전에 호출
        obj.value = 10;
    }

    void TearDown() override {
        // 각 테스트 케이스 실행 후에 호출
        // 자원 해제 등
    }
};

TEST_F(MyClassTest, InitialValue) {
    EXPECT_EQ(10, obj.value);
}

TEST_F(MyClassTest, IncrementValue) {
    obj.increment();
    EXPECT_EQ(11, obj.value);
}
```

### 3. 테스트 실행

`main` 함수에서 `::testing::InitGoogleTest(&argc, argv);`를 호출하여 Google Test를 초기화하고, `RUN_ALL_TESTS()`를 호출하여 모든 테스트를 실행합니다.

```cpp
#include "gtest/gtest.h"

// ... (위에서 정의한 테스트 코드들)

int main(int argc, char **argv) {
    // Google Test 초기화
    ::testing::InitGoogleTest(&argc, argv);
    // 모든 테스트 실행
    return RUN_ALL_TESTS();
}
```

Google Test는 C++ 프로젝트의 품질을 높이고, 코드 변경 시 회귀 오류를 빠르게 감지하는 데 매우 유용한 도구입니다.

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
