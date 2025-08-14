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

## `new`와 `delete`의 동작 방식

`new`와 `delete` 연산자는 단순히 메모리를 할당하고 해제하는 `malloc`/`free`와 달리, 객체의 생성자와 소멸자를 호출하는 추가적인 역할을 수행합니다.

*   **`new` 연산자**: 메모리를 할당한 후, 해당 메모리 공간에 객체의 **생성자(Constructor)**를 호출하여 객체를 초기화합니다. 만약 메모리 할당에 실패하면 `std::bad_alloc` 예외를 발생시킵니다.
*   **`delete` 연산자**: 객체의 **소멸자(Destructor)**를 호출한 후, 해당 객체가 사용하던 메모리를 해제합니다.

```cpp
#include <iostream>

class MyObject {
public:
    MyObject() { std::cout << "MyObject 생성자 호출" << std::endl; }
    ~MyObject() { std::cout << "MyObject 소멸자 호출" << std::endl; }
};

int main() {
    std::cout << "객체 생성 전" << std::endl;
    MyObject* obj = new MyObject(); // new 호출 시 생성자 호출
    std::cout << "객체 생성 후" << std::endl;
    delete obj; // delete 호출 시 소멸자 호출
    std::cout << "객체 소멸 후" << std::endl;

    // 배열의 경우
    std::cout << "\n배열 객체 생성 전" << std::endl;
    MyObject* arr = new MyObject[3]; // 각 요소에 대해 생성자 호출
    std::cout << "배열 객체 생성 후" << std::endl;
    delete[] arr; // 각 요소에 대해 소멸자 호출
    std::cout << "배열 객체 소멸 후" << std::endl;

    return 0;
}
```

## `new` 연산자의 예외 처리 (`std::nothrow`)

기본적으로 `new` 연산자는 메모리 할당에 실패하면 `std::bad_alloc` 예외를 발생시킵니다. 하지만 `std::nothrow`를 사용하면 예외 대신 `nullptr`를 반환하도록 할 수 있습니다. 이는 예외 처리를 사용하지 않는 환경이나, 메모리 할당 실패를 `nullptr` 검사를 통해 처리하고자 할 때 유용합니다.

```cpp
#include <iostream>
#include <new> // std::nothrow를 위해 필요

int main() {
    int* ptr = new (std::nothrow) int; // 예외 대신 nullptr 반환

    if (ptr == nullptr) {
        std::cout << "메모리 할당 실패! (std::nothrow 사용)" << std::endl;
    } else {
        *ptr = 100;
        std::cout << "할당된 값: " << *ptr << std::endl;
        delete ptr;
    }

    // 매우 큰 배열 할당 시도 (실패 가능성 높음)
    long long* large_array = new (std::nothrow) long long[100000000000LL]; // 의도적으로 큰 값

    if (large_array == nullptr) {
        std::cout << "매우 큰 배열 메모리 할당 실패!" << std::endl;
    } else {
        std::cout << "매우 큰 배열 메모리 할당 성공!" << std::endl;
        delete[] large_array;
    }

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

## `new`와 `delete`의 동작 방식

`new`와 `delete` 연산자는 단순히 메모리를 할당하고 해제하는 `malloc`/`free`와 달리, 객체의 생성자와 소멸자를 호출하는 추가적인 역할을 수행합니다.

*   **`new` 연산자**: 메모리를 할당한 후, 해당 메모리 공간에 객체의 **생성자(Constructor)**를 호출하여 객체를 초기화합니다. 만약 메모리 할당에 실패하면 `std::bad_alloc` 예외를 발생시킵니다.
*   **`delete` 연산자**: 객체의 **소멸자(Destructor)**를 호출한 후, 해당 객체가 사용하던 메모리를 해제합니다.

```cpp
#include <iostream>

class MyObject {
public:
    MyObject() { std::cout << "MyObject 생성자 호출" << std::endl; }
    ~MyObject() { std::cout << "MyObject 소멸자 호출" << std::endl; }
};

int main() {
    std::cout << "객체 생성 전" << std::endl;
    MyObject* obj = new MyObject(); // new 호출 시 생성자 호출
    std::cout << "객체 생성 후" << std::endl;
    delete obj; // delete 호출 시 소멸자 호출
    std::cout << "객체 소멸 후" << std::endl;

    // 배열의 경우
    std::cout << "\n배열 객체 생성 전" << std::endl;
    MyObject* arr = new MyObject[3]; // 각 요소에 대해 생성자 호출
    std::cout << "배열 객체 생성 후" << std::endl;
    delete[] arr; // 각 요소에 대해 소멸자 호출
    std::cout << "배열 객체 소멸 후" << std::endl;

    return 0;
}
```

## `new` 연산자의 예외 처리 (`std::nothrow`)

기본적으로 `new` 연산자는 메모리 할당에 실패하면 `std::bad_alloc` 예외를 발생시킵니다. 하지만 `std::nothrow`를 사용하면 예외 대신 `nullptr`를 반환하도록 할 수 있습니다. 이는 예외 처리를 사용하지 않는 환경이나, 메모리 할당 실패를 `nullptr` 검사를 통해 처리하고자 할 때 유용합니다.

```cpp
#include <iostream>
#include <new> // std::nothrow를 위해 필요

int main() {
    int* ptr = new (std::nothrow) int; // 예외 대신 nullptr 반환

    if (ptr == nullptr) {
        std::cout << "메모리 할당 실패! (std::nothrow 사용)" << std::endl;
    } else {
        *ptr = 100;
        std::cout << "할당된 값: " << *ptr << std::endl;
        delete ptr;
    }

    // 매우 큰 배열 할당 시도 (실패 가능성 높음)
    long long* large_array = new (std::nothrow) long long[100000000000LL]; // 의도적으로 큰 값

    if (large_array == nullptr) {
        std::cout << "매우 큰 배열 메모리 할당 실패!" << std::endl;
    } else {
        std::cout << "매우 큰 배열 메모리 할당 성공!" << std::endl;
        delete[] large_array;
    }

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
