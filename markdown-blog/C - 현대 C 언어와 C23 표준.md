---
date: 2025-06-30
tags:
  - C
aliases:
---

# 현대 C 언어와 C23 표준

C 언어의 최신 표준은 **C23**이며, 공식 명칭은 **ISO/IEC 9899:2024**입니다. 이 표준은 2024년 10월 31일에 발표되었으며, 이전 C17(ISO/IEC 9899:2018) 표준을 대체합니다.

C23 표준은 C 언어에 여러 새로운 기능과 개선 사항을 도입하여 코드 가독성, 안전성, 성능 및 최신 시스템과의 호환성을 향상시키는 것을 목표로 합니다.

## 주요 변경 사항 및 새로운 기능:

### `__STDC_VERSION__` 매크로 값 변경

C 표준 버전을 나타내는 매크로 `__STDC_VERSION__`의 값이 `202311L`로 변경되었습니다. 이를 통해 컴파일러가 어떤 C 표준을 따르는지 프로그램 내에서 확인할 수 있습니다.

```c
#include <stdio.h>

int main() {
    #if __STDC_VERSION__ >= 202311L
        printf("C23 표준 이상을 사용 중입니다.\n");
    #elif __STDC_VERSION__ >= 201710L
        printf("C17 표준 이상을 사용 중입니다.\n");
    #else
        printf("이전 C 표준을 사용 중입니다.\n");
    #endif
    return 0;
}
```

### `nullptr` 키워드 도입

C++에서 사용되던 `nullptr` 키워드가 C23에 도입되어 타입 안전성을 높인 널 포인터 표현을 제공합니다. 기존의 `NULL` 매크로보다 명확하고 타입 검사에 유리합니다.

```c
#include <stdio.h>

int main() {
    int *ptr = nullptr; // nullptr 사용
    if (ptr == nullptr) {
        printf("ptr은 널 포인터입니다.\n");
    }
    return 0;
}
```

### `constexpr` 키워드 도입

컴파일 시간에 변수와 함수를 평가할 수 있게 하여 성능 최적화를 돕습니다. `constexpr`로 선언된 변수는 컴파일 시간에 값이 결정되어야 하며, `constexpr` 함수는 컴파일 시간에 실행될 수 있습니다.

```c
#include <stdio.h>

constexpr int get_square(int x) {
    return x * x;
}

int main() {
    constexpr int val = 10; // 컴파일 시간 상수
    int result = get_square(val); // 컴파일 시간에 계산될 수 있음
    printf("Result: %d\n", result);
    return 0;
}
```

### `typeof` 및 `typeof_unqual` 연산자 표준화

표현식의 타입을 추론할 수 있게 하여 변수 선언을 간소화합니다. `typeof`는 `const`, `volatile`과 같은 한정자를 포함한 타입을 반환하고, `typeof_unqual`은 한정자를 제거한 기본 타입을 반환합니다.

```c
#include <stdio.h>

int main() {
    const int x = 10;
    typeof(x) y = x; // y는 const int 타입
    typeof_unqual(x) z = x; // z는 int 타입

    printf("y: %d, z: %d\n", y, z);
    return 0;
}
```

### `auto` 키워드

객체 정의 시 타입 추론을 위해 사용됩니다. C++의 `auto`와 유사하게 초기화 표현식으로부터 변수의 타입을 추론합니다. (함수 반환 타입이나 매개변수 타입 추론에는 사용되지 않습니다).

```c
#include <stdio.h>

int main() {
    auto num = 10; // num은 int 타입으로 추론
    auto pi = 3.14; // pi는 double 타입으로 추론
    printf("num: %d, pi: %.2f\n", num, pi);
    return 0;
}
```

### 가변 수정 타입(VMT) 의무화

가변 길이 배열(VLA)은 C99에서 도입되었으나 C11에서 선택 사항이 되었습니다. C23에서는 VLA가 자동 변수로는 의무화되지 않습니다. 이는 VLA의 사용을 권장하지 않는 방향으로 표준이 나아가고 있음을 의미합니다.

### `const` 한정자 지원 강화

배열과 함께 `const`를 사용하는 것에 대한 지원이 개선되었습니다. 예를 들어, `const int arr[5]`와 같이 배열 전체를 상수로 선언할 수 있습니다.

### 이진 리터럴 지원

`0b` 접두사를 사용하여 이진수 리터럴을 직접 표현할 수 있게 되었습니다. 이는 코드의 가독성을 높이고 비트 연산 시 유용합니다.

```c
#include <stdio.h>

int main() {
    int binary_num = 0b1010; // 십진수 10
    printf("Binary number: %d\n", binary_num); // 출력: 10
    return 0;
}
```

### 10진 부동 소수점 타입

`_Decimal32`, `_Decimal64`, `_Decimal128`과 같은 10진 부동 소수점 타입이 추가되었습니다. 이는 금융 계산과 같이 정밀한 10진수 연산이 필요한 경우에 유용합니다.

