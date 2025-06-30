---
date: 2025-06-30
tags:
  - C
aliases:
---

# 함수 (Function)

C 언어 함수는 특정 작업을 수행하는 코드 블록입니다. 함수는 프로그램을 더 작고 관리하기 쉬운 부분으로 나누는 데 사용됩니다.

주요 특징은 다음과 같습니다:
*   **재사용성**: 한 번 정의된 함수는 프로그램의 여러 곳에서 호출될 수 있습니다.
*   **모듈화**: 복잡한 프로그램을 논리적인 단위로 분할하여 코드의 가독성과 유지보수성을 높입니다.
*   **입력 및 출력**: 함수는 인수를 통해 데이터를 입력받을 수 있으며, 반환 값을 통해 결과를 출력할 수 있습니다.

기본적인 함수 선언 및 정의 구조는 다음과 같습니다:

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

**예시:**

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