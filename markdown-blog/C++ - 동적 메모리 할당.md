---
date: 2025-06-30
tags:
  - C++
aliases:
---

# 동적 메모리 할당

C++에서 동적 메모리 할당은 `new` 연산자를 사용하고, 할당된 메모리를 해제할 때는 `delete` 연산자를 사용합니다. 이는 프로그램 실행 중에 필요한 만큼의 메모리를 힙(heap) 영역에서 할당하고 해제할 수 있게 해줍니다.

### 1. 단일 객체 할당 및 해제

**할당:** `new Type;`
**해제:** `delete pointer_to_Type;`

```cpp
#include <iostream>

int main() {
    // int 타입의 단일 변수를 위한 메모리 동적 할당
    int* ptr_int = new int;

    // 할당된 메모리에 값 저장
    *ptr_int = 100;

    // 값 출력
    std::cout << "동적 할당된 int 값: " << *ptr_int << std::endl;

    // 동적 할당된 메모리 해제
    delete ptr_int;
    ptr_int = nullptr; // Dangling pointer 방지를 위해 nullptr로 초기화하는 것이 좋습니다.

    // 해제된 메모리에 접근 시도 (런타임 오류 또는 예측 불가능한 동작 발생 가능)
    // std::cout << *ptr_int << std::endl; // 이 줄은 실행하지 마세요.

    return 0;
}

```

### 2. 배열 할당 및 해제

**할당:** `new Type[size];`
**해제:** `delete[] pointer_to_array;`

배열을 할당할 때는 `new[]`를 사용하고, 해제할 때는 반드시 `delete[]`를 사용해야 합니다. `delete` 대신 `delete[]`를 사용하지 않으면 정의되지 않은 동작(undefined behavior)이 발생할 수 있으며, 일반적으로 메모리 누수(memory leak)로 이어집니다.

```cpp
#include <iostream>

int main() {
    int size = 5;

    // int 타입의 5개 요소를 위한 배열 메모리 동적 할당
    int* ptr_array = new int[size];

    // 배열에 값 저장
    for (int i = 0; i < size; ++i) {
        ptr_array[i] = (i + 1) * 10;
    }

    // 배열 값 출력
    std::cout << "동적 할당된 배열 값: ";
    for (int i = 0; i < size; ++i) {
        std::cout << ptr_array[i] << " ";
    }
    std::cout << std::endl;

    // 동적 할당된 배열 메모리 해제
    delete[] ptr_array;
    ptr_array = nullptr; // Dangling pointer 방지를 위해 nullptr로 초기화

    return 0;
}

```

### 3. `new`와 `delete` 사용 시 주의사항

*   **메모리 누수(Memory Leak):** `new`로 할당한 메모리는 반드시 `delete` 또는 `delete[]`로 해제해야 합니다. 해제하지 않으면 프로그램이 종료될 때까지 해당 메모리가 운영체제로 반환되지 않아 메모리 누수가 발생합니다. 장시간 실행되는 프로그램에서는 심각한 문제가 될 수 있습니다.
*   **`new`와 `delete`의 짝:** 단일 객체는 `new`와 `delete`, 배열은 `new[]`와 `delete[]`를 반드시 짝으로 사용해야 합니다.
*   **Dangling Pointer:** 메모리를 해제한 후에도 포인터가 해당 메모리 주소를 가리키고 있는 상태를 Dangling Pointer라고 합니다. 해제된 메모리에 접근하면 런타임 오류나 예측 불가능한 동작을 유발할 수 있으므로, `delete` 후에는 포인터를 `nullptr`로 초기화하는 것이 좋은 습관입니다.
*   **예외 안전성:** `new` 연산자는 메모리 할당에 실패할 경우 `std::bad_alloc` 예외를 발생시킬 수 있습니다. 예외가 발생하면 `delete`가 호출되지 않아 메모리 누수가 발생할 수 있습니다.

### 4. 스마트 포인터 (Smart Pointers)

C++11부터는 `new`와 `delete`의 직접적인 사용으로 인한 메모리 누수 및 Dangling Pointer 문제를 해결하기 위해 **스마트 포인터(Smart Pointers)**가 도입되었습니다. `std::unique_ptr`, `std::shared_ptr`, `std::weak_ptr` 등이 있으며, 이들은 RAII(Resource Acquisition Is Initialization) 원칙에 따라 메모리 관리를 자동화하여 `delete`를 명시적으로 호출할 필요가 없게 해줍니다.

현대 C++ 프로그래밍에서는 특별한 이유가 없는 한 `new`와 `delete`를 직접 사용하는 대신 스마트 포인터를 사용하는 것이 권장됩니다.

```cpp
#include <iostream>
#include <memory> // 스마트 포인터를 사용하기 위한 헤더

int main() {
    // std::unique_ptr을 사용하여 단일 int 객체 동적 할당
    std::unique_ptr<int> u_ptr = std::make_unique<int>(200);
    std::cout << "unique_ptr 값: " << *u_ptr << std::endl;
    // u_ptr은 main 함수를 벗어날 때 자동으로 메모리를 해제합니다.

    // std::unique_ptr을 사용하여 int 배열 동적 할당
    std::unique_ptr<int[]> u_arr = std::make_unique<int[]>(3);
    u_arr[0] = 10;
    u_arr[1] = 20;
    u_arr[2] = 30;
    std::cout << "unique_ptr 배열 값: " << u_arr[0] << ", " << u_arr[1] << ", " << u_arr[2] << std::endl;
    // u_arr도 main 함수를 벗어날 때 자동으로 메모리를 해제합니다.

    // std::shared_ptr을 사용하여 단일 double 객체 동적 할당
    std::shared_ptr<double> s_ptr = std::make_shared<double>(3.14);
    std::cout << "shared_ptr 값: " << *s_ptr << std::endl;
    // s_ptr은 참조 카운트가 0이 될 때 자동으로 메모리를 해제합니다.

    return 0;
}

```