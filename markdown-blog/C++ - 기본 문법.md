---
date: 2025-07-01
tags:
  - C++
aliases:
---

# C++ 기본 문법

C++는 C 언어의 확장으로, 절차 지향 프로그래밍의 강력함과 객체 지향 프로그래밍의 유연성을 모두 제공하는 다중 패러다임 언어입니다. 다음은 C++ 프로그래밍의 가장 기본적인 문법 요소들입니다.

## 1. 프로그램 기본 구조

모든 C++ 프로그램은 `main` 함수에서 시작됩니다. 프로그램이 실행될 때 운영체제에 의해 가장 먼저 호출되는 함수입니다.

```cpp
#include <iostream> // 표준 입출력 스트림을 사용하기 위한 헤더 파일 포함

int main() { // 프로그램의 시작점인 main 함수
    // 여기에 프로그램 코드를 작성합니다.
    std::cout << "Hello, C++ World!" << std::endl; // 화면에 "Hello, C++ World!"를 출력
    return 0; // 프로그램이 성공적으로 종료되었음을 운영체제에 알림
}
```

**구조 설명:**

*   **`#include <iostream>`**: 전처리기 지시문으로, 표준 입출력 스트림(`std::cout`, `std::cin` 등)을 사용하기 위해 필요한 헤더 파일입니다.
*   **`int main() { ... }`**: `main` 함수는 C++ 프로그램의 진입점입니다. `int`는 함수가 정수형 값을 반환한다는 것을 의미하고, `()`는 인자를 받지 않음을 나타냅니다.
*   **`std::cout << "..." << std::endl;`**: `std::cout`은 표준 출력 스트림 객체이며, `<<` 연산자를 사용하여 데이터를 출력합니다. `std::endl`은 줄 바꿈과 버퍼 비우기(flush)를 수행합니다.
*   **`return 0;`**: `main` 함수가 성공적으로 실행되었음을 운영체제에 알리는 반환 값입니다. `0`은 성공을 의미합니다.

## 2. 변수와 데이터 타입

변수는 데이터를 저장하는 메모리 공간의 이름입니다. C++는 다양한 종류의 데이터를 저장하기 위한 여러 내장 데이터 타입을 제공합니다.

*   **정수형:** `int`, `short`, `long`, `long long` (크기 및 범위는 시스템에 따라 다를 수 있음)
*   **실수형:** `float`, `double`, `long double` (부동 소수점 숫자)
*   **문자형:** `char` (단일 문자)
*   **논리형:** `bool` (`true` 또는 `false` 값)
*   **문자열:** `std::string` (가변 길이 문자열, `<string>` 헤더 필요)

```cpp
#include <iostream>
#include <string> // std::string 사용을 위해

int main() {
    int age = 30; // 정수형 변수 선언 및 초기화
    double pi = 3.14159; // 실수형 변수
    char initial = 'J'; // 문자형 변수
    bool is_active = true; // 논리형 변수
    std::string name = "Alice"; // 문자열 변수

    std::cout << "이름: " << name << std::endl;
    std::cout << "나이: " << age << std::endl;
    std::cout << "원주율: " << pi << std::endl;
    std::cout << "이니셜: " << initial << std::endl;
    std::cout << "활성화 여부: " << is_active << std::endl; // true는 1, false는 0으로 출력될 수 있음

    age = 31; // 변수 값 변경
    std::cout << "변경된 나이: " << age << std::endl;

    return 0;
}
```

## 3. 입출력 (Input/Output)

C++에서는 `iostream` 라이브러리의 `std::cin`과 `std::cout` 객체를 사용하여 표준 입출력을 수행합니다.

*   **`std::cout`**: 데이터를 화면에 출력할 때 사용합니다. `<<` (삽입 연산자)를 사용합니다.
*   **`std::cin`**: 사용자로부터 데이터를 입력받을 때 사용합니다. `>>` (추출 연산자)를 사용합니다.

```cpp
#include <iostream>
#include <string>

int main() {
    std::string user_name;
    int user_age;

    std::cout << "이름을 입력하세요: ";
    std::cin >> user_name; // 사용자로부터 이름 입력

    std::cout << "나이를 입력하세요: ";
    std::cin >> user_age; // 사용자로부터 나이 입력

    std::cout << "안녕하세요, " << user_name << "님! "
              << user_age << "살이시군요." << std::endl;

    return 0;
}
```

## 4. 연산자 (Operators)

C++는 다양한 연산자를 제공하여 변수와 값에 대한 연산을 수행합니다.

