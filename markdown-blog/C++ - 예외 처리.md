---
date: 2025-06-30
tags:
  - C++
aliases:
---

# 예외 처리

C++ 예외 처리는 프로그램 실행 중 발생하는 오류나 예외적인 상황을 처리하는 메커니즘입니다. `try`, `catch`, `throw` 키워드를 사용하여 구현됩니다.

*   **`try` 블록**: 예외가 발생할 수 있는 코드를 포함합니다.
*   **`throw` 문**: 예외가 발생했을 때 예외 객체를 던집니다.
*   **`catch` 블록**: `try` 블록에서 던져진 예외를 잡아서 처리합니다.

**기본 구조:**

```cpp
#include <iostream>
#include <string>

double divide(int numerator, int denominator) {
    if (denominator == 0) {
        throw std::string("0으로 나눌 수 없습니다!"); // 예외 발생
    }
    return static_cast<double>(numerator) / denominator;
}

int main() {
    try {
        double result = divide(10, 0); // 예외가 발생할 수 있는 코드
        std::cout << "결과: " << result << std::endl;
    } catch (const std::string& e) { // string 타입의 예외를 잡음
        std::cerr << "예외 발생: " << e << std::endl;
    } catch (...) { // 모든 다른 타입의 예외를 잡음 (catch-all)
        std::cerr << "알 수 없는 예외 발생!" << std::endl;
    }

    std::cout << "프로그램 계속 실행." << std::endl;
    return 0;
}
```

## 예외 계층 구조 (Exception Hierarchy)

C++ 표준 라이브러리는 `std::exception`을 기반으로 하는 예외 클래스 계층 구조를 제공합니다. 이를 사용하면 예외를 더 체계적으로 관리하고 특정 타입의 예외만 처리할 수 있습니다.

```cpp
#include <iostream>
#include <stdexcept> // std::exception, std::runtime_error, std::logic_error 등

void process_data(int value) {
    if (value < 0) {
        throw std::out_of_range("값은 음수가 될 수 없습니다.");
    } else if (value == 0) {
        throw std::invalid_argument("값은 0이 될 수 없습니다.");
    }
    std::cout << "데이터 처리 완료: " << value << std::endl;
}

int main() {
    try {
        process_data(-5);
    } catch (const std::out_of_range& e) {
        std::cerr << "범위 오류: " << e.what() << std::endl;
    } catch (const std::invalid_argument& e) {
        std::cerr << "잘못된 인자: " << e.what() << std::endl;
    } catch (const std::exception& e) { // 모든 표준 예외의 기본 클래스
        std::cerr << "일반 예외: " << e.what() << std::endl;
    } catch (...) { // 모든 다른 예외
        std::cerr << "알 수 없는 예외 발생!" << std::endl;
    }
    return 0;
}
```

## `noexcept` 키워드

`noexcept` 키워드는 C++11에서 도입되었으며, 함수가 예외를 던지지 않음을 컴파일러에게 약속하는 역할을 합니다. `noexcept`로 선언된 함수가 예외를 던지면 프로그램은 즉시 종료됩니다(`std::terminate` 호출).

*   **목적**: 컴파일러가 더 많은 최적화를 수행할 수 있도록 돕고, 함수의 예외 동작에 대한 명확한 인터페이스를 제공합니다.
*   **사용법**: 함수 선언 뒤에 `noexcept`를 붙입니다.

```cpp
#include <iostream>

// 이 함수는 예외를 던지지 않음을 약속합니다.
void safe_function() noexcept {
    std::cout << "이 함수는 안전합니다." << std::endl;
    // throw std::runtime_error("오류!"); // 이 경우 std::terminate 호출
}

// 이 함수는 예외를 던질 수 있습니다.
void unsafe_function() {
    std::cout << "이 함수는 안전하지 않을 수 있습니다." << std::endl;
    throw std::runtime_error("오류 발생!");
}

int main() {
    safe_function();

    try {
        unsafe_function();
    } catch (const std::runtime_error& e) {
        std::cerr << "예외 처리됨: " << e.what() << std::endl;
    }
    return 0;
}
```

## 예외 안전성 (Exception Safety)

예외 안전성은 예외가 발생했을 때 프로그램의 상태가 어떻게 유지되는지를 나타내는 보장 수준입니다. 일반적으로 세 가지 수준의 예외 안전성이 있습니다.

1.  **기본 보장 (Basic Guarantee)**:
    *   예외가 발생해도 프로그램의 모든 불변식(invariants)이 유지됩니다.
    *   자원 누수(memory leak 등)는 발생하지 않습니다.
    *   하지만 객체의 상태는 유효하지만 예측 불가능한 상태가 될 수 있습니다.

2.  **강한 보장 (Strong Guarantee)**:
    *   예외가 발생하면 작업이 완전히 성공하거나, 아니면 작업이 시작되기 전의 원래 상태로 되돌아갑니다 (트랜잭션과 유사).
    *   "커밋 또는 롤백" 의미론을 가집니다.

3.  **예외 없음 보장 (No-Throw Guarantee)**:
    *   함수가 예외를 절대 던지지 않음을 보장합니다. `noexcept` 키워드로 명시할 수 있습니다.
    *   가장 강력한 보장 수준입니다.

예외 안전성을 고려하여 코드를 설계하는 것은 견고하고 신뢰할 수 있는 C++ 애플리케이션을 개발하는 데 중요합니다.

