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

## 함수 포인터 배열 (Array of Function Pointers)

함수 포인터의 배열을 사용하여 여러 함수를 하나의 배열로 관리하고, 인덱스를 통해 원하는 함수를 호출할 수 있습니다. 이는 조건문(`if-else if`)을 대체하여 코드를 간결하게 만들 수 있습니다.

```c
#include <stdio.h>

int add(int a, int b) { return a + b; }
int subtract(int a, int b) { return a - b; }
int multiply(int a, int b) { return a * b; }
int divide(int a, int b) { return a / b; }

int main() {
    // int를 반환하고 int 두 개를 매개변수로 받는 함수 포인터 배열 선언
    int (*operations[4])(int, int) = {add, subtract, multiply, divide};

    int x = 10, y = 5;
    int choice;

    printf("연산을 선택하세요 (0:덧셈, 1:뺄셈, 2:곱셈, 3:나눗셈): ");
    scanf("%d", &choice);

    if (choice >= 0 && choice < 4) {
        printf("결과: %d\n", operations[choice](x, y));
    } else {
        printf("잘못된 선택입니다.\n");
    }

    return 0;
}
```

## 콜백 함수 예시 (Callback Function Example)

콜백 함수는 다른 함수의 인자로 전달되어, 특정 이벤트가 발생하거나 특정 시점에 호출되는 함수입니다. `qsort` 함수가 대표적인 예시입니다.

```c
#include <stdio.h>
#include <stdlib.h> // qsort 사용을 위해

// qsort에 전달할 비교 함수
// 두 포인터가 가리키는 int 값을 비교하여 정렬 순서를 결정
int compare_integers(const void *a, const void *b) {
    int arg1 = *(const int *)a;
    int arg2 = *(const int *)b;

    if (arg1 < arg2) return -1;
    if (arg1 > arg2) return 1;
    return 0;
}

int main() {
    int numbers[] = {5, 2, 8, 1, 9, 4, 7, 3, 6};
    int n = sizeof(numbers) / sizeof(numbers[0]);

    printf("정렬 전: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n");

    // qsort 함수 호출: 배열, 요소 개수, 요소 크기, 비교 함수 포인터
    qsort(numbers, n, sizeof(int), compare_integers);

    printf("정렬 후: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n");

    return 0;
}
```

---
 기본 문법
 - [[C - 구조]]
 - [[C - 자료형]]
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
 - [[C - 컴파일과 링크]]
 - [[C - IDE]]
 - [[C - 헤더 파일]]
 - [[C - 현대 C 언어와 C23 표준]]
 - [[C - 실무에서 사용하는 C 언어의 변형]]

```