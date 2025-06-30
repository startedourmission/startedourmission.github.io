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