---
date: 2025-06-30
tags:
  - C++
aliases:
---

# 예외 처리

C++ 예외 처리는 프로그램 실행 중 발생하는 오류나 예외적인 상황을 처리하는 메커니즘입니다. `try`, `catch`, `throw` 키워드를 사용하여 구현됩니다.

*   **`try` 블록**: 예외가 발생할 수 있는 코드를 포함합니다.
*   **`throw` 문**: 예외가 발생했을 때 예외 객체를 던집니다.
*   **`catch` 블록**: `try` 블록에서 던져진 예외를 잡아서 처리합니다.

**기본 구조:**

```cpp
#include <iostream>
#include <string>

double divide(int numerator, int denominator) {
    if (denominator == 0) {
        throw std::string("0으로 나눌 수 없습니다!"); // 예외 발생
    }
    return static_cast<double>(numerator) / denominator;
}

int main() {
    try {
        double result = divide(10, 0); // 예외가 발생할 수 있는 코드
        std::cout << "결과: " << result << std::endl;
    } catch (const std::string& e) { // string 타입의 예외를 잡음
        std::cerr << "예외 발생: " << e << std::endl;
    } catch (...) { // 모든 다른 타입의 예외를 잡음 (catch-all)
        std::cerr << "알 수 없는 예외 발생!" << std::endl;
    }

    std::cout << "프로그램 계속 실행." << std::endl;
    return 0;
}
```

## 예외 계층 구조 (Exception Hierarchy)

C++ 표준 라이브러리는 `std::exception`을 기반으로 하는 예외 클래스 계층 구조를 제공합니다. 이를 사용하면 예외를 더 체계적으로 관리하고 특정 타입의 예외만 처리할 수 있습니다.

```cpp
#include <iostream>
#include <stdexcept> // std::exception, std::runtime_error, std::logic_error 등

void process_data(int value) {
    if (value < 0) {
        throw std::out_of_range("값은 음수가 될 수 없습니다.");
    } else if (value == 0) {
        throw std::invalid_argument("값은 0이 될 수 없습니다.");
    }
    std::cout << "데이터 처리 완료: " << value << std::endl;
}

int main() {
    try {
        process_data(-5);
    } catch (const std::out_of_range& e) {
        std::cerr << "범위 오류: " << e.what() << std::endl;
    } catch (const std::invalid_argument& e) {
        std::cerr << "잘못된 인자: " << e.what() << std::endl;
    } catch (const std::exception& e) { // 모든 표준 예외의 기본 클래스
        std::cerr << "일반 예외: " << e.what() << std::endl;
    } catch (...) { // 모든 다른 예외
        std::cerr << "알 수 없는 예외 발생!" << std::endl;
    }
    return 0;
}
```

## `noexcept` 키워드

`noexcept` 키워드는 C++11에서 도입되었으며, 함수가 예외를 던지지 않음을 컴파일러에게 약속하는 역할을 합니다. `noexcept`로 선언된 함수가 예외를 던지면 프로그램은 즉시 종료됩니다(`std::terminate` 호출).

*   **목적**: 컴파일러가 더 많은 최적화를 수행할 수 있도록 돕고, 함수의 예외 동작에 대한 명확한 인터페이스를 제공합니다.
*   **사용법**: 함수 선언 뒤에 `noexcept`를 붙입니다.

```cpp
#include <iostream>

// 이 함수는 예외를 던지지 않음을 약속합니다.
void safe_function() noexcept {
    std::cout << "이 함수는 안전합니다." << std::endl;
    // throw std::runtime_error("오류!"); // 이 경우 std::terminate 호출
}

// 이 함수는 예외를 던질 수 있습니다.
void unsafe_function() {
    std::cout << "이 함수는 안전하지 않을 수 있습니다." << std::endl;
    throw std::runtime_error("오류 발생!");
}

int main() {
    safe_function();

    try {
        unsafe_function();
    } catch (const std::runtime_error& e) {
        std::cerr << "예외 처리됨: " << e.what() << std::endl;
    }
    return 0;
}
```

## 예외 안전성 (Exception Safety)

예외 안전성은 예외가 발생했을 때 프로그램의 상태가 어떻게 유지되는지를 나타내는 보장 수준입니다. 일반적으로 세 가지 수준의 예외 안전성이 있습니다.

1.  **기본 보장 (Basic Guarantee)**:
    *   예외가 발생해도 프로그램의 모든 불변식(invariants)이 유지됩니다.
    *   자원 누수(memory leak 등)는 발생하지 않습니다.
    *   하지만 객체의 상태는 유효하지만 예측 불가능한 상태가 될 수 있습니다.

2.  **강한 보장 (Strong Guarantee)**:
    *   예외가 발생하면 작업이 완전히 성공하거나, 아니면 작업이 시작되기 전의 원래 상태로 되돌아갑니다 (트랜잭션과 유사).
    *   "커밋 또는 롤백" 의미론을 가집니다.

3.  **예외 없음 보장 (No-Throw Guarantee)**:
    *   함수가 예외를 절대 던지지 않음을 보장합니다. `noexcept` 키워드로 명시할 수 있습니다.
    *   가장 강력한 보장 수준입니다.

예외 안전성을 고려하여 코드를 설계하는 것은 견고하고 신뢰할 수 있는 C++ 애플리케이션을 개발하는 데 중요합니다.

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
