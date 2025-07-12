---
date: 2025-06-30
tags:
  - C
aliases:
---
함수(Function)는 특정 작업을 수행하는 코드 블록입니다. 프로그램을 더 작은 프로그램을 쪼개 관리가 용이한 코드로 만드는데 사용합니다.

*   **재사용성**: 한 번 정의된 함수는 프로그램의 여러 곳에서 호출될 수 있습니다.
*   **모듈화**: 복잡한 프로그램을 논리적인 단위로 분할하여 코드의 가독성과 유지보수성을 높입니다.
*   **입력 및 출력**: 함수는 인수를 통해 데이터를 입력받을 수 있으며, 반환 값을 통해 결과를 출력할 수 있습니다.

기본적인 함수 선언 및 정의 구조는 다음과 같습니다

```c
// 함수 선언 (프로토타입)
return_type function_name(parameter_list);

// 함수 정의
return_type function_name(parameter_list) {
    // 함수 본문
    // 작업 수행
    return return_value;
}
```

예시

```c
#include <stdio.h>

// 함수 선언
int add(int a, int b);

int main() {
    int result;
    result = add(5, 3); // 함수 호출
    printf("Result: %d\n", result); // 출력: Result: 8
    return 0;
}

// 함수 정의
int add(int a, int b) {
    return a + b;
}
```

## 함수 호출 방식

C 언어에서 함수에 인자를 전달하는 방식은 크게 두 가지가 있습니다.

### 1. 값에 의한 호출 (Call by Value)

*   함수를 호출할 때 인자의 **값**을 복사하여 전달합니다.
*   함수 내부에서 매개변수의 값을 변경해도 원본 변수의 값은 변경되지 않습니다.
*   대부분의 기본 자료형(int, float, char 등)은 값에 의한 호출 방식으로 전달됩니다.

```c
#include <stdio.h>

void increment(int num) {
    num = num + 1;
    printf("함수 내부: num = %d\n", num); // 11
}

int main() {
    int value = 10;
    increment(value);
    printf("함수 호출 후: value = %d\n", value); // 10 (변경 없음)
    return 0;
}
```

### 2. 주소에 의한 호출 (Call by Reference / Call by Address)

*   함수를 호출할 때 인자의 **메모리 주소**를 전달합니다. 포인터를 사용합니다.
*   함수 내부에서 포인터를 통해 해당 주소의 값을 변경하면 원본 변수의 값도 변경됩니다.
*   배열이나 구조체와 같이 큰 데이터를 전달할 때 효율적이며, 함수 내에서 원본 값을 변경해야 할 때 사용됩니다.

```c
#include <stdio.h>

void increment_by_address(int *num_ptr) {
    *num_ptr = *num_ptr + 1;
    printf("함수 내부: *num_ptr = %d\n", *num_ptr); // 11
}

int main() {
    int value = 10;
    increment_by_address(&value); // value의 주소 전달
    printf("함수 호출 후: value = %d\n", value); // 11 (변경됨)
    return 0;
}
```

## 재귀 함수 (Recursive Function)

재귀 함수는 함수가 자기 자신을 호출하여 문제를 해결하는 방식의 함수입니다. 특정 조건을 만족할 때까지 반복적으로 자신을 호출하며, 종료 조건(base case)이 반드시 필요합니다.

```c
#include <stdio.h>

// 팩토리얼 계산 함수 (재귀)
int factorial(int n) {
    if (n == 0) { // 종료 조건
        return 1;
    } else {
        return n * factorial(n - 1); // 재귀 호출
    }
}

int main() {
    int num = 5;
    printf("%d의 팩토리얼: %d\n", num, factorial(num)); // 출력: 5의 팩토리얼: 120
    return 0;
}
```

## 함수 포인터 (Function Pointer)

함수 포인터는 함수의 메모리 주소를 저장하는 포인터 변수입니다. 이를 통해 함수를 다른 함수의 인자로 전달하거나, 배열에 저장하거나, 동적으로 호출하는 등의 작업을 수행할 수 있습니다. 자세한 내용은 [[C - 함수 포인터]] 노트를 참조하세요.