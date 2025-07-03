---
date: 2025-07-01
tags:
  - C++
aliases:
---

# 포인터 (Pointer)

C++에서 포인터는 메모리 주소를 저장하는 변수입니다. 이를 통해 프로그램은 메모리에 직접 접근하고 조작할 수 있습니다. C 언어의 포인터 개념과 매우 유사하지만, C++에서는 객체 지향적인 맥락에서 더 다양한 방식으로 활용됩니다.

## 1. 포인터의 기본

### 선언 (Declaration)
포인터 변수를 선언할 때는 `*` 기호를 사용하여 해당 변수가 포인터임을 나타냅니다.

```cpp
int* ptr; // int형 변수의 주소를 저장할 포인터 선언
double* dptr; // double형 변수의 주소를 저장할 포인터 선언
```

### 주소 연산자 (`&`)
변수의 메모리 주소를 얻기 위해 사용됩니다.

```cpp
#include <iostream>

int main() {
    int num = 10;
    int* ptr = &num; // num 변수의 주소를 ptr에 저장
    std::cout << "num의 주소: " << ptr << std::endl;
    return 0;
}
```

### 역참조 연산자 (`*`)
포인터가 가리키는 메모리 주소에 저장된 값에 접근하기 위해 사용됩니다.

```cpp
#include <iostream>

int main() {
    int num = 10;
    int* ptr = &num;
    std::cout << "ptr이 가리키는 값: " << *ptr << std::endl; // 출력: 10
    *ptr = 20; // 포인터를 통해 값 변경
    std::cout << "변경된 num의 값: " << num << std::endl; // 출력: 20
    return 0;
}
```

### `nullptr`

C++11부터 도입된 `nullptr`는 어떤 유효한 메모리 주소도 가리키지 않는 포인터를 나타내는 키워드입니다. 기존의 `NULL` 매크로보다 타입 안전성이 높습니다.

```cpp
#include <iostream>

int main() {
    int* ptr = nullptr; // nullptr로 초기화
    if (ptr == nullptr) {
        std::cout << "ptr은 널 포인터입니다." << std::endl;
    }
    // *ptr = 10; // 런타임 오류 발생 가능: 널 포인터 역참조
    return 0;
}
```

## 2. 포인터 산술 (Pointer Arithmetic)

포인터에 정수를 더하거나 빼는 것은 포인터가 가리키는 데이터 타입의 크기만큼 메모리 주소를 이동시킵니다. 이는 배열 요소를 순회할 때 유용합니다.

```cpp
#include <iostream>

int main() {
    int arr[] = {10, 20, 30, 40, 50};
    int* ptr = arr; // arr[0]의 주소를 가리킴

    std::cout << "ptr이 가리키는 값: " << *ptr << std::endl; // 출력: 10

    ptr++; // ptr은 이제 arr[1]을 가리킴 (int 크기만큼 이동)
    std::cout << "ptr++ 후 값: " << *ptr << std::endl; // 출력: 20

    ptr = ptr + 2; // ptr은 이제 arr[3]을 가리킴
    std::cout << "ptr + 2 후 값: " << *ptr << std::endl; // 출력: 40

    int* ptr_end = &arr[4];
    std::cout << "두 포인터의 차이 (요소 개수): " << ptr_end - arr << std::endl; // 출력: 4

    return 0;
}
```

## 3. 동적 메모리 할당과 포인터 (`new`, `delete`)

C++에서는 `new`와 `delete` 연산자를 사용하여 힙(heap) 메모리에서 동적으로 메모리를 할당하고 해제합니다. `new`는 메모리를 할당하고 생성자를 호출하며, `delete`는 소멸자를 호출하고 메모리를 해제합니다.

```cpp
#include <iostream>

int main() {
    int* dynamic_int = new int; // int형 변수 동적 할당
    *dynamic_int = 100;
    std::cout << "동적 할당된 int: " << *dynamic_int << std::endl;
    delete dynamic_int; // 메모리 해제
    dynamic_int = nullptr; // Dangling Pointer 방지

    int* dynamic_array = new int[5]; // int형 배열 5개 동적 할당
    for (int i = 0; i < 5; ++i) {
        dynamic_array[i] = (i + 1) * 10;
    }
    std::cout << "동적 할당된 배열 첫 요소: " << dynamic_array[0] << std::endl;
    delete[] dynamic_array; // 배열 메모리 해제
    dynamic_array = nullptr;

    return 0;
}
```

## 4. 포인터 사용 시 주의사항

*   **널 포인터 역참조**: `nullptr`을 가리키는 포인터를 역참조하면 프로그램 충돌과 같은 런타임 오류가 발생합니다.
*   **댕글링 포인터 (Dangling Pointer)**: `delete`로 메모리를 해제한 후에도 해당 메모리 주소를 가리키는 포인터입니다. 해제된 메모리에 접근하면 예측 불가능한 동작이 발생할 수 있으므로, 메모리 해제 후에는 포인터를 `nullptr`로 설정하는 것이 좋습니다.
*   **메모리 누수 (Memory Leak)**: `new`로 할당한 메모리를 `delete`로 해제하지 않으면, 해당 메모리는 프로그램 종료 시까지 운영체제로 반환되지 않아 메모리 누수가 발생합니다.
*   **스마트 포인터 사용 권장**: 현대 C++에서는 `std::unique_ptr`, `std::shared_ptr`와 같은 스마트 포인터를 사용하여 메모리 관리를 자동화하고 위에서 언급된 많은 문제점을 해결하는 것을 권장합니다. (자세한 내용은 [[C++ - 스마트 포인터]] 참조)

---
### C++ 기본

- [[C++ - 개요 및 C 언어와의 차이점]]
- [[C++ - 기본 문법]]
- [[C++ - 컴파일과 링크]]
- [[C++ - IDE 및 개발 환경]]

### 객체 지향 프로그래밍 (OOP)

- [[C++ - 클래스와 객체]]
- [[C++ - 생성자 및 소멸자]]
- [[C++ - 캡슐화]]
- [[C++ - 상속]]
- [[C++ - 다형성]]
- [[C++ - 추상화]]

### 메모리 관리

- [[C++ - 동적 메모리 할당]]
- [[C++ - 스마트 포인터]]

### 고급 C++ 기능

- [[C++ - 포인터]]
- [[C++ - 참조]]
- [[C++ - 템플릿]]
- [[C++ - 예외 처리]]
- [[C++ - 표준 라이브러리 (STL)]]
- [[C++ - 파일 입출력]]
- [[C++ - 현대 C++]]

### 실무 C++

- [[C++ - 빌드 시스템]]
- [[C++ - 테스트 프레임워크]]
- [[C++ - 디버깅 기법]]
- [[C++ - 성능 최적화]]
- [[C++ - 디자인 패턴]]
- [[C++ - 실무에서 사용하는 C++의 변형]]