### 비트 정밀 정수 (`_BitInt`)

`_BitInt` 타입이 추가되어 임의의 비트 정밀도를 가진 정수를 선언할 수 있게 되었습니다. 예를 들어, `_BitInt(128)`은 128비트 정수를 나타냅니다.

### `u8` 문자 상수 및 문자열 리터럴

`u8` 접두사가 붙은 문자 상수와 문자열 리터럴의 타입이 변경되었습니다. 이는 UTF-8 인코딩된 문자열을 더 명확하게 다룰 수 있게 합니다.

### 숫자 구분자

숫자 리터럴 내에 작은따옴표(`'`)를 사용하여 숫자를 구분할 수 있게 되어 큰 숫자의 가독성을 높입니다 (예: `1'000'000`).

```c
#include <stdio.h>

int main() {
    long long large_num = 1'000'000'000LL; // 10억
    printf("Large number: %lld\n", large_num);
    return 0;
}
```

### 빈 초기화 (`{}`)

배열 및 구조체에 대한 빈 초기화(`{}`)가 허용됩니다. 이는 모든 멤버를 0으로 초기화하는 효과를 가집니다.

```c
#include <stdio.h>

struct Point {
    int x;
    int y;
};

int main() {
    int arr[5] = {}; // 모든 요소를 0으로 초기화
    struct Point p = {}; // 모든 멤버를 0으로 초기화

    printf("arr[0]: %d, p.x: %d\n", arr[0], p.x);
    return 0;
}
```

### C++ 호환성 개선

선언 전 레이블, 이름 없는 함수 인자, `{}`를 사용한 제로 초기화, 이름 없는 인자를 가진 가변 인자 함수, C++11 스타일 속성 등 C++와의 호환성이 향상되었습니다. 이는 C/C++ 혼합 프로젝트에서 유용합니다.

### 새로운 속성

`[[deprecated]]`, `[[fallthrough]]`, `[[maybe_unused]]`, `[[nodiscard]]`, `[[noreturn]]`과 같은 C++ 스타일 속성이 추가되었습니다. 이 속성들은 컴파일러에게 추가적인 정보를 제공하여 경고나 오류를 발생시키거나 코드 분석에 도움을 줍니다.

```c
#include <stdio.h>

[[deprecated("이 함수는 더 이상 사용되지 않습니다. new_function을 사용하세요.")]]
void old_function() {
    printf("오래된 함수입니다.\n");
}

int main() {
    old_function();
    return 0;
}
```

### `bool`, `true`, `false` 키워드

불리언 타입과 값을 위한 `bool`, `true`, `false` 키워드가 추가되었습니다. 이는 C++와 유사하게 불리언 값을 더 명확하게 다룰 수 있게 합니다.

```c
#include <stdio.h>
#include <stdbool.h> // bool, true, false 사용을 위해

int main() {
    bool is_active = true;
    if (is_active) {
        printf("활성화 상태입니다.\n");
    }
    return 0;
}
```

### `alignas` 및 `alignof` 키워드

기존 매크로에서 키워드로 변경되었습니다. `alignas`는 변수나 타입의 메모리 정렬을 지정하고, `alignof`는 타입의 정렬 요구사항을 반환합니다.

### `static_assert` 키워드

기존 매크로에서 키워드로 변경되었습니다. 컴파일 시간에 조건을 검사하여 조건이 거짓이면 컴파일 오류를 발생시킵니다.

```c
#include <assert.h>

// int의 크기가 4바이트가 아니면 컴파일 오류 발생
static_assert(sizeof(int) == 4, "int의 크기가 4바이트가 아닙니다.");

int main() {
    // ...
    return 0;
}
```

## 제거되거나 사용이 권장되지 않는 기능:

*   **트라이그래프(Trigraphs) 제거:** `??=`와 같은 3문자 시퀀스가 단일 문자로 해석되는 기능이 제거되었습니다.
*   **K&R 스타일 함수 정의/선언 제거:** 구형 C 스타일의 함수 정의 방식이 제거되었습니다.
*   **2의 보수(two's complement) 외의 부호 있는 정수 표현 제거:** 부호 있는 정수는 2의 보수 표현만 허용됩니다.
*   `_Noreturn`, `noreturn`, `<stdnoreturn.h>`가 사용이 권장되지 않습니다.
*   `__STDC_IEC_559__`, `__STDC_IEC_559_COMPLEX__`가 사용이 권장되지 않습니다.

## 컴파일러 지원:

GCC 13 이상 버전은 C23을 지원합니다. Clang 9.0 및 Pelles C 11.00은 실험적인 지원을 제공합니다. Visual Studio 17.9 이상 또는 cl.exe 버전 19.39.33428 이상에서는 `/std:clatest` 옵션을 통해 `typeof` 및 `typeof_unqual`과 같은 C23 기능을 사용할 수 있습니다.

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

