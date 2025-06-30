---
date: 2025-07-01
tags:
  - C
aliases:
---

# 자료형 (Data Types)

C 언어에서 자료형은 변수가 저장할 데이터의 종류와 크기를 정의합니다. 각 자료형은 메모리에서 차지하는 공간과 표현할 수 있는 값의 범위가 다릅니다.

C 언어의 주요 자료형은 다음과 같이 분류할 수 있습니다:

## 1. 기본 자료형 (Primitive Data Types)
가장 기본적인 자료형으로, 정수, 실수, 문자를 표현합니다.

*   **정수형 (Integer Types)**: 소수점 없는 숫자를 저장합니다.
    *   `int`: 가장 기본적인 정수형입니다. 일반적으로 2 또는 4바이트를 차지하며, 시스템에 따라 크기가 달라질 수 있습니다.
        *   `short` 또는 `short int`: `int`보다 작거나 같은 크기를 가집니다. 보통 2바이트입니다.
        *   `long` 또는 `long int`: `int`보다 크거나 같은 크기를 가집니다. 보통 4바이트 또는 8바이트입니다.
        *   `long long` 또는 `long long int`: C99 표준에서 추가되었으며, 최소 8바이트를 보장합니다.
    *   **수식어 (Modifiers)**: 정수형 자료형과 함께 사용하여 값의 범위를 조절합니다.
        *   `signed`: 양수와 음수를 모두 표현합니다. (기본값)
        *   `unsigned`: 0을 포함한 양수만 표현합니다.

*   **문자형 (Character Type)**: 단일 문자를 저장합니다.
    *   `char`: 1바이트를 차지하며, ASCII 코드 값을 저장합니다.
        *   `signed char`: -128에서 127까지의 값을 표현합니다.
        *   `unsigned char`: 0에서 255까지의 값을 표현합니다.

*   **실수형 (Floating-Point Types)**: 소수점 있는 숫자를 저장합니다.
    *   `float`: 단정밀도 부동소수점 숫자를 저장합니다. 일반적으로 4바이트를 차지하며, 약 6-7자리의 정밀도를 가집니다.
    *   `double`: 배정밀도 부동소수점 숫자를 저장합니다. 일반적으로 8바이트를 차지하며, 약 15자리의 정밀도를 가집니다.
    *   `long double`: `double`보다 크거나 같은 정밀도를 가집니다.

*   **논리형 (Boolean Type)**: C99 표준에서 `_Bool` 타입이 추가되었습니다. `true` 또는 `false` 값을 가집니다. (C 언어는 별도의 논리값 자료형이 없으며, 정수값으로 표현하기도 합니다.)

*   **`void` 타입**: 값이 없음을 나타내는 자료형입니다. 주로 함수에서 반환 값이 없거나, 어떤 타입이든 가리킬 수 있는 포인터(`void *`)에 사용됩니다.

## 2. 파생 자료형 (Derived Data Types)
기본 자료형을 기반으로 만들어진 자료형입니다.
*   배열 (Arrays)
*   포인터 (Pointers)
*   함수 (Functions)

## 3. 사용자 정의 자료형 (User-Defined Data Types)
프로그래머가 직접 정의하여 사용하는 자료형입니다.
*   구조체 (Structures)
*   공용체 (Unions)
*   열거형 (Enumerations)

**자료형의 크기 확인**
각 자료형의 정확한 크기는 시스템 및 컴파일러에 따라 다를 수 있습니다. `sizeof` 연산자를 사용하여 특정 자료형이나 변수의 메모리 크기(바이트 단위)를 확인할 수 있습니다.

예시:
```c
#include <stdio.h>

int main() {
    printf("Size of char: %zu bytes\n", sizeof(char));
    printf("Size of int: %zu bytes\n", sizeof(int));
    printf("Size of float: %zu bytes\n", sizeof(float));
    printf("Size of double: %zu bytes\n", sizeof(double));
    printf("Size of long double: %zu bytes\n", sizeof(long double));
    printf("Size of short: %zu bytes\n", sizeof(short));
    printf("Size of long: %zu bytes\n", sizeof(long));
    printf("Size of long long: %zu bytes\n", sizeof(long long));
    return 0;
}
```

---
 기본 문법
 - [[C - 개요]]
 - [[C - 변수]]
 - [[C - 조건문]]
 - [[C - 반복문]]
 - [[C - 함수]]

심화 문법
 - [[C - 구조체]]
 - [[C - 공용체]]
 - [[C - 열거형]]
 - [[C - 전처리기]]

 포인터
 - [[C - 포인터의 기본]]
 - [[C - 배열과 포인터]]
 - [[C - 함수 포인터]]
 - [[C - 구조체 포인터]]

 기타
 - [[C - 헤더 파일]]
 - [[C - 현대 C 언어와 C23 표준]]
 - [[C - 실무에서 사용하는 C 언어의 변형]]
