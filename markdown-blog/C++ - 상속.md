---
date: 2025-06-30
tags:
  - C++
aliases:
---

# 상속

C++에서 상속(Inheritance)은 객체 지향 프로그래밍의 핵심 개념 중 하나로, 기존 클래스(부모 클래스 또는 기본 클래스)의 속성과 메서드를 새로운 클래스(자식 클래스 또는 파생 클래스)가 물려받아 재사용할 수 있도록 하는 기능입니다. 이를 통해 코드의 재사용성을 높이고 중복을 줄여 더 효율적이고 관리하기 쉬운 코드를 작성할 수 있습니다.

**상속의 기본 개념:**

*   **기본 클래스 (Base Class / Parent Class):** 속성과 메서드를 제공하는 기존 클래스입니다.
*   **파생 클래스 (Derived Class / Child Class):** 기본 클래스로부터 속성과 메서드를 물려받는 새로운 클래스입니다. 파생 클래스는 기본 클래스의 기능을 모두 가지면서 자신만의 새로운 속성과 메서드를 추가할 수 있습니다.

**상속 문법:**

C++에서 상속은 콜론(`:`) 기호를 사용하여 선언합니다.

```cpp
class DerivedClass : access_specifier BaseClass {
    // 클래스 내용
};
```

여기서 `access_specifier`는 `public`, `protected`, `private` 중 하나가 될 수 있으며, 이는 기본 클래스의 멤버들이 파생 클래스에서 어떻게 접근될지 결정합니다.

## 상속 접근 지정자 (Access Specifiers)

기본 클래스의 멤버(public, protected, private)가 파생 클래스에서 어떤 접근 권한을 가지게 될지 결정합니다.

### 1. `public` 상속

*   기본 클래스의 `public` 멤버는 파생 클래스에서 `public`으로 상속됩니다.
*   기본 클래스의 `protected` 멤버는 파생 클래스에서 `protected`로 상속됩니다.
*   기본 클래스의 `private` 멤버는 파생 클래스에서 직접 접근할 수 없습니다.
*   가장 일반적인 상속 방식으로, 기본 클래스의 인터페이스를 그대로 유지하면서 기능을 확장할 때 사용됩니다.

```cpp
#include <iostream>

class BasePublic {
public:
    int public_var;
protected:
    int protected_var;
private:
    int private_var;
};

class DerivedPublic : public BasePublic {
public:
    void access_members() {
        public_var = 1;    // public 접근 가능
        protected_var = 2; // protected 접근 가능
        // private_var = 3; // private 접근 불가 (컴파일 오류)
        std::cout << "DerivedPublic: public_var = " << public_var << ", protected_var = " << protected_var << std::endl;
    }
};

int main() {
    DerivedPublic dp;
    dp.public_var = 10; // 외부에서 public_var 접근 가능
    // dp.protected_var = 20; // 외부에서 protected_var 접근 불가
    // dp.private_var = 30; // 외부에서 private_var 접근 불가
    dp.access_members();
    return 0;
}
```

### 2. `protected` 상속

*   기본 클래스의 `public` 및 `protected` 멤버는 파생 클래스에서 `protected`로 상속됩니다.
*   기본 클래스의 `private` 멤버는 파생 클래스에서 직접 접근할 수 없습니다.
*   파생 클래스 내부에서는 접근 가능하지만, 파생 클래스의 객체를 통해서는 외부에서 접근할 수 없게 됩니다.

```cpp
#include <iostream>

class BaseProtected {
public:
    int public_var;
protected:
    int protected_var;
private:
    int private_var;
};

class DerivedProtected : protected BaseProtected {
public:
    void access_members() {
        public_var = 1;    // protected로 상속되어 접근 가능
        protected_var = 2; // protected 접근 가능
        std::cout << "DerivedProtected: public_var = " << public_var << ", protected_var = " << protected_var << std::endl;
    }
};

int main() {
    DerivedProtected dp;
    // dp.public_var = 10; // 외부에서 public_var 접근 불가 (protected로 상속됨)
    dp.access_members();
    return 0;
}
```

### 3. `private` 상속

*   기본 클래스의 `public` 및 `protected` 멤버는 파생 클래스에서 `private`로 상속됩니다.
*   기본 클래스의 `private` 멤버는 파생 클래스에서 직접 접근할 수 없습니다.
*   파생 클래스 내부에서만 기본 클래스의 멤버에 접근할 수 있으며, 파생 클래스의 객체를 통해서는 외부에서 전혀 접근할 수 없게 됩니다. 구현 상속(Implementation Inheritance)에 주로 사용됩니다.

```cpp
#include <iostream>

class BasePrivate {
public:
    int public_var;
protected:
    int protected_var;
private:
    int private_var;
};

class DerivedPrivate : private BasePrivate {
public:
    void access_members() {
        public_var = 1;    // private로 상속되어 접근 가능
        protected_var = 2; // private 접근 가능
        std::cout << "DerivedPrivate: public_var = " << public_var << ", protected_var = " << protected_var << std::endl;
    }
};

int main() {
    DerivedPrivate dp;
    // dp.public_var = 10; // 외부에서 public_var 접근 불가 (private로 상속됨)
    dp.access_members();
    return 0;
}
```

**상속의 장점:**

*   **코드 재사용성:** 기존 클래스의 코드를 재사용하여 개발 시간을 단축하고 코드 중복을 줄입니다.
*   **유지보수 용이성:** 기본 클래스의 변경 사항이 모든 파생 클래스에 자동으로 반영되어 유지보수가 쉬워집니다.
*   **확장성:** 기존 클래스를 수정하지 않고도 새로운 기능을 추가하여 시스템을 확장할 수 있습니다.
*   **다형성(Polymorphism):** 가상 함수(virtual functions)를 통해 런타임에 객체의 실제 타입에 따라 적절한 함수가 호출되도록 하여 다형성을 구현할 수 있습니다.

**가상 함수 (Virtual Functions):**

가상 함수는 기본 클래스에 선언되고 파생 클래스에서 재정의(override)될 수 있는 멤버 함수입니다. 기본 클래스 포인터나 참조를 사용하여 파생 클래스 객체를 가리킬 때, 가상 함수를 호출하면 런타임에 실제 객체의 타입에 해당하는 함수가 실행됩니다. 이는 C++에서 런타임 다형성을 구현하는 핵심 메커니즘입니다.

*   **순수 가상 함수 (Pure Virtual Functions):** `= 0`을 사용하여 선언되며, 파생 클래스에서 반드시 재정의해야 하는 가상 함수입니다. 순수 가상 함수를 하나라도 포함하는 클래스는 추상 클래스(Abstract Class)가 되며, 직접 객체를 생성할 수 없습니다.

**생성자와 소멸자:**

상속 관계에서 객체가 생성될 때 생성자는 부모 클래스에서 자식 클래스 순서로 호출되며, 소멸자는 자식 클래스에서 부모 클래스 순서로 호출됩니다. 기본 클래스에 가상 함수가 하나라도 있다면, 소멸자도 `virtual`로 선언하는 것이 좋습니다. 이는 파생 클래스 객체가 기본 클래스 포인터를 통해 `delete`될 때, 파생 클래스의 소멸자가 올바르게 호출되도록 보장하여 메모리 누수를 방지합니다.

**다중 상속 (Multiple Inheritance):**

C++은 여러 개의 기본 클래스로부터 상속받는 다중 상속을 지원합니다. 하지만 다중 상속은 "다이아몬드 문제(Diamond Problem)"와 같은 복잡성을 야기할 수 있으며, 이는 가상 상속(virtual inheritance)을 통해 해결될 수 있습니다.

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
