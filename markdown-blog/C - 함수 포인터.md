---
date: 2025-06-30
tags:
  - C
aliases:
---

# 함수 포인터

C 언어에서 함수 포인터는 함수의 메모리 주소를 가리키는 포인터 변수입니다. 이를 통해 함수를 다른 함수의 인자로 전달하거나, 배열에 저장하거나, 동적으로 호출하는 등의 작업을 수행할 수 있습니다.

**1. 함수 포인터 선언 문법:**

```c
반환타입 (*포인터이름)(매개변수1_타입, 매개변수2_타입, ...);
```

*   `반환타입`: 포인터가 가리킬 함수의 반환 타입입니다.
*   `(*포인터이름)`: 괄호 `()` 안에 포인터 이름을 넣고 앞에 `*`를 붙여 함수 포인터임을 명시합니다. (괄호가 없으면 함수가 포인터를 반환하는 것으로 해석됩니다.)
*   `(매개변수1_타입, ...)`: 포인터가 가리킬 함수의 매개변수 타입 목록입니다.

**예시:**

```c
int (*func_ptr)(int, int); // int를 반환하고 int 두 개를 매개변수로 받는 함수를 가리키는 포인터
void (*print_msg)(char*); // void를 반환하고 char*를 매개변수로 받는 함수를 가리키는 포인터
```

**2. 함수 포인터 사용 예시:**

```c
#include <stdio.h>

// 두 정수를 더하는 함수
int add(int a, int b) {
    return a + b;
}

// 두 정수를 빼는 함수
int subtract(int a, int b) {
    return a - b;
}

// 메시지를 출력하는 함수
void print_message(char* msg) {
    printf("Message: %s\n", msg);
}

int main() {
    // 1. 함수 포인터 선언 및 초기화
    int (*operation)(int, int); // int를 반환하고 int 두 개를 매개변수로 받는 함수 포인터 선언
    void (*message_printer)(char*); // void를 반환하고 char*를 매개변수로 받는 함수 포인터 선언

    // 2. 함수 포인터에 함수의 주소 할당
    // 함수 이름 자체가 함수의 주소를 나타냅니다. & 연산자를 사용해도 됩니다.
    operation = add;
    // operation = &add; // 이렇게 사용해도 동일합니다.

    message_printer = print_message;

    // 3. 함수 포인터를 사용하여 함수 호출
    int result_add = operation(10, 5); // add 함수 호출
    printf("Addition result: %d\n", result_add); // 출력: Addition result: 15

    operation = subtract; // subtract 함수로 포인터 변경
    int result_sub = operation(10, 5); // subtract 함수 호출
    printf("Subtraction result: %d\n", result_sub); // 출력: Subtraction result: 5

    message_printer("Hello, Function Pointers!"); // print_message 함수 호출

    return 0;
}
```

**3. 주요 사용 사례:**

*   **콜백 함수 (Callback Functions):** 특정 이벤트가 발생했을 때 호출될 함수를 미리 등록하는 데 사용됩니다. (예: `qsort` 함수의 비교 함수)
*   **점프 테이블 (Jump Tables):** 여러 함수 중 하나를 조건에 따라 동적으로 호출해야 할 때, 함수 포인터 배열을 사용하여 효율적으로 구현할 수 있습니다.
*   **상태 머신 (State Machines):** 각 상태에 해당하는 함수를 함수 포인터로 관리하여 상태 전환 로직을 구현할 수 있습니다.
