---
date: 2025-06-30
tags:
  - C++
aliases:
---

# 생성자 및 소멸자

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
