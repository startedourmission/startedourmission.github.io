---
date: 2025-06-30
tags:
  - C++
aliases:
---

# 스마트 포인터

C++11부터는 `new`와 `delete`의 직접적인 사용으로 인한 메모리 누수 및 Dangling Pointer 문제를 해결하기 위해 **스마트 포인터(Smart Pointers)**가 도입되었습니다. `std::unique_ptr`, `std::shared_ptr`, `std::weak_ptr` 등이 있으며, 이들은 RAII(Resource Acquisition Is Initialization) 원칙에 따라 메모리 관리를 자동화하여 `delete`를 명시적으로 호출할 필요가 없게 해줍니다.

현대 C++ 프로그래밍에서는 특별한 이유가 없는 한 `new`와 `delete`를 직접 사용하는 대신 스마트 포인터를 사용하는 것이 권장됩니다.

### `std::unique_ptr`

*   **소유권:** 단독 소유권을 가집니다. 하나의 `unique_ptr`만이 특정 자원을 소유할 수 있습니다.
*   **이동:** 소유권을 다른 `unique_ptr`로 이동(move)할 수 있지만, 복사(copy)는 불가능합니다.
*   **자동 해제:** `unique_ptr`이 스코프를 벗어나거나 재할당될 때, 소유하고 있던 자원을 자동으로 해제합니다.
*   **배열 지원:** `std::unique_ptr<Type[]>` 형태로 배열을 관리할 수 있습니다.

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
    // u_ptr은 이제 nullptr이 됩니다.

    // std::unique_ptr을 사용하여 int 배열 동적 할당
    std::unique_ptr<int[]> u_arr = std::make_unique<int[]>(3);
    u_arr[0] = 10;
    u_arr[1] = 20;
    u_arr[2] = 30;
    std::cout << "unique_ptr 배열 값: " << u_arr[0] << ", " << u_arr[1] << ", " << u_arr[2] << std::endl;

    return 0;
}
```

### `std::shared_ptr`

*   **소유권:** 공유 소유권을 가집니다. 여러 `shared_ptr`가 동일한 자원을 소유할 수 있습니다.
*   **참조 카운트:** 자원을 소유하는 `shared_ptr`의 개수를 추적하는 참조 카운트(reference count)를 가집니다. 참조 카운트가 0이 되면 자원을 자동으로 해제합니다.
*   **복사 가능:** `shared_ptr`는 복사할 수 있으며, 복사될 때마다 참조 카운트가 증가합니다.

```cpp
#include <iostream>
#include <memory> // shared_ptr을 사용하기 위한 헤더

int main() {
    // std::shared_ptr을 사용하여 단일 double 객체 동적 할당
    std::shared_ptr<double> s_ptr = std::make_shared<double>(3.14);
    std::cout << "shared_ptr 값: " << *s_ptr << std::endl;
    std::cout << "참조 카운트: " << s_ptr.use_count() << std::endl;

    std::shared_ptr<double> s_ptr2 = s_ptr; // 복사
    std::cout << "s_ptr2 값: " << *s_ptr2 << std::endl;
    std::cout << "참조 카운트: " << s_ptr.use_count() << std::endl;

    return 0;
}
```

### `std::weak_ptr`

*   **소유권:** `shared_ptr`가 소유한 자원을 참조하지만, 소유권을 가지지 않습니다. 참조 카운트에 영향을 주지 않습니다.
*   **순환 참조 해결:** `shared_ptr` 간의 순환 참조(circular dependency)로 인한 메모리 누수 문제를 해결하는 데 사용됩니다.
*   **유효성 검사:** `weak_ptr`가 가리키는 자원이 유효한지 `lock()` 메서드를 통해 확인할 수 있습니다.

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

    // 스코프를 벗어나면 A와 B의 소멸자가 정상적으로 호출됩니다.
    return 0;
}
```