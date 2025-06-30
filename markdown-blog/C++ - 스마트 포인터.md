---
date: 2025-06-30
tags:
  - C++
aliases:
---

# 스마트 포인터

C++11부터는 `new`와 `delete`의 직접적인 사용으로 인한 메모리 누수 및 Dangling Pointer 문제를 해결하기 위해 **스마트 포인터(Smart Pointers)**가 도입되었습니다. `std::unique_ptr`, `std::shared_ptr`, `std::weak_ptr` 등이 있으며, 이들은 RAII(Resource Acquisition Is Initialization) 원칙에 따라 메모리 관리를 자동화하여 `delete`를 명시적으로 호출할 필요가 없게 해줍니다.

현대 C++ 프로그래밍에서는 특별한 이유가 없는 한 `new`와 `delete`를 직접 사용하는 대신 스마트 포인터를 사용하는 것이 권장됩니다.

## `std::unique_ptr`

*   **소유권:** 단독 소유권을 가집니다. 하나의 `unique_ptr`만이 특정 자원을 소유할 수 있습니다. 복사 생성자나 복사 할당 연산자가 삭제되어 복사가 불가능하며, `std::move`를 통해서만 소유권을 이전할 수 있습니다.
*   **이동:** 소유권을 다른 `unique_ptr`로 이동(move)할 수 있지만, 복사(copy)는 불가능합니다. 이동 후 원본 `unique_ptr`은 `nullptr`이 됩니다.
*   **자동 해제:** `unique_ptr`이 스코프를 벗어나거나 재할당될 때, 소유하고 있던 자원을 자동으로 해제합니다. 이는 스택 기반의 RAII를 통해 이루어집니다.
*   **배열 지원:** `std::unique_ptr<Type[]>` 형태로 배열을 관리할 수 있으며, 이 경우 `delete[]`가 자동으로 호출됩니다.
*   **경량:** `shared_ptr`에 비해 오버헤드가 적어 성능상 이점이 있습니다.

```cpp
#include <iostream>
#include <memory> // unique_ptr을 사용하기 위한 헤더

int main() {
    // std::unique_ptr을 사용하여 단일 int 객체 동적 할당
    std::unique_ptr<int> u_ptr = std::make_unique<int>(200);
    std::cout << "unique_ptr 값: " << *u_ptr << std::endl;

    // 소유권 이동
    std::unique_ptr<int> u_ptr2 = std::move(u_ptr);
    std::cout << "u_ptr2 값: " << *u_ptr2 << std::endl;
    // u_ptr은 이제 nullptr이 됩니다. (std::cout << *u_ptr; 하면 런타임 오류 발생)

    // std::unique_ptr을 사용하여 int 배열 동적 할당
    std::unique_ptr<int[]> u_arr = std::make_unique<int[]>(3);
    u_arr[0] = 10;
    u_arr[1] = 20;
    u_arr[2] = 30;
    std::cout << "unique_ptr 배열 값: " << u_arr[0] << ", " << u_arr[1] << ", " << u_arr[2] << std::endl;

    return 0;
}
```

## `std::shared_ptr`

*   **소유권:** 공유 소유권을 가집니다. 여러 `shared_ptr`가 동일한 자원을 소유할 수 있습니다. 참조 카운트(reference count) 메커니즘을 사용하여 자원의 소유자를 추적합니다.
*   **참조 카운트:** 자원을 소유하는 `shared_ptr`의 개수를 추적하는 참조 카운트를 가집니다. 참조 카운트가 0이 되면 (즉, 더 이상 해당 자원을 가리키는 `shared_ptr`가 없으면) 자원을 자동으로 해제합니다.
*   **복사 가능:** `shared_ptr`는 복사할 수 있으며, 복사될 때마다 참조 카운트가 증가합니다.
*   **오버헤드:** `unique_ptr`에 비해 참조 카운트 관리를 위한 약간의 런타임 오버헤드가 있습니다.

```cpp
#include <iostream>
#include <memory> // shared_ptr을 사용하기 위한 헤더

int main() {
    // std::shared_ptr을 사용하여 단일 double 객체 동적 할당
    std::shared_ptr<double> s_ptr = std::make_shared<double>(3.14);
    std::cout << "shared_ptr 값: " << *s_ptr << std::endl;
    std::cout << "참조 카운트: " << s_ptr.use_count() << std::endl; // 출력: 1

    std::shared_ptr<double> s_ptr2 = s_ptr; // 복사
    std::cout << "s_ptr2 값: " << *s_ptr2 << std::endl;
    std::cout << "참조 카운트: " << s_ptr.use_count() << std::endl; // 출력: 2

    { // 새로운 스코프
        std::shared_ptr<double> s_ptr3 = s_ptr; // 또 다른 복사
        std::cout << "내부 스코프 참조 카운트: " << s_ptr.use_count() << std::endl; // 출력: 3
    } // s_ptr3 소멸, 참조 카운트 감소

    std::cout << "외부 스코프 참조 카운트: " << s_ptr.use_count() << std::endl; // 출력: 2

    return 0;
}
```

