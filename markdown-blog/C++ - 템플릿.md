---
date: 2025-06-30
tags:
  - C++
aliases:
---

# 템플릿

C++ 템플릿은 함수나 클래스를 일반적인 타입에 대해 작동하도록 정의할 수 있게 해주는 강력한 기능입니다. 이를 통해 코드의 재사용성을 높이고, 타입에 독립적인 코드를 작성할 수 있습니다.

주요 두 가지 유형의 템플릿이 있습니다:

## 1. 함수 템플릿 (Function Templates)

여러 다른 타입의 인수에 대해 동일한 작업을 수행하는 함수를 정의할 때 사용됩니다. 예를 들어, 두 값을 교환하는 `swap` 함수를 정수, 실수, 문자열 등 다양한 타입에 대해 재사용할 수 있습니다.

```cpp
template <typename T>
void swap(T& a, T& b) {
    T temp = a;
    a = b;
    b = temp;
}

#include <iostream>

int main() {
    int i = 10, j = 20;
    swap(i, j);
    std::cout << "i: " << i << ", j: " << j << std::endl; // 출력: i: 20, j: 10

    double d1 = 3.14, d2 = 1.618;
    swap(d1, d2);
    std::cout << "d1: " << d1 << ", d2: " << d2 << std::endl; // 출력: d1: 1.618, d2: 3.14
    return 0;
}
```

## 2. 클래스 템플릿 (Class Templates)

컨테이너 클래스(예: 스택, 큐, 리스트)와 같이 여러 다른 타입의 데이터를 저장하고 관리하는 클래스를 정의할 때 유용합니다.

```cpp
template <typename T>
class MyContainer {
public:
    T value;
    MyContainer(T val) : value(val) {}
    void print() {
        std::cout << "Value: " << value << std::endl;
    }
};

#include <iostream>
#include <string>

int main() {
    MyContainer<int> intContainer(123);
    intContainer.print(); // 출력: Value: 123

    MyContainer<std::string> stringContainer("Hello Template");
    stringContainer.print(); // 출력: Value: Hello Template
    return 0;
}
```

템플릿은 컴파일 시점에 특정 타입으로 인스턴스화(instantiation)되어 실제 코드가 생성됩니다. 이는 런타임 오버헤드 없이 타입 안전성을 제공합니다.

## 3. 템플릿 특수화 (Template Specialization)

특정 타입에 대해 템플릿의 일반적인 구현 대신 특별한 구현을 제공하는 기능입니다. 이는 특정 타입에 대해 더 효율적이거나 다른 동작을 수행해야 할 때 사용됩니다.

```cpp
#include <iostream>
#include <string>

// 일반 함수 템플릿
template <typename T>
void print_type(T val) {
    std::cout << "Generic type: " << val << std::endl;
}

// int 타입에 대한 템플릿 특수화
template <>
void print_type<int>(int val) {
    std::cout << "Specialized for int: " << val << std::endl;
}

// 클래스 템플릿 특수화 예시 (간략화)
template <typename T>
class MyData {
public:
    MyData(T val) { std::cout << "Generic MyData created with value: " << val << std::endl; }
};

template <>
class MyData<char*> {
public:
    MyData(char* val) { std::cout << "Specialized MyData for char* created with value: " << val << std::endl; }
};

int main() {
    print_type(1.23); // Generic type: 1.23
    print_type(10);   // Specialized for int: 10

    MyData<double> d_data(3.14);
    char* c_str = "test";
    MyData<char*> s_data(c_str);

    return 0;
}
```

## 4. 템플릿 메타프로그래밍 (Template Metaprogramming, TMP)

컴파일 시간에 계산을 수행하는 프로그래밍 기법입니다. 템플릿과 재귀를 사용하여 컴파일러가 코드를 생성하는 과정에서 복잡한 계산이나 로직을 처리하게 합니다. 런타임 성능을 최적화하는 데 사용될 수 있지만, 코드가 복잡해지고 디버깅이 어려울 수 있습니다.

```cpp
#include <iostream>

// 팩토리얼을 컴파일 시간에 계산하는 템플릿 메타프로그래밍
template <int N>
struct Factorial {
    static const int value = N * Factorial<N - 1>::value;
};

// 종료 조건 (base case)
template <>
struct Factorial<0> {
    static const int value = 1;
};

int main() {
    // 컴파일 시간에 팩토리얼 값 계산
    std::cout << "Factorial of 5: " << Factorial<5>::value << std::endl; // 출력: Factorial of 5: 120
    std::cout << "Factorial of 0: " << Factorial<0>::value << std::endl; // 출력: Factorial of 0: 1
    return 0;
}
```

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
