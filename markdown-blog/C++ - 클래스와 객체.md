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
    yourCar.model = "K5";
    yourCar.year = 2024;
    yourCar.displayInfo(); // 출력: Brand: Kia, Model: K5, Year: 2024

    return 0;
}
```

이 예시에서 `Car`는 클래스이고, `myCar`와 `yourCar`는 `Car` 클래스의 객체입니다. 각 객체는 자신만의 `brand`, `model`, `year` 값을 가지며, `displayInfo()` 함수를 통해 자신의 정보를 출력할 수 있습니다.