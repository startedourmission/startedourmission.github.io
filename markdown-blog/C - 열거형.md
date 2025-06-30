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

## 열거형의 내부 동작 방식 (정수 값)

C 언어에서 열거형 멤버는 내부적으로 정수(integer) 값으로 표현됩니다. 명시적으로 값을 지정하지 않으면 첫 번째 멤버는 0, 그 다음 멤버는 1씩 증가하는 값을 가집니다. 이는 열거형을 정수형 변수처럼 사용할 수 있게 합니다.

```c
#include <stdio.h>

enum Colors {
    RED,   // 0
    GREEN, // 1
    BLUE   // 2
};

int main() {
    enum Colors myColor = GREEN;
    printf("myColor의 정수 값: %d\n", myColor); // 출력: myColor의 정수 값: 1

    // 정수 값을 열거형 변수에 할당할 수도 있습니다 (명시적 형 변환 권장)
    enum Colors anotherColor = (enum Colors)0;
    printf("anotherColor의 정수 값: %d\n", anotherColor); // 출력: anotherColor의 정수 값: 0

    return 0;
}
```

## 열거형 사용 시 주의사항

*   **이름 충돌**: 열거형 멤버의 이름은 해당 스코프 내에서 유일해야 합니다. 다른 열거형이나 변수와 이름이 겹치지 않도록 주의해야 합니다.
*   **타입 안전성 부족**: C 언어의 열거형은 C++의 `enum class`와 달리 타입 안전성이 약합니다. 즉, 열거형 변수에 해당 열거형에 정의되지 않은 정수 값을 할당할 수 있으며, 컴파일러가 경고를 주지 않을 수도 있습니다. 이는 예상치 못한 동작을 유발할 수 있습니다.
*   **값의 중복**: 명시적으로 값을 지정할 경우, 여러 멤버가 동일한 정수 값을 가질 수 있습니다. 이는 코드의 의미를 모호하게 만들 수 있으므로 피하는 것이 좋습니다.

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