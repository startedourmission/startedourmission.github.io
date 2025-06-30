---
date: 2025-06-30
tags:
  - C++
aliases:
---

# 표준 라이브러리 (STL)

C++ 표준 라이브러리(Standard Template Library, STL)는 C++ 프로그래밍 언어를 위한 템플릿 클래스 및 함수의 집합으로, 일반적인 자료 구조와 알고리즘을 구현하여 제공합니다. 이는 C++ 표준 라이브러리의 중요한 부분이며, 효율적이고 재사용 가능한 코드를 작성하는 데 도움을 줍니다.

STL은 크게 네 가지 주요 구성 요소로 나뉩니다.

## 1. 컨테이너 (Containers)

데이터를 저장하고 관리하는 객체입니다. 각 컨테이너는 특정 요구 사항에 따라 데이터를 저장하며, 기본 작업을 수행하는 메서드를 포함하는 템플릿 클래스로 구현됩니다.

### 시퀀스 컨테이너 (Sequence Containers)
데이터를 선형적으로 저장합니다.

*   **`std::vector`**: 동적 배열로, 크기를 자동으로 조절할 수 있습니다. 임의 접근이 빠르고, 끝에 요소를 추가/삭제하는 것이 효율적입니다. 중간에 삽입/삭제는 비효율적입니다. 연속된 메모리 공간을 사용합니다.
    ```cpp
    #include <iostream>
    #include <vector>

    int main() {
        std::vector<int> v = {1, 2, 3};
        v.push_back(4); // 끝에 요소 추가
        std::cout << "Vector elements: ";
        for (int n : v) {
            std::cout << n << " ";
        }
        std::cout << std::endl; // 출력: Vector elements: 1 2 3 4
        std::cout << "Vector size: " << v.size() << std::endl; // 출력: Vector size: 4
        return 0;
    }
    ```
*   **`std::list`**: 양방향 연결 리스트입니다. 요소의 삽입 및 삭제가 빠르지만, 임의 접근(인덱스를 통한 접근)은 느립니다. 연속된 메모리 공간을 사용하지 않습니다.
*   **`std::deque`**: 양방향 큐로, 양쪽 끝에서 요소를 추가하거나 제거하는 것이 효율적입니다. `vector`와 `list`의 중간적인 특성을 가집니다.
*   **`std::array`**: 컴파일 시 크기가 고정된 배열입니다. C 스타일 배열과 유사하지만, STL 컨테이너의 인터페이스를 제공합니다.
*   **`std::forward_list`**: 단방향 연결 리스트입니다. `list`보다 메모리 사용량이 적고 삽입/삭제가 빠르지만, 뒤에서부터 접근하거나 크기를 알 수 없습니다.

### 연관 컨테이너 (Associative Containers)
정렬된 데이터를 키-값 쌍으로 저장하며, 빠른 검색을 제공합니다. 내부적으로 균형 이진 트리(Balanced Binary Tree) 구조를 사용합니다.

*   **`std::set`**: 고유한 값을 정렬된 순서로 저장합니다. 중복을 허용하지 않습니다.
*   **`std::map`**: 고유한 키와 해당 값의 쌍을 저장합니다. 키를 기준으로 정렬됩니다.
*   **`std::multiset`**, **`std::multimap`**: 중복된 키를 허용하는 `set`과 `map`입니다.

### 컨테이너 어댑터 (Container Adaptors)
기존 컨테이너의 인터페이스를 제한하여 특정 데이터 구조처럼 동작하게 합니다.

*   **`std::stack`**: LIFO(Last In, First Out) 원칙에 따라 작동합니다. (기본적으로 `std::deque`를 사용)
*   **`std::queue`**: FIFO(First In, First Out) 원칙에 따라 작동합니다. (기본적으로 `std::deque`를 사용)
*   **`std::priority_queue`**: 우선순위에 따라 요소를 정렬합니다. (기본적으로 `std::vector`를 사용)

### 비정렬 연관 컨테이너 (Unordered Associative Containers)
연관 컨테이너와 유사하지만, 데이터를 정렬하지 않고 해시 테이블을 사용하여 빠른 검색 시간을 제공합니다.

*   **`std::unordered_set`**: 고유한 값을 저장하며, 순서가 없습니다. 평균적으로 빠른 검색 속도를 가집니다.
*   **`std::unordered_map`**: 고유한 키와 해당 값의 쌍을 저장하며, 순서가 없습니다. 평균적으로 빠른 검색 속도를 가집니다.

### `std::string`

`std::string`은 문자열을 다루기 위한 클래스로, C 스타일 문자열(`char*`)의 단점을 보완하고 다양한 문자열 조작 기능을 제공합니다. 내부적으로 문자의 `vector`와 유사하게 동작합니다.

