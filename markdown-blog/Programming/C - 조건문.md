---
date: 2025-06-30
tags:
  - C
aliases:
---
# 조건문 (If)

C 언어의 조건문은 특정 조건에 따라 코드 블록을 실행하거나 건너뛸 때 사용됩니다. 주요 조건문은 `if`, `else if`, `else`, 그리고 `switch` 문입니다.

### 1. `if` 문
가장 기본적인 조건문입니다. 괄호 안의 조건이 참일 경우에만 코드 블록을 실행합니다. 

```c
#include <stdio.h>

int main() {
    int num = 10;
    if (num > 5) {
        printf("num은 5보다 큽니다.\n");
    }
    return 0;
}
```

### 2. `if-else` 문
`if` 문의 조건이 참이면 `if` 블록을, 거짓이면 `else` 블록을 실행합니다.

```c
#include <stdio.h>

int main() {
    int num = 3;
    if (num > 5) {
        printf("num은 5보다 큽니다.\n");
    } else {
        printf("num은 5보다 작거나 같습니다.\n");
    }
    return 0;
}
```

### 3. `if-else if-else` 문
여러 조건을 순차적으로 검사할 때 사용합니다. 첫 번째 `if` 조건이 거짓이면 다음 `else if` 조건을 검사하고, 모든 조건이 거짓이면 마지막 `else` 블록을 실행합니다.

```c
#include <stdio.h>

int main() {
    int score = 85;
    if (score >= 90) {
        printf("학점: A\n");
    } else if (score >= 80) {
        printf("학점: B\n");
    } else if (score >= 70) {
        printf("학점: C\n");
    } else {
        printf("학점: F\n");
    }
    return 0;
}
```

### 4. `switch` 문
하나의 변수(정수형 또는 문자형)의 값에 따라 여러 경우 중 하나를 선택하여 실행할 때 사용합니다. 각 `case` 블록의 끝에는 일반적으로 `break` 문을 사용하여 해당 `case` 실행 후 `switch` 문을 빠져나오도록 합니다. `break`가 없으면 다음 `case` 문으로 계속 실행됩니다 (`fall-through`). `default`는 어떤 `case`와도 일치하지 않을 때 실행됩니다.

```c
#include <stdio.h>

int main() {
    char grade = 'B';
    switch (grade) {
        case 'A':
            printf("Excellent!\n");
            break;
        case 'B':
            printf("Good!\n");
            break;
        case 'C':
            printf("Pass!\n");
            break;
        default:
            printf("Fail!\n");
            break;
    }
    return 0;
}
```

## 조건문 사용 시 주의사항

###  `=` (할당 연산자)와 `==` (비교 연산자) 혼동

C 언어에서는 `if (변수 = 값)`과 같이 할당 연산자를 사용해도 문법 오류가 발생하지 않고, 할당된 값이 0이 아니면 참으로 간주됩니다. 이는 의도치 않은 버그를 유발할 수 있으므로 주의해야 합니다. 항상 비교할 때는 `==`를 사용해야 합니다.

### `switch` 문에서의 `break` 누락

`switch` 문에서 각 `case` 끝에 `break` 문을 사용하지 않으면, 해당 `case`가 실행된 후 다음 `case`로 계속 실행되는 `fall-through` 현상이 발생합니다. 이는 의도된 동작일 수도 있지만, 대부분의 경우 버그로 이어지므로 주의해야 합니다.

### 복잡한 조건문 피하기

`if` 문 내부에 너무 많은 `&&` (AND)나 `||` (OR) 연산자를 사용하여 복잡한 조건을 만들면 가독성이 떨어지고 오류 발생 가능성이 높아집니다. 필요한 경우 조건을 여러 줄로 나누거나, 함수로 분리하여 가독성을 높이는 것이 좋습니다.

### 중첩된 `if` 문 최소화

`if` 문을 너무 깊게 중첩하면 코드의 흐름을 파악하기 어렵고 유지보수가 힘들어집니다. 가능한 경우 `else if`를 사용하거나, 함수로 분리하여 중첩 깊이를 줄이는 것을 고려해야 합니다.
