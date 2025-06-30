---
date: 2025-06-30
tags:
  - C++
aliases:
---

# 템플릿

C++ 템플릿은 함수나 클래스를 일반적인 타입에 대해 작동하도록 정의할 수 있게 해주는 강력한 기능입니다. 이를 통해 코드의 재사용성을 높이고, 타입에 독립적인 코드를 작성할 수 있습니다.

주요 두 가지 유형의 템플릿이 있습니다:

1.  **함수 템플릿 (Function Templates)**: 여러 다른 타입의 인수에 대해 동일한 작업을 수행하는 함수를 정의할 때 사용됩니다. 예를 들어, 두 값을 교환하는 `swap` 함수를 정수, 실수, 문자열 등 다양한 타입에 대해 재사용할 수 있습니다.

    ```cpp
    template <typename T>
    void swap(T& a, T& b) {
        T temp = a;
        a = b;
        b = temp;
    }
    ```

2.  **클래스 템플릿 (Class Templates)**: 컨테이너 클래스(예: 스택, 큐, 리스트)와 같이 여러 다른 타입의 데이터를 저장하고 관리하는 클래스를 정의할 때 유용합니다.

    ```cpp
    template <typename T>
    class MyContainer {
    public:
        T value;
        MyContainer(T val) : value(val) {}
        void print() {
            // ...
        }
    };
    ```

템플릿은 컴파일 시점에 특정 타입으로 인스턴스화(instantiation)되어 실제 코드가 생성됩니다. 이는 런타임 오버헤드 없이 타입 안전성을 제공합니다.