## `std::weak_ptr`

*   **소유권:** `shared_ptr`가 소유한 자원을 참조하지만, 소유권을 가지지 않습니다. 참조 카운트에 영향을 주지 않습니다.
*   **순환 참조 해결:** `shared_ptr` 간의 순환 참조(circular dependency)로 인한 메모리 누수 문제를 해결하는 데 사용됩니다. `shared_ptr`가 서로를 참조하여 참조 카운트가 0이 되지 않아 메모리가 해제되지 않는 상황을 방지합니다.
*   **유효성 검사:** `weak_ptr`가 가리키는 자원이 유효한지 `lock()` 메서드를 통해 확인할 수 있습니다. `lock()`은 자원이 유효하면 `shared_ptr`를 반환하고, 유효하지 않으면 `nullptr`를 반환합니다.

```cpp
#include <iostream>
#include <memory>

class B;

class A {
public:
    std::shared_ptr<B> b_ptr;
    ~A() { std::cout << "A 소멸자 호출" << std::endl; }
};

class B {
public:
    std::weak_ptr<A> a_ptr; // weak_ptr 사용
    ~B() { std::cout << "B 소멸자 호출" << std::endl; }
};

int main() {
    std::shared_ptr<A> a = std::make_shared<A>();
    std::shared_ptr<B> b = std::make_shared<B>();

    a->b_ptr = b;
    b->a_ptr = a; // weak_ptr 사용으로 순환 참조 방지

    // weak_ptr이 가리키는 자원이 유효한지 확인
    if (auto shared_a = b->a_ptr.lock()) {
        std::cout << "A 객체가 아직 유효합니다." << std::endl;
    } else {
        std::cout << "A 객체가 소멸되었습니다." << std::endl;
    }

    // 스코프를 벗어나면 A와 B의 소멸자가 정상적으로 호출됩니다.
    return 0;
}
```

## 언제 어떤 스마트 포인터를 사용해야 하는가?

스마트 포인터의 선택은 자원의 소유권 관리 방식에 따라 달라집니다.

*   **`std::unique_ptr`**: 자원에 대한 **단독 소유권**이 필요할 때 사용합니다. 가장 기본적인 스마트 포인터이며, 오버헤드가 가장 적습니다. 함수에서 동적으로 할당된 객체를 반환할 때나, 컨테이너에 객체를 저장할 때 유용합니다. `std::make_unique`를 사용하여 생성하는 것이 좋습니다.

*   **`std::shared_ptr`**: 자원에 대한 **공유 소유권**이 필요할 때 사용합니다. 여러 객체가 동일한 자원을 공유하고, 마지막 소유자가 자원을 해제해야 할 때 적합합니다. `std::make_shared`를 사용하여 생성하는 것이 좋습니다.

*   **`std::weak_ptr`**: `shared_ptr`의 **순환 참조 문제를 해결**하기 위해 사용합니다. `shared_ptr`가 소유한 자원을 참조하지만, 소유권을 주장하지 않아 참조 카운트에 영향을 주지 않습니다. 주로 `shared_ptr`와 함께 사용되며, 객체의 존재 여부를 확인하는 용도로 사용됩니다.

일반적으로 `unique_ptr`를 우선적으로 고려하고, 공유 소유권이 명확히 필요한 경우에만 `shared_ptr`를 사용하며, `shared_ptr` 간의 순환 참조가 발생할 때 `weak_ptr`를 사용하여 문제를 해결하는 것이 좋은 관례입니다.

---
# C++ 가이드북 목차

# 개요

C++는 C 언어에서 확장된 프로그래밍 언어로, 객체 지향 프로그래밍(OOP) 패러다임을 지원하는 것이 가장 큰 특징입니다. Bjarne Stroustrup이 1979년 C 언어에 객체 지향 개념을 추가하여 "C with Classes"라는 이름으로 개발을 시작했으며, 1983년에 C++로 이름이 변경되었습니다. C++는 절차 지향, 객체 지향, 제네릭 프로그래밍 등 다양한 프로그래밍 스타일을 지원하는 다중 패러다임 언어입니다.

C++는 운영 체제, 게임 개발, 임베디드 시스템, 고성능 애플리케이션 등 다양한 분야에서 널리 사용됩니다. C++는 시스템 자원과 메모리에 대한 높은 수준의 제어를 제공하며, 빠른 실행 속도를 자랑합니다.

# 본문

## [[C++ - C 언어와의 차이점]]

## 객체 지향 프로그래밍 (OOP)
### [[C++ - 클래스와 객체]]
### [[C++ - 상속]]
### [[C++ - 다형성]]
### [[C++ - 캡슐화]]
### [[C++ - 추상화]]

## 메모리 관리
### [[C++ - 동적 메모리 할당]]
### [[C++ - 스마트 포인터]]

## [[C++ - 템플릿]]

## [[C++ - 예외 처리]]

## [[C++ - 표준 라이브러리 (STL)]]

## [[C++ - 현대 C++]]