```cpp
#include <iostream>
#include <string>

int main() {
    std::string s1 = "Hello";
    std::string s2 = " World";

    std::string s3 = s1 + s2; // 문자열 연결
    std::cout << "s3: " << s3 << std::endl; // 출력: s3: Hello World

    std::cout << "Length of s3: " << s3.length() << std::endl; // 출력: Length of s3: 11

    s3.append("!"); // 문자열 추가
    std::cout << "s3 after append: " << s3 << std::endl; // 출력: s3 after append: Hello World!

    std::cout << "Character at index 0: " << s3[0] << std::endl; // 출력: Character at index 0: H

    return 0;
}
```

## 2. 알고리즘 (Algorithms)

컨테이너의 데이터를 조작하는 함수들의 집합입니다. 정렬, 검색, 변형 등 다양한 작업을 수행하며, 주로 이터레이터를 통해 컨테이너와 독립적으로 작동합니다.

*   예시: `std::sort()`, `std::find()`, `std::max_element()`, `std::min_element()`, `std::count()`, `std::for_each()` 등.

```cpp
#include <iostream>
#include <vector>
#include <algorithm> // std::sort, std::find 등
#include <numeric>   // std::accumulate 등

int main() {
    std::vector<int> v = {5, 2, 8, 1, 9};

    // 정렬
    std::sort(v.begin(), v.end());
    std::cout << "Sorted vector: ";
    for (int n : v) {
        std::cout << n << " ";
    }
    std::cout << std::endl; // 출력: Sorted vector: 1 2 5 8 9

    // 요소 찾기
    auto it = std::find(v.begin(), v.end(), 5);
    if (it != v.end()) {
        std::cout << "Found 5 at index: " << std::distance(v.begin(), it) << std::endl; // 출력: Found 5 at index: 2
    }

    // 합계 계산
    int sum = std::accumulate(v.begin(), v.end(), 0);
    std::cout << "Sum of elements: " << sum << std::endl; // 출력: Sum of elements: 25

    return 0;
}
```

## 3. 이터레이터 (Iterators)

컨테이너의 요소에 접근하는 포인터와 유사한 객체입니다. 이터레이터를 사용하면 컨테이너의 내부 구조에 관계없이 일관된 방식으로 요소를 순회하고 조작할 수 있습니다.

*   다섯 가지 주요 유형이 있습니다: 입력 이터레이터, 출력 이터레이터, 전방향 이터레이터, 양방향 이터레이터, 임의 접근 이터레이터.

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {10, 20, 30, 40, 50};

    // begin()과 end()를 사용하여 이터레이터 얻기
    std::vector<int>::iterator it = v.begin();

    // 이터레이터를 사용하여 요소 접근 및 순회
    while (it != v.end()) {
        std::cout << *it << " "; // 역참조하여 값 접근
        ++it; // 다음 요소로 이동
    }
    std::cout << std::endl; // 출력: 10 20 30 40 50

    return 0;
}
```

## 4. 함수 객체 (Functors / Function Objects)

함수처럼 호출될 수 있는 객체입니다. `operator()`를 오버로드하여 함수처럼 동작하게 만들며, 알고리즘과 함께 사용될 때 유연성을 제공하고 상태를 가질 수 있습니다.

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

// 두 숫자를 더하는 함수 객체
class Adder {
public:
    int operator()(int a, int b) const {
        return a + b;
    }
};

// 특정 값보다 큰지 확인하는 함수 객체 (상태를 가짐)
class GreaterThan {
private:
    int value_to_compare;
public:
    GreaterThan(int val) : value_to_compare(val) {}
    bool operator()(int n) const {
        return n > value_to_compare;
    }
};

int main() {
    Adder add_obj;
    std::cout << "Sum: " << add_obj(5, 3) << std::endl; // 출력: Sum: 8

    std::vector<int> v = {1, 10, 3, 20, 5};
    GreaterThan gt_obj(7);

    // 알고리즘과 함수 객체 사용
    int count = std::count_if(v.begin(), v.end(), gt_obj);
    std::cout << "Elements greater than 7: " << count << std::endl; // 출력: Elements greater than 7: 2

    return 0;
}
```

STL은 템플릿을 사용하여 구현되었기 때문에, 다양한 데이터 타입에 대해 동일한 코드를 재사용할 수 있는 일반화 프로그래밍(Generic Programming) 패러다임을 따릅니다. 이는 C++98 표준의 일부로 채택되었으며, 현대 C++ 프로그래밍에서 필수적인 부분입니다.

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
