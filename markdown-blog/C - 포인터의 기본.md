---
date: 2025-06-30
tags:
  - C
aliases:
---

# 포인터의 기본

C 언어에서 포인터는 메모리 주소를 저장하는 변수입니다. 다른 변수의 메모리 위치를 가리키는 데 사용됩니다.

**포인터의 기본 개념:**

1.  **선언 (Declaration):**
    포인터 변수를 선언할 때는 `*` 기호를 사용하여 해당 변수가 포인터임을 나타냅니다.
    ```c
    int *ptr; // int형 변수의 주소를 저장할 포인터 ptr 선언
    char *c_ptr; // char형 변수의 주소를 저장할 포인터 c_ptr 선언
    ```

2.  **주소 연산자 (`&`):**
    변수의 메모리 주소를 얻기 위해 사용됩니다.
    ```c
    int num = 10;
    int *ptr = &num; // num 변수의 주소를 ptr에 저장
    ```

3.  **역참조 연산자 (`*`):**
    포인터가 가리키는 메모리 주소에 저장된 값을 가져올 때 사용됩니다.
    ```c
    int num = 10;
    int *ptr = &num;
    printf("%d\n", *ptr); // ptr이 가리키는 값 (num의 값, 즉 10) 출력
    ```

**예제:**

```c
#include <stdio.h>

int main() {
    int num = 100;
    double pi = 3.14;

    // 포인터 선언 및 초기화
    int *ptr_num = &num;
    double *ptr_pi = &pi;

    printf("num의 값: %d\n", num);
    printf("num의 주소: %p\n", &num);
    printf("ptr_num이 가리키는 값: %d\n", *ptr_num);
    printf("ptr_num의 값 (num의 주소): %p\n", ptr_num);
    printf("ptr_num 자체의 주소: %p\n", &ptr_num);

    printf("\n");

    printf("pi의 값: %.2f\n", pi);
    printf("pi의 주소: %p\n", &pi);
    printf("ptr_pi가 가리키는 값: %.2f\n", *ptr_pi);
    printf("ptr_pi의 값 (pi의 주소): %p\n", ptr_pi);
    printf("ptr_pi 자체의 주소: %p\n", &ptr_pi);

    // 포인터를 사용하여 값 변경
    *ptr_num = 200;
    printf("\n*ptr_num = 200 후 num의 값: %d\n", num);

    return 0;
}
```

이 예제는 포인터가 변수의 주소를 저장하고, 역참조 연산자를 통해 해당 주소의 값을 읽거나 변경할 수 있음을 보여줍니다.

## 포인터 산술 (Pointer Arithmetic)

포인터는 정수형 값처럼 덧셈, 뺄셈 연산을 수행할 수 있습니다. 하지만 일반적인 정수 연산과는 다르게, 포인터의 자료형 크기만큼 주소 값이 증감합니다.

*   **덧셈 (`+`)**: 포인터에 정수를 더하면, 포인터가 가리키는 자료형의 크기만큼 주소 값이 증가합니다.
*   **뺄셈 (`-`)**: 포인터에서 정수를 빼면, 포인터가 가리키는 자료형의 크기만큼 주소 값이 감소합니다.
*   **포인터 간의 뺄셈**: 동일한 자료형을 가리키는 두 포인터의 뺄셈은 두 주소 사이의 요소 개수를 반환합니다.

```c
#include <stdio.h>

int main() {
    int arr[5] = {10, 20, 30, 40, 50};
    int *ptr = arr; // ptr은 arr[0]을 가리킴

    printf("ptr의 초기 주소: %p\n", (void*)ptr);
    printf("ptr이 가리키는 값: %d\n", *ptr); // 10

    ptr++; // ptr은 이제 arr[1]을 가리킴 (int 크기만큼 증가)
    printf("ptr++ 후 주소: %p\n", (void*)ptr);
    printf("ptr이 가리키는 값: %d\n", *ptr); // 20

    ptr = ptr + 2; // ptr은 이제 arr[3]을 가리킴 (int 크기 * 2 만큼 증가)
    printf("ptr + 2 후 주소: %p\n", (void*)ptr);
    printf("ptr이 가리키는 값: %d\n", *ptr); // 40

    int *ptr2 = &arr[4];
    printf("ptr2의 주소: %p\n", (void*)ptr2);
    printf("ptr2가 가리키는 값: %d\n", *ptr2); // 50

    // 두 포인터 간의 뺄셈
    printf("ptr2 - ptr: %td\n", ptr2 - ptr); // 1 (arr[4] - arr[3])

    return 0;
}
```

## `void` 포인터 (Generic Pointer)

`void` 포인터는 특정 자료형을 가리키지 않는 일반(generic) 포인터입니다. 어떤 자료형의 주소든 저장할 수 있지만, 역참조하여 값을 직접 읽거나 포인터 산술 연산을 수행하려면 반드시 특정 자료형으로 형 변환(type casting)해야 합니다.

```c
#include <stdio.h>

int main() {
    int num = 10;
    float pi = 3.14f;
    void *generic_ptr;

    generic_ptr = &num; // int 변수의 주소 저장
    printf("void 포인터가 가리키는 int 값: %d\n", *(int*)generic_ptr); // int*로 형 변환 후 역참조

    generic_ptr = &pi; // float 변수의 주소 저장
    printf("void 포인터가 가리키는 float 값: %.2f\n", *(float*)generic_ptr); // float*로 형 변환 후 역참조

    // void 포인터는 직접 산술 연산 불가 (C 표준)
    // generic_ptr++; // 컴파일 오류 발생

    return 0;
}
```

---
 기본 문법
 - [[C - 개요]]
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