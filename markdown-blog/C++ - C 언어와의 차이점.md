---
date: 2025-06-30
tags:
  - C++
aliases:
---

# C 언어와 C++ 언어의 주요 차이점

*   **프로그래밍 패러다임:**
    *   **C 언어:** 절차 지향 프로그래밍 언어입니다. 프로그램의 순서와 절차를 중요하게 생각하며, 함수를 중심으로 코드를 구성합니다.
        ```c
        // C 언어 예시: 절차 지향
        #include <stdio.h>

        void print_message() {
            printf("Hello from C!\n");
        }

        int main() {
            print_message();
            return 0;
        }
        ```
    *   **C++ 언어:** 객체 지향 프로그래밍(OOP)을 지원하는 다중 패러다임 언어입니다. 클래스와 객체를 통해 데이터와 함수를 캡슐화하고, 재사용성 및 유지보수성을 높입니다.
        ```cpp
        // C++ 언어 예시: 객체 지향
        #include <iostream>

        class Greeter {
        public:
            void print_message() {
                std::cout << "Hello from C++!" << std::endl;
            }
        };

        int main() {
            Greeter g;
            g.print_message();
            return 0;
        }
        ```

*   **객체 지향 기능:**
    *   **C 언어:** 클래스, 객체, 상속, 다형성, 캡슐화, 추상화와 같은 객체 지향 개념을 지원하지 않습니다.
    *   **C++ 언어:** 클래스, 객체, 상속, 다형성, 캡슐화, 추상화 등 객체 지향의 주요 개념을 모두 지원합니다.
        ```cpp
        // C++ 언어 예시: 클래스 (OOP의 기본)
        #include <iostream>
        #include <string>

        class Animal {
        public:
            std::string name;
            Animal(std::string n) : name(n) {}
            void speak() {
                std::cout << name << " makes a sound." << std::endl;
            }
        };

        int main() {
            Animal dog("Buddy");
            dog.speak(); // Buddy makes a sound.
            return 0;
        }
        ```

*   **메모리 관리:**
    *   **C 언어:** `malloc()`, `calloc()`, `free()` 함수를 사용하여 동적 메모리를 할당하고 해제합니다.
        ```c
        // C 언어 예시: malloc/free
        #include <stdio.h>
        #include <stdlib.h>

        int main() {
            int *arr = (int*)malloc(5 * sizeof(int));
            if (arr == NULL) return 1;
            arr[0] = 10;
            printf("C malloc: %d\n", arr[0]);
            free(arr);
            return 0;
        }
        ```
    *   **C++ 언어:** `new` 및 `delete` 연산자를 사용하여 동적 메모리를 할당하고 해제합니다.
        ```cpp
        // C++ 언어 예시: new/delete
        #include <iostream>

        int main() {
            int *num = new int(20);
            std::cout << "C++ new: " << *num << std::endl;
            delete num;
            return 0;
        }
        ```

*   **함수 및 연산자:**
    *   **C 언어:** 함수 오버로딩(동일한 이름의 함수를 여러 용도로 사용하는 것)을 지원하지 않습니다.
    *   **C++ 언어:** 함수 오버로딩 및 연산자 오버로딩(기존 연산자에 새로운 연산을 정의)을 지원합니다.
        ```cpp
        // C++ 언어 예시: 함수 오버로딩
        #include <iostream>

        int add(int a, int b) { return a + b; }
        double add(double a, double b) { return a + b; }

        int main() {
            std::cout << "Int add: " << add(1, 2) << std::endl;
            std::cout << "Double add: " << add(1.5, 2.5) << std::endl;
            return 0;
        }
        ```

*   **입출력:**
    *   **C 언어:** `scanf()`와 `printf()` 함수를 표준 입출력에 사용합니다.
        ```c
        // C 언어 예시: printf/scanf
        #include <stdio.h>

        int main() {
            int val;
            printf("Enter an integer (C): ");
            scanf("%d", &val);
            printf("You entered (C): %d\n", val);
            return 0;
        }
        ```
    *   **C++ 언어:** `cin`과 `cout` 객체를 표준 입출력에 사용합니다.
        ```cpp
        // C++ 언어 예시: cout/cin
        #include <iostream>

        int main() {
            int val;
            std::cout << "Enter an integer (C++): ";
            std::cin >> val;
            std::cout << "You entered (C++): " << val << std::endl;
            return 0;
        }
        ```

*   **예외 처리:**
    *   **C 언어:** 직접적인 예외 처리 메커니즘을 제공하지 않습니다.
    *   **C++ 언어:** `try-catch` 블록을 사용하여 예외 처리를 지원합니다.
        ```cpp
        // C++ 언어 예시: try-catch
        #include <iostream>
        #include <stdexcept>

        double divide(double a, double b) {
            if (b == 0) {
                throw std::runtime_error("Division by zero!");
            }
            return a / b;
        }

        int main() {
            try {
                std::cout << divide(10.0, 0.0) << std::endl;
            } catch (const std::runtime_error& e) {
                std::cerr << "Error: " << e.what() << std::endl;
            }
            return 0;
        }
        ```

*   **참조 변수:**
    *   **C 언어:** 포인터만 지원하며 참조 변수 개념이 없습니다.
    *   **C++ 언어:** 포인터와 함께 참조 변수를 지원합니다.
        ```cpp
        // C++ 언어 예시: 참조 변수
        #include <iostream>

        int main() {
            int a = 10;
            int &ref = a; // ref는 a의 참조
            ref = 20;     // ref를 변경하면 a도 변경됨
            std::cout << "a: " << a << ", ref: " << ref << std::endl;
            return 0;
        }
        ```

*   **호환성:**
    *   **C++ 언어:** C 언어의 확장이며 상위 집합이므로, 거의 모든 유효한 C 프로그램은 유효한 C++ 프로그램으로 컴파일될 수 있습니다.

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
