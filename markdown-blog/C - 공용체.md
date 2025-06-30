---
date: 2025-06-30
tags:
  - C
aliases:
---

# 공용체

C 언어에서 공용체(union)는 여러 멤버 변수들이 **같은 메모리 공간을 공유**하도록 하는 사용자 정의 자료형입니다. 구조체(struct)와 유사하게 여러 타입의 변수들을 하나로 묶을 수 있지만, 구조체는 각 멤버가 독립적인 메모리 공간을 가지는 반면, 공용체는 모든 멤버가 시작 주소를 공유하며, 가장 큰 멤버의 크기만큼 메모리를 할당받습니다.

**주요 특징:**
*   **메모리 공유:** 공용체 내의 모든 멤버는 동일한 메모리 공간을 사용합니다.
*   **크기:** 공용체의 크기는 멤버 중 가장 큰 멤버의 크기와 같습니다.
*   **값 저장:** 한 번에 하나의 멤버만 유효한 값을 가질 수 있습니다. 즉, 특정 멤버에 값을 저장하면 이전에 저장된 다른 멤버의 값은 덮어쓰여집니다.

**선언 방법:**

```c
union UnionName {
    dataType member1;
    dataType member2;
    // ...
};
```

**사용 예시:**

```c
#include <stdio.h>
#include <string.h> // strcpy 함수를 사용하기 위해 필요

union Data {
    int i;
    float f;
    char str[20];
};

int main() {
    union Data data;

    data.i = 10;
    printf("data.i : %d\n", data.i); // 출력: data.i : 10

    data.f = 220.5;
    printf("data.f : %f\n", data.f); // 출력: data.f : 220.5
    // 이 시점에서 data.i의 값은 유효하지 않게 됩니다.

    strcpy(data.str, "C Programming");
    printf("data.str : %s\n", data.str); // 출력: data.str : C Programming
    // 이 시점에서 data.i와 data.f의 값은 유효하지 않게 됩니다.

    // 모든 멤버가 같은 메모리를 공유하므로, 마지막으로 할당된 멤버의 값만 유효합니다.
    printf("data.i : %d\n", data.i);   // 예상치 못한 값 출력 (메모리 오염)
    printf("data.f : %f\n", data.f);   // 예상치 못한 값 출력 (메모리 오염)

    return 0;
}
```

**사용 목적:**
공용체는 주로 메모리를 절약해야 할 때, 또는 여러 데이터 타입 중 **하나만** 사용될 것이 확실할 때 유용하게 사용됩니다. 예를 들어, 특정 상황에 따라 정수, 실수, 문자열 중 하나의 데이터만 저장해야 하는 경우에 활용될 수 있습니다. 또한, 서로 다른 데이터 타입으로 동일한 메모리 영역을 해석해야 할 때도 사용됩니다.
