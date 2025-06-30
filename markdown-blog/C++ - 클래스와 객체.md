---
date: 2025-06-30
tags:
  - C++
aliases:
---

# 클래스와 객체

C++에서 클래스는 객체를 생성하기 위한 틀 또는 설계도입니다. 클래스는 데이터(멤버 변수)와 해당 데이터를 조작하는 함수(멤버 함수)를 캡슐화합니다.

객체는 클래스의 인스턴스입니다. 즉, 클래스라는 설계도를 바탕으로 실제로 만들어진 실체입니다. 각 객체는 클래스에 정의된 멤버 변수와 멤버 함수를 가집니다.

**예시:**

```cpp
#include <iostream>
#include <string>

// 클래스 정의
class Car {
public:
    // 멤버 변수 (데이터)
    std::string brand;
    std::string model;
    int year;

    // 멤버 함수 (행동)
    void displayInfo() {
        std::cout << "Brand: " << brand << ", Model: " << model << ", Year: " << year << std::endl;
    }
};

// 객체 생성 및 사용
int main() {
    // Car 클래스의 객체 myCar 생성
    Car myCar;

    // 객체의 멤버 변수에 접근하여 값 할당
    myCar.brand = "Hyundai";
    myCar.model = "Sonata";
    myCar.year = 2023;

    // 객체의 멤버 함수 호출
    myCar.displayInfo(); // 출력: Brand: Hyundai, Model: Sonata, Year: 2023

    // 또 다른 Car 클래스의 객체 yourCar 생성
    Car yourCar;
    yourCar.brand = "Kia";
    your_Car.model = "K5";
    your_Car.year = 2024;
    your_Car.displayInfo(); // 출력: Brand: Kia, Model: K5, Year: 2024

    return 0;
}
```

이 예시에서 `Car`는 클래스이고, `myCar`와 `yourCar`는 `Car` 클래스의 객체입니다. 각 객체는 자신만의 `brand`, `model`, `year` 값을 가지며, `displayInfo()` 함수를 통해 자신의 정보를 출력할 수 있습니다.

## 생성자 (Constructor)

생성자는 객체가 생성될 때 자동으로 호출되는 특별한 멤버 함수입니다. 주로 객체의 멤버 변수를 초기화하는 데 사용됩니다. 생성자는 클래스와 동일한 이름을 가지며, 반환 타입이 없습니다.

```cpp
#include <iostream>
#include <string>

class Dog {
public:
    std::string name;
    int age;

    // 생성자
    Dog(std::string n, int a) {
        name = n;
        age = a;
        std::cout << name << " 객체가 생성되었습니다." << std::endl;
    }

    void displayInfo() {
        std::cout << "이름: " << name << ", 나이: " << age << std::endl;
    }
};

int main() {
    Dog myDog("바둑이", 3); // 객체 생성과 동시에 생성자 호출
    myDog.displayInfo();

    Dog yourDog("초코", 5);
    yourDog.displayInfo();

    return 0;
}
```

## 소멸자 (Destructor)

소멸자는 객체가 소멸될 때(메모리에서 해제될 때) 자동으로 호출되는 특별한 멤버 함수입니다. 주로 객체가 사용했던 자원(동적 할당된 메모리, 파일 핸들 등)을 해제하는 데 사용됩니다. 소멸자는 클래스 이름 앞에 `~`를 붙여 정의하며, 매개변수를 가질 수 없고 반환 타입도 없습니다.

```cpp
#include <iostream>

class MyClass {
public:
    MyClass() {
        std::cout << "생성자 호출" << std::endl;
    }

    ~MyClass() { // 소멸자
        std::cout << "소멸자 호출" << std::endl;
    }
};

int main() {
    MyClass obj1; // 객체 생성
    // obj1은 main 함수가 끝날 때 소멸자가 호출됩니다.

    if (true) {
        MyClass obj2; // 블록 내에서 객체 생성
        // obj2는 블록을 벗어날 때 소멸자가 호출됩니다.
    }

    std::cout << "main 함수 끝" << std::endl;
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
