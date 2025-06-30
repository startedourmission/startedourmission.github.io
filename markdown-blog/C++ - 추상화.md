---
date: 2025-06-30
tags:
  - C++
aliases:
---

# 추상화

C++에서 추상화(Abstraction)는 사용자가 복잡한 구현 세부 사항을 알 필요 없이 필수적인 정보만 노출하고 불필요한 세부 사항은 숨기는 객체 지향 프로그래밍의 핵심 개념입니다.

## 주요 구현 방법:

### 1. 추상 클래스 (Abstract Classes)

하나 이상의 순수 가상 함수(pure virtual function)를 포함하는 클래스입니다. 추상 클래스는 직접 객체를 생성할 수 없으며, 반드시 파생 클래스에서 순수 가상 함수를 구현해야 합니다.

*   **순수 가상 함수**: `= 0`을 사용하여 선언되며, 기반 클래스에서 구현을 제공하지 않고 파생 클래스에서 반드시 재정의해야 하는 가상 함수입니다.
    *   예시: `virtual void draw() = 0;`

```cpp
#include <iostream>

// 추상 클래스 Shape
class Shape {
public:
    // 순수 가상 함수: 파생 클래스에서 반드시 구현해야 함
    virtual void draw() = 0;

    // 일반 멤버 함수 (구현을 가질 수 있음)
    void displayMessage() {
        std::cout << "도형을 그립니다." << std::endl;
    }

    // 가상 소멸자: 다형적 소멸을 위해 필수
    virtual ~Shape() {}
};

// 파생 클래스 Circle
class Circle : public Shape {
public:
    void draw() override { // 순수 가상 함수 구현
        std::cout << "원을 그립니다." << std::endl;
    }
};

// 파생 클래스 Rectangle
class Rectangle : public Shape {
public:
    void draw() override { // 순수 가상 함수 구현
        std::cout << "사각형을 그립니다." << std::endl;
    }
};

int main() {
    // Shape s; // 컴파일 오류: 추상 클래스는 객체를 생성할 수 없음

    Shape* circle = new Circle();
    Shape* rectangle = new Rectangle();

    circle->displayMessage();
    circle->draw(); // 출력: 원을 그립니다.

    rectangle->displayMessage();
    rectangle->draw(); // 출력: 사각형을 그립니다.

    delete circle;
    delete rectangle;

    return 0;
}
```

### 2. 인터페이스 (Interfaces)와 추상 클래스의 차이점

C++에는 `interface` 키워드가 별도로 존재하지 않지만, 모든 멤버 함수가 순수 가상 함수로만 이루어진 추상 클래스를 통해 인터페이스와 유사한 기능을 구현할 수 있습니다.

| 특징         | 추상 클래스 (Abstract Class)                               | 인터페이스 (Pure Abstract Class)                               |
| :----------- | :--------------------------------------------------------- | :------------------------------------------------------------- |
| **멤버 함수**  | 순수 가상 함수와 일반(구현된) 멤버 함수를 모두 가질 수 있음 | 모든 멤버 함수가 순수 가상 함수여야 함 (구현을 가질 수 없음)   |
| **멤버 변수**  | 멤버 변수를 가질 수 있음                                   | 멤버 변수를 가질 수 없음 (C++에서는 가능하지만, 인터페이스의 목적상 사용하지 않음) |
| **생성자/소멸자** | 생성자 및 소멸자를 가질 수 있음 (순수 가상 함수를 포함해도) | 생성자를 가질 수 없음 (소멸자는 가상 소멸자로 가질 수 있음)   |
| **목적**       | 공통된 기능을 부분적으로 구현하고, 파생 클래스에 특정 기능의 구현을 강제 | 파생 클래스가 반드시 구현해야 할 기능들의 집합(규약)을 정의    |
| **상속 목적**  | `is-a` 관계 (A는 B의 일종이다)를 나타내며, 코드 재사용 및 확장 | `can-do` 관계 (A는 B를 할 수 있다)를 나타내며, 다형성 구현에 중점 |

```cpp
#include <iostream>

// 인터페이스 (모든 함수가 순수 가상 함수)
class ILogger {
public:
    virtual void log(const std::string& message) = 0;
    virtual ~ILogger() {}
};

// 추상 클래스 (일반 함수와 순수 가상 함수를 모두 가짐)
class BaseProcessor {
public:
    virtual void processData() = 0;
    void commonOperation() {
        std::cout << "공통 작업을 수행합니다." << std::endl;
    }
    virtual ~BaseProcessor() {}
};

// 인터페이스를 구현하는 클래스
class ConsoleLogger : public ILogger {
public:
    void log(const std::string& message) override {
        std::cout << "[Console Log]: " << message << std::endl;
    }
};

// 추상 클래스를 상속받아 구현하는 클래스
class DataProcessor : public BaseProcessor {
public:
    void processData() override {
        std::cout << "데이터를 처리합니다." << std::endl;
    }
};

int main() {
    ILogger* logger = new ConsoleLogger();
    logger->log("인터페이스 예시");
    delete logger;

    BaseProcessor* processor = new DataProcessor();
    processor->commonOperation();
    processor->processData();
    delete processor;

    return 0;
}
```

## 추상화의 이점:

*   **복잡성 감소**: 사용자가 필요한 기능에만 집중하고 내부 구현의 복잡성을 무시할 수 있게 합니다.
*   **유지보수성 향상**: 내부 구현이 변경되어도 외부 인터페이스가 동일하게 유지되면, 해당 인터페이스를 사용하는 코드를 수정할 필요가 없습니다.
*   **확장성**: 새로운 기능을 추가하거나 기존 기능을 변경할 때, 추상화된 인터페이스를 통해 유연하게 대처할 수 있습니다.
*   **보안**: 중요한 데이터나 구현 세부 사항을 숨겨 외부로부터의 접근을 제한할 수 있습니다.

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