*   **산술 연산자:** `+` (덧셈), `-` (뺄셈), `*` (곱셈), `/` (나눗셈), `%` (나머지)
*   **관계 연산자:** `==` (같다), `!=` (같지 않다), `<` (작다), `>` (크다), `<=` (작거나 같다), `>=` (크거나 같다)
*   **논리 연산자:** `&&` (AND), `||` (OR), `!` (NOT)
*   **대입 연산자:** `=` (대입), `+=`, `-=`, `*=` 등 (복합 대입)
*   **증감 연산자:** `++` (증가), `--` (감소)

```cpp
#include <iostream>

int main() {
    int a = 10;
    int b = 3;

    std::cout << "a + b = " << (a + b) << std::endl; // 13
    std::cout << "a / b = " << (a / b) << std::endl; // 3 (정수 나눗셈)
    std::cout << "a % b = " << (a % b) << std::endl; // 1

    bool cond1 = (a > b); // true
    bool cond2 = (a == 10 && b < 5); // true

    std::cout << "a > b: " << cond1 << std::endl;
    std::cout << "a == 10 && b < 5: " << cond2 << std::endl;

    a++; // a는 11이 됨
    std::cout << "a++: " << a << std::endl;

    return 0;
}
```

## 5. 조건문 (Conditional Statements)

특정 조건에 따라 코드 블록을 실행하거나 건너뛸 때 사용됩니다. `if`, `else if`, `else`, `switch` 문이 있습니다.

*   **`if` 문:** 조건이 참일 때 코드 실행
*   **`if-else` 문:** 조건이 참일 때 `if` 블록, 거짓일 때 `else` 블록 실행
*   **`if-else if-else` 문:** 여러 조건을 순차적으로 검사
*   **`switch` 문:** 하나의 변수 값에 따라 여러 경우 중 하나를 선택하여 실행

```cpp
#include <iostream>

int main() {
    int score = 85;

    if (score >= 90) {
        std::cout << "학점: A" << std::endl;
    } else if (score >= 80) {
        std::cout << "학점: B" << std::endl;
    } else {
        std::cout << "학점: C 이하" << std::endl;
    }

    int day = 3;
    switch (day) {
        case 1:
            std::cout << "월요일" << std::endl;
            break;
        case 2:
            std::cout << "화요일" << std::endl;
            break;
        default:
            std::cout << "그 외 요일" << std::endl;
            break;
    }

    return 0;
}
```

## 6. 반복문 (Loops)

특정 코드 블록을 반복적으로 실행할 때 사용됩니다. `for`, `while`, `do-while` 루프가 있습니다.

*   **`for` 루프:** 정해진 횟수만큼 반복하거나, 초기화, 조건, 증감식이 명확할 때 사용
*   **`while` 루프:** 조건이 참인 동안 반복
*   **`do-while` 루프:** 최소 한 번은 실행하고 조건을 검사

```cpp
#include <iostream>

int main() {
    // for 루프
    for (int i = 0; i < 3; ++i) {
        std::cout << "for 루프: " << i << std::endl;
    }

    // while 루프
    int count = 0;
    while (count < 3) {
        std::cout << "while 루프: " << count << std::endl;
        count++;
    }

    // do-while 루프
    int j = 0;
    do {
        std::cout << "do-while 루프: " << j << std::endl;
        j++;
    } while (j < 3);

    return 0;
}
```

## 7. 함수 (Functions)

코드의 재사용성을 높이고 프로그램을 모듈화하는 데 사용됩니다. 특정 작업을 수행하는 코드 블록을 정의합니다.

```cpp
#include <iostream>

// 함수 선언 (프로토타입)
int add(int x, int y);

// 함수 정의
int add(int x, int y) {
    return x + y;
}

void greet(const std::string& name) {
    std::cout << "Hello, " << name << "!" << std::endl;
}

int main() {
    int result = add(5, 3); // 함수 호출
    std::cout << "5 + 3 = " << result << std::endl;

    greet("World");
    return 0;
}
```

## 8. 주석 (Comments)

코드에 설명을 추가하여 가독성을 높입니다. 컴파일러는 주석을 무시합니다.

*   **한 줄 주석:** `//`로 시작
*   **여러 줄 주석:** `/*`로 시작하여 `*/`로 끝남

```cpp
// 이것은 한 줄 주석입니다.

/*
이것은 여러 줄 주석입니다.
여러 줄에 걸쳐 설명을 작성할 수 있습니다.
*/
int main() {
    int x = 10; // 변수 x를 선언하고 10으로 초기화
    return 0;
}
```

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
