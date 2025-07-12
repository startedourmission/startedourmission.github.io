---
date: 2025-06-30
tags:
  - C
aliases:
---
전처리기(Preprocessor)는 컴파일러가 소스 코드를 실제 컴파일하기 전에 소스 코드를 변환하는 역할을 하는 프로그램입니다. 전처리기는 `#` 기호로 시작하는 **전처리기 지시문**이라는 특별한 명령어를 처리합니다.

## 1. 헤더 파일 포함 (`#include`)

다른 파일(주로 `.h` 확장자를 가진 헤더 파일)의 내용을 현재 소스 파일에 삽입합니다. 이를 통해 함수 선언, 매크로 정의 등을 여러 파일에서 공유할 수 있습니다.

*   `#include <stdio.h>`: 표준 라이브러리 헤더 파일을 포함할 때 사용합니다. `< >`는 컴파일러가 표준 경로에서 헤더 파일을 찾도록 지시합니다.

*   `#include "myheader.h"`: 사용자가 정의한 헤더 파일을 포함할 때 사용합니다. `""`는 컴파일러가 현재 디렉토리 또는 지정된 경로에서 헤더 파일을 찾도록 지시합니다.

```c
// myheader.h 파일 내용
#ifndef MY_HEADER_H
#define MY_HEADER_H

#define MAX_VALUE 100
int add(int a, int b);

#endif

// main.c 파일 내용
#include <stdio.h>
#include "myheader.h"

int add(int a, int b) {
    return a + b;
}

int main() {
    printf("MAX_VALUE: %d\n", MAX_VALUE);
    printf("Sum: %d\n", add(10, 20));
    return 0;
}
```

## 2. 매크로 확장 (`#define`, `#undef`)

코드 내에서 특정 값이나 코드 조각을 나타내는 매크로를 정의하고 확장합니다. `#define`으로 정의된 매크로는 컴파일 전에 해당 값이나 코드로 대체됩니다. `#undef`는 정의된 매크로를 해제합니다.

*   **객체형 매크로 (Object-like Macro):** 상수를 정의할 때 주로 사용됩니다.
    ```c
    #define PI 3.141592
    #define MESSAGE "Hello, Macros!"
    ```
*   **함수형 매크로 (Function-like Macro):** 함수처럼 인자를 받아 처리하는 매크로입니다. 인자 주위에 괄호를 사용하여 예상치 못한 부작용을 방지하는 것이 중요합니다.
    ```c
    #define SQUARE(x) ((x) * (x))
    #define MAX(a, b) ((a) > (b) ? (a) : (b))
    ```

```c
#include <stdio.h>

#define PI 3.141592
#define SQUARE(x) ((x) * (x))

int main() {
    printf("PI: %f\n", PI);
    printf("SQUARE(5): %d\n", SQUARE(5));
    printf("SQUARE(2 + 3): %d\n", SQUARE(2 + 3)); // (2 + 3) * (2 + 3) = 25

    #undef PI // PI 매크로 정의 해제
    // printf("PI: %f\n", PI); // 에러 발생: PI가 정의되지 않음

    return 0;
}
```

## 3. 조건부 컴파일 (`#if`, `#ifdef`, `#ifndef`, `#else`, `#elif`, `#endif`)

특정 조건에 따라 코드의 일부를 컴파일에 포함하거나 제외할 수 있습니다. 이는 디버깅, 플랫폼별 코드 작성 또는 프로그램의 다른 버전을 생성하는 데 유용합니다.

*   `#ifdef 매크로이름`: `매크로이름`이 정의되어 있으면 참.
*   `#ifndef 매크로이름`: `매크로이름`이 정의되어 있지 않으면 참.
*   `#if 상수_표현식`: `상수_표현식`이 0이 아니면 참.
*   `#else`: 이전 `#if`, `#ifdef`, `#ifndef` 조건이 거짓일 때 실행.
*   `#elif 상수_표현식`: 이전 조건이 거짓이고 현재 `상수_표현식`이 참일 때 실행.
*   `#endif`: 조건부 컴파일 블록의 끝.

```c
#include <stdio.h>

#define DEBUG
#define OS_WINDOWS

int main() {
    #ifdef DEBUG
        printf("디버그 모드입니다.\n");
    #endif

    #ifndef RELEASE
        printf("릴리즈 모드가 아닙니다.\n");
    #endif

    #if __STDC_VERSION__ >= 201112L // C11 표준 이상
        printf("C11 표준 이상을 사용 중입니다.\n");
    #elif __STDC_VERSION__ >= 199901L // C99 표준 이상
        printf("C99 표준 이상을 사용 중입니다.\n");
    #else
        printf("구형 C 표준을 사용 중입니다.\n");
    #endif

    #ifdef OS_WINDOWS
        printf("운영체제: Windows\n");
    #elif defined(OS_LINUX)
        printf("운영체제: Linux\n");
    #else
        printf("알 수 없는 운영체제\n");
    #endif

    return 0;
}
```

## 4. 기타 지시문

*   `#line`: 컴파일러에게 현재 파일 이름과 줄 번호를 변경하도록 지시합니다. 주로 디버깅이나 오류 메시지 추적에 사용됩니다.
*   `#error`: 컴파일 시 오류 메시지를 출력하고 컴파일을 중단합니다. 특정 조건이 충족되지 않을 때 컴파일을 막는 데 사용됩니다.
    ```c
    #if !defined(MY_MACRO)
    #error "MY_MACRO가 정의되지 않았습니다!"
    #endif
    ```
*   `#pragma`: 컴파일러에 특정 지시를 내립니다. 컴파일러마다 지원하는 `pragma`가 다를 수 있습니다.
    ```c
    #pragma once // 헤더 파일 중복 포함 방지 (비표준이지만 널리 사용됨)
    #pragma warning(disable: 4996) // 특정 경고 비활성화 (MSVC)
    ```

## 전처리기 사용 시 주의사항

*   **매크로의 부작용 (Side Effects):** 함수형 매크로의 인자에 부작용이 있는 표현식(예: `x++`)을 사용하면 예상치 못한 결과가 발생할 수 있습니다. 매크로 인자 주위에 항상 괄호를 사용하는 것이 중요합니다.
    ```c
    #define SQUARE(x) (x * x) // 잘못된 예시
    // int a = 5;
    // int result = SQUARE(a++); // (a++ * a++) -> 5 * 6 = 30 (예상치 못한 결과)

    #define SQUARE_SAFE(x) ((x) * (x)) // 올바른 예시
    // int a = 5;
    // int result = SQUARE_SAFE(a++); // ((a++) * (a++)) -> (5) * (6) = 30 (여전히 부작용 발생 가능)
    // 가장 안전한 방법은 매크로 대신 인라인 함수나 일반 함수를 사용하는 것입니다.
    ```

  - **매크로의 타입 안전성 부족:** 매크로는 타입 검사를 수행하지 않으므로, 잘못된 타입의 인자가 전달되어도 컴파일러가 오류를 감지하기 어렵습니다.
  - **디버깅의 어려움:** 전처리된 코드는 원본 코드와 다를 수 있어 디버깅이 어려울 수 있습니다.
  - **매크로 남용 피하기:** 복잡한 로직이나 여러 줄의 코드를 매크로로 정의하는 것은 피해야 합니다. 가독성을 해치고 디버깅을 어렵게 만듭니다. 간단한 상수나 짧은 코드 조각에만 사용하는 것이 좋습니다.

전처리는 컴파일 과정의 첫 번째 단계로, 소스 코드를 수정하여 컴파일러가 처리할 최종 코드를 생성합니다.
