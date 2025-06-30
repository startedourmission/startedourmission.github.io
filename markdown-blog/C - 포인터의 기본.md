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
