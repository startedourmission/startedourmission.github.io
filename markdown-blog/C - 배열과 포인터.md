---
date: 2025-04-18
tags:
  - C
aliases:
---

# 배열과 포인터

C 언어에서 배열과 포인터는 매우 밀접하게 관련되어 있으며, 포인터를 사용하여 배열 요소를 효율적으로 조작할 수 있습니다.

## 배열 이름과 포인터
*   배열 이름은 배열의 첫 번째 요소의 주소를 나타냅니다. 예를 들어, `int arr[5];`라고 선언하면 `arr`는 `arr[0]`의 주소를 가리킵니다.
*   따라서 `arr`와 `&arr[0]`는 동일한 값을 가집니다.
*   배열 이름은 상수 포인터이므로, `arr = arr + 1;`과 같이 값을 변경할 수 없습니다.

## 포인터를 이용한 배열 요소 접근

*   포인터 변수를 사용하여 배열 요소를 접근할 수 있습니다.
*   `int *ptr = arr;` 또는 `int *ptr = &arr[0];`와 같이 배열의 첫 번째 요소 주소를 포인터에 할당할 수 있습니다.
*   `ptr[i]`는 `*(ptr + i)`와 동일하며, 이는 `arr[i]`와 동일하게 배열의 `i`번째 요소에 접근합니다.

## 배열 이름과 포인터 변수의 차이점

*   **할당 가능성**: 배열 이름은 상수 포인터이므로 다른 주소를 할당할 수 없습니다. 반면, 포인터 변수는 다른 주소를 할당할 수 있습니다.
*   **`sizeof` 연산**: `sizeof(배열_이름)`은 배열 전체의 크기(바이트)를 반환합니다. `sizeof(포인터_변수)`는 포인터 변수 자체의 크기(일반적으로 4 또는 8바이트)를 반환합니다.

### 예시

```c
#include <stdio.h>

int main() {
    int arr[5] = {10, 20, 30, 40, 50};
    int *ptr;

    // 배열 이름은 첫 번째 요소의 주소와 같습니다.
    printf("arr의 주소: %p\n", (void*)arr);
    printf("arr[0]의 주소: %p\n", (void*)&arr[0]);

    // 포인터에 배열의 주소를 할당
    ptr = arr; // 또는 ptr = &arr[0];

    // 포인터를 이용한 배열 요소 접근
    printf("ptr[0]의 값: %d\n", ptr[0]); // 10
    printf("*(ptr + 1)의 값: %d\n", *(ptr + 1)); // 20

    // 포인터 증감
    ptr++; // ptr은 이제 arr[1]을 가리킵니다.
    printf("ptr이 가리키는 값 (증가 후): %d\n", *ptr); // 20

    // sizeof 연산의 차이
    printf("sizeof(arr): %zu 바이트\n", sizeof(arr)); // 배열 전체 크기 (5 * 4 = 20 바이트)
    printf("sizeof(ptr): %zu 바이트\n", sizeof(ptr)); // 포인터 변수 크기 (예: 8 바이트)

    return 0;
}
```

## 다차원 배열과 포인터

다차원 배열은 메모리상에 연속적으로 저장됩니다. 2차원 배열의 경우, 배열 이름은 첫 번째 행의 주소를 가리키는 포인터로 해석될 수 있습니다. 각 행은 다시 첫 번째 요소의 주소를 가리키는 포인터로 해석됩니다.

```c
#include <stdio.h>

int main() {
    int matrix[2][3] = {{1, 2, 3}, {4, 5, 6}};

    // matrix는 첫 번째 행의 주소 (int (*)[3] 타입)
    printf("matrix: %p\n", (void*)matrix);
    printf("matrix[0]: %p\n", (void*)matrix[0]);
    printf("&matrix[0][0]: %p\n", (void*)&matrix[0][0]);

    // 포인터를 이용한 접근
    printf("matrix[0][0]: %d\n", **matrix); // 1
    printf("matrix[0][1]: %d\n", *(*matrix + 1)); // 2
    printf("matrix[1][0]: %d\n", *(*(matrix + 1))); // 4
    printf("matrix[1][2]: %d\n", *(*(matrix + 1) + 2)); // 6

    return 0;
}
```

## 동적 할당된 배열과 포인터

`malloc` 함수를 사용하여 힙(heap) 영역에 동적으로 배열을 할당할 수 있습니다. 이 경우 `malloc`은 할당된 메모리 블록의 시작 주소를 반환하며, 이 주소를 포인터 변수에 저장하여 배열처럼 사용할 수 있습니다.

```c
#include <stdio.h>
#include <stdlib.h> // malloc, free 사용을 위해

int main() {
    int *arr_ptr;
    int size = 5;

    // int형 요소 5개를 저장할 메모리 동적 할당
    arr_ptr = (int *)malloc(size * sizeof(int));

    // 메모리 할당 실패 시 처리
    if (arr_ptr == NULL) {
        printf("메모리 할당 실패!\n");
        return 1;
    }

    // 배열처럼 사용
    for (int i = 0; i < size; i++) {
        arr_ptr[i] = (i + 1) * 10;
    }

    // 값 출력
    for (int i = 0; i < size; i++) {
        printf("arr_ptr[%d]: %d\n", i, arr_ptr[i]);
    }

    // 동적으로 할당된 메모리 해제
    free(arr_ptr);
    arr_ptr = NULL; // Dangling pointer 방지

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

```