---
date: 2025-06-30
tags:
  - C++
aliases:
---

# 캡슐화

C++에서 캡슐화(Encapsulation)는 객체 지향 프로그래밍(OOP)의 핵심 원칙 중 하나로, 데이터(속성)와 해당 데이터를 조작하는 메서드(함수)를 하나의 단위(클래스)로 묶는 것을 의미합니다. 또한, 외부에서 직접 접근할 수 없도록 데이터를 보호하고, 메서드를 통해서만 접근하도록 제한하는 정보 은닉(Information Hiding)의 개념을 포함합니다.

**캡슐화의 목적:**

1.  **데이터 보호 (정보 은닉):** 클래스 내부의 데이터를 외부에서 직접 변경하는 것을 막아 데이터의 무결성을 유지합니다.
2.  **유지보수성 향상:** 내부 구현이 변경되더라도 외부 인터페이스가 동일하게 유지되므로, 코드 변경의 파급 효과를 줄여 유지보수를 용이하게 합니다.
3.  **재사용성 증대:** 잘 캡슐화된 클래스는 독립적인 모듈로 작동하여 다른 프로젝트나 다른 부분에서 쉽게 재사용될 수 있습니다.
4.  **복잡성 감소:** 사용자는 클래스의 내부 구현을 알 필요 없이 제공되는 인터페이스(public 메서드)만 사용하여 객체를 조작할 수 있으므로, 코드의 복잡성을 줄입니다.

**C++에서 캡슐화를 구현하는 방법:**

C++에서는 주로 **접근 지정자(Access Specifiers)**를 사용하여 캡슐화를 구현합니다.

### `private` 접근 지정자

*   `private`으로 선언된 멤버(데이터 또는 함수)는 해당 클래스 내부에서만 접근할 수 있습니다.
*   클래스 외부에서는 직접 접근할 수 없으며, `public` 메서드를 통해서만 간접적으로 접근하거나 수정할 수 있습니다. 이것이 정보 은닉의 핵심입니다.

```cpp
#include <iostream>

class MyClass {
private:
    int private_data; // private 멤버 변수

public:
    void setPrivateData(int val) {
        private_data = val;
    }
    int getPrivateData() {
        return private_data;
    }
};

int main() {
    MyClass obj;
    // obj.private_data = 10; // 컴파일 오류: private 멤버에 직접 접근 불가
    obj.setPrivateData(10);
    std::cout << obj.getPrivateData() << std::endl; // 출력: 10
    return 0;
}
```

### `protected` 접근 지정자

*   `protected`로 선언된 멤버는 해당 클래스 내부와 해당 클래스를 상속받은 파생 클래스에서만 접근할 수 있습니다.
*   `private`보다는 넓고 `public`보다는 좁은 접근 범위를 가집니다.

```cpp
#include <iostream>

class Base {
protected:
    int protected_data; // protected 멤버 변수

public:
    Base() : protected_data(0) {}
};

class Derived : public Base {
public:
    void setProtectedData(int val) {
        protected_data = val; // 파생 클래스에서 protected 멤버 접근 가능
    }
    int getProtectedData() {
        return protected_data;
    }
};

int main() {
    Derived d;
    d.setProtectedData(20);
    std::cout << d.getProtectedData() << std::endl; // 출력: 20
    // d.protected_data = 30; // 컴파일 오류: 외부에서 protected 멤버 접근 불가
    return 0;
}
```

### `public` 접근 지정자

*   `public`으로 선언된 멤버는 클래스 외부 어디에서든 접근할 수 있습니다.
*   일반적으로 클래스의 인터페이스(외부에서 호출할 수 있는 함수)를 정의할 때 사용됩니다.

```cpp
#include <iostream>

class AnotherClass {
public:
    int public_data; // public 멤버 변수

    void display() {
        std::cout << "Public data: " << public_data << std::endl;
    }
};

int main() {
    AnotherClass obj;
    obj.public_data = 30; // 외부에서 public 멤버 직접 접근 가능
    obj.display(); // 출력: Public data: 30
    return 0;
}
```

## `friend` 키워드

`friend` 키워드는 캡슐화 원칙의 예외를 허용합니다. `friend`로 선언된 함수나 클래스는 해당 클래스의 `private` 및 `protected` 멤버에 직접 접근할 수 있습니다. 이는 특정 상황에서 코드의 편의성이나 성능을 위해 사용되지만, 캡슐화를 약화시키므로 신중하게 사용해야 합니다.

### `friend` 함수

```cpp
#include <iostream>

class MyClass {
private:
    int value;

    // friend 함수 선언
    friend void printValue(MyClass& obj);

public:
    MyClass(int v) : value(v) {}
};

// friend 함수 정의
void printValue(MyClass& obj) {
    // friend 함수는 private 멤버에 직접 접근 가능
    std::cout << "Value from friend function: " << obj.value << std::endl;
}

int main() {
    MyClass obj(100);
    printValue(obj); // 출력: Value from friend function: 100
    return 0;
}
```

### `friend` 클래스

```cpp
#include <iostream>

class MyClass {
private:
    int secret_data;

    // friend 클래스 선언
    friend class FriendClass;

public:
    MyClass(int data) : secret_data(data) {}
};

class FriendClass {
public:
    void displaySecretData(MyClass& obj) {
        // FriendClass는 MyClass의 private 멤버에 직접 접근 가능
        std::cout << "Secret data from FriendClass: " << obj.secret_data << std::endl;
    }
};

int main() {
    MyClass obj(200);
    FriendClass f_obj;
    f_obj.displaySecretData(obj); // 출력: Secret data from FriendClass: 200
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
