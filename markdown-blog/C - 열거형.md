---
date: 2025-06-30
tags:
  - C
aliases:
---

# 열거형

C 언어에서 열거형(enumeration, `enum`)은 정수형 상수의 집합에 이름을 부여하여 코드의 가독성과 유지보수성을 높이는 데 사용되는 사용자 정의 데이터 타입입니다.

**1. 열거형 선언**

열거형은 `enum` 키워드를 사용하여 선언합니다.

```c
enum 열거형_이름 {
    상수1,
    상수2,
    상수3
};
```

예시:

```c
enum Weekday {
    MONDAY,
    TUESDAY,
    WEDNESDAY,
    THURSDAY,
    FRIDAY,
    SATURDAY,
    SUNDAY
};
```

**2. 열거형 멤버의 값**

기본적으로 열거형 멤버는 0부터 시작하여 1씩 증가하는 정수 값을 가집니다.

*   `MONDAY`는 0
*   `TUESDAY`는 1
*   `WEDNESDAY`는 2
*   ...
*   `SUNDAY`는 6

명시적으로 값을 지정할 수도 있습니다. 값을 지정하면 그 다음 멤버는 지정된 값에서 1씩 증가합니다.

```c
enum Status {
    SUCCESS = 0,
    FAILURE = 1,
    PENDING = 5, // PENDING은 5
    UNKNOWN      // UNKNOWN은 6 (PENDING 다음이므로 5 + 1)
};
```

**3. 열거형 변수 선언 및 사용**

열거형을 선언한 후에는 해당 열거형 타입의 변수를 선언하고 사용할 수 있습니다.

```c
enum Weekday today; // Weekday 타입의 변수 today 선언
today = MONDAY;     // 열거형 멤버 할당

if (today == MONDAY) {
    printf("오늘은 월요일입니다.\n");
}

enum Status currentStatus = PENDING;
printf("현재 상태: %d\n", currentStatus); // 출력: 현재 상태: 5
```

**4. 열거형의 장점**

*   **가독성 향상:** 숫자 상수 대신 의미 있는 이름을 사용하여 코드를 더 쉽게 이해할 수 있습니다. 예를 들어, `if (day == 0)` 대신 `if (day == MONDAY)`를 사용하는 것이 훨씬 명확합니다.
*   **유지보수성 향상:** 관련된 상수들을 한 곳에 모아 관리할 수 있습니다. 새로운 상수가 추가되거나 기존 상수의 값이 변경될 때, 열거형 정의만 수정하면 됩니다.
*   **타입 안전성 (제한적):** 컴파일러가 열거형 변수에 유효하지 않은 값을 할당하는 것을 완전히 막지는 못하지만, 의도하지 않은 숫자 사용을 줄이는 데 도움이 됩니다.

**5. `typedef`와 함께 사용**

`enum` 키워드를 매번 쓰는 것이 번거롭다면 `typedef`를 사용하여 더 간결하게 타입을 정의할 수 있습니다.

```c
typedef enum {
    RED,
    GREEN,
    BLUE
} Color; // 이제 Color는 enum { RED, GREEN, BLUE }와 동일한 타입 이름이 됩니다.

Color myColor = BLUE;
printf("My color is %d\n", myColor); // 출력: My color is 2
```
