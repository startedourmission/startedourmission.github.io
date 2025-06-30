---
date: 2025-06-30
tags:
  - C
aliases:
---

# 반복문 (Loop)

C 언어에는 주로 세 가지 종류의 반복문이 있습니다:

### 1. `for` 문
특정 횟수만큼 반복하거나, 초기화, 조건, 증감식이 명확할 때 사용합니다.

```c
#include <stdio.h>

int main() {
    for (int i = 0; i < 5; i++) {
        printf("for 루프: %d\n", i);
    }
    return 0;
}
```

### 2. `while` 문
조건이 참(true)인 동안 반복합니다. 조건이 처음부터 거짓(false)이면 한 번도 실행되지 않을 수 있습니다.

```c
#include <stdio.h>

int main() {
    int i = 0;
    while (i < 5) {
        printf("while 루프: %d\n", i);
        i++;
    }
    return 0;
}
```

### 3. `do-while` 문
코드를 최소 한 번 실행한 후 조건이 참(true)인 동안 반복합니다. `while` 문과 달리 조건이 처음부터 거짓이더라도 최소 한 번은 실행됩니다.

```c
#include <stdio.h>

int main() {
    int i = 0;
    do {
        printf("do-while 루프: %d\n", i);
        i++;
    } while (i < 5);

    int j = 10; // 조건이 처음부터 거짓인 경우
    do {
        printf("이 메시지는 한 번만 출력됩니다: %d\n", j);
        j++;
    } while (j < 5);
    return 0;
}
```

## `break` 문

`break` 문은 반복문(for, while, do-while) 또는 `switch` 문 내에서 사용되며, `break` 문을 만나면 해당 반복문이나 `switch` 문을 즉시 종료하고 다음 코드로 넘어갑니다.

```c
#include <stdio.h>

int main() {
    for (int i = 0; i < 10; i++) {
        if (i == 5) {
            break; // i가 5가 되면 루프 종료
        }
        printf("break 예시: %d\n", i);
    }
    printf("루프 종료 후\n");
    return 0;
}
```

## `continue` 문

`continue` 문은 반복문 내에서 사용되며, `continue` 문을 만나면 현재 반복(iteration)의 나머지 부분을 건너뛰고 다음 반복을 즉시 시작합니다.

```c
#include <stdio.h>

int main() {
    for (int i = 0; i < 10; i++) {
        if (i % 2 == 0) {
            continue; // i가 짝수이면 다음 반복으로 넘어감
        }
        printf("continue 예시 (홀수만 출력): %d\n", i);
    }
    return 0;
}
```

---
## C 언어 가이드북 목차

## [[C - 개요]]

## [[C - 변수]]

## [[C - 조건문]]

## [[C - 반복문]]

## [[C - 함수]]

## 포인터
### [[C - 포인터의 기본]]
### [[C - 배열과 포인터]]
### [[C - 함수 포인터]]
### [[C - 구조체 포인터]]

## 구조체, 공용체, 열거형
### [[C - 구조체]]
### [[C - 공용체]]
### [[C - 열거형]]

## [[C - 전처리기]]

## [[C - 헤더 파일]]

## [[C - 현대 C 언어와 C23 표준]]

## [[C - 실무에서 사용하는 C 언어의 방언]]
