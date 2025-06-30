---
date: 2025-06-30
tags:
  - C
aliases:
---

# 구조체

C 언어에서 `구조체(struct)`는 여러 개의 서로 다른 데이터 타입(예: `int`, `char`, `float` 등)을 하나의 논리적인 단위로 묶어서 새로운 사용자 정의 데이터 타입을 생성할 수 있게 해주는 기능입니다. 이는 관련된 데이터를 함께 관리할 때 유용합니다.

**구조체를 사용하는 이유:**

*   **데이터 묶음:** 관련된 여러 정보를 하나의 변수로 묶어 관리할 수 있습니다. 예를 들어, 학생의 이름, 학번, 성적을 하나의 `Student` 구조체로 묶을 수 있습니다.
*   **코드 가독성 및 유지보수성 향상:** 데이터의 의미를 명확히 하고, 코드를 더 체계적으로 만들 수 있습니다.
*   **함수 인자 전달:** 여러 개의 데이터를 함수에 전달할 때, 구조체 변수 하나만 전달하면 되므로 코드가 간결해집니다.

**구조체 선언 방법:**

```c
struct 구조체이름 {
    데이터타입 멤버1;
    데이터타입 멤버2;
    // ...
};
```

**예시:**

```c
#include <stdio.h>
#include <string.h> // strcpy 함수를 사용하기 위해 필요

// 학생 정보를 담는 구조체 선언
struct Student {
    char name[50]; // 이름
    int id;        // 학번
    float score;   // 성적
};

int main() {
    // 1. 구조체 변수 선언
    struct Student student1;

    // 2. 구조체 멤버에 값 할당
    strcpy(student1.name, "김철수"); // 문자열은 strcpy 사용
    student1.id = 2023001;
    student1.score = 95.5;

    // 3. 구조체 멤버 값 출력
    printf("학생 이름: %s\n", student1.name);
    printf("학번: %d\n", student1.id);
    printf("성적: %.1f\n", student1.score);

    // 다른 구조체 변수 선언 및 초기화
    struct Student student2 = {"이영희", 2023002, 88.0};

    printf("\n학생 이름: %s\n", student2.name);
    printf("학번: %d\n", student2.id);
    printf("성적: %.1f\n", student2.score);

    return 0;
}
```

**주요 개념:**

*   **`struct` 키워드:** 구조체를 정의할 때 사용합니다.
*   **구조체 이름:** 구조체를 식별하는 이름입니다 (위 예시에서는 `Student`).
*   **멤버(Member):** 구조체 내부에 선언된 변수들입니다 (위 예시에서는 `name`, `id`, `score`).
*   **구조체 변수:** 선언된 구조체 타입을 사용하여 생성된 실제 변수입니다 (위 예시에서는 `student1`, `student2`).
*   **멤버 접근 연산자 (`.`):** 구조체 변수의 특정 멤버에 접근할 때 사용합니다.

## `typedef`를 이용한 구조체 별칭

`typedef` 키워드를 사용하면 `struct` 키워드를 매번 사용하지 않고도 구조체 타입을 더 간결하게 사용할 수 있습니다.

```c
#include <stdio.h>
#include <string.h>

// typedef를 사용하여 Student 구조체에 대한 별칭 정의
typedef struct {
    char name[50];
    int id;
    float score;
} Student; // 이제 Student는 struct Student와 동일한 타입 이름이 됩니다.

int main() {
    Student s1; // struct Student s1; 대신 Student s1; 사용
    strcpy(s1.name, "박영희");
    s1.id = 2024001;
    s1.score = 92.0;

    printf("Name: %s, ID: %d, Score: %.1f\n", s1.name, s1.id, s1.score);

    return 0;
}
```

## 중첩 구조체 (Nested Structures)

하나의 구조체 안에 다른 구조체를 멤버로 포함할 수 있습니다. 이는 더 복잡하고 계층적인 데이터를 표현할 때 유용합니다.

```c
#include <stdio.h>
#include <string.h>

// 주소 정보를 담는 구조체
struct Address {
    char street[100];
    char city[50];
    char zipcode[10];
};

// 사람 정보를 담는 구조체 (Address 구조체를 멤버로 포함)
struct Person {
    char name[50];
    int age;
    struct Address addr; // Address 구조체 변수
};

int main() {
    struct Person p1;

    strcpy(p1.name, "김민수");
    p1.age = 28;
    strcpy(p1.addr.street, "강남대로 123"); // 중첩 구조체 멤버 접근
    strcpy(p1.addr.city, "서울");
    strcpy(p1.addr.zipcode, "06130");

    printf("Name: %s\n", p1.name);
    printf("Age: %d\n", p1.age);
    printf("Address: %s, %s, %s\n", p1.addr.street, p1.addr.city, p1.addr.zipcode);

    return 0;
}
```

## 구조체 배열 (Array of Structures)

동일한 구조체 타입의 여러 객체를 배열 형태로 저장할 수 있습니다. 이는 여러 개의 레코드를 관리할 때 유용합니다.

```c
#include <stdio.h>
#include <string.h>

struct Book {
    char title[100];
    char author[50];
    int year;
};

int main() {
    // Book 구조체 3개를 저장할 배열 선언 및 초기화
    struct Book library[3] = {
        {"The Great Gatsby", "F. Scott Fitzgerald", 1925},
        {"1984", "George Orwell", 1949},
        {"To Kill a Mockingbird", "Harper Lee", 1960}
    };

    // 배열 순회 및 출력
    for (int i = 0; i < 3; i++) {
        printf("Book %d:\n", i + 1);
        printf("  Title: %s\n", library[i].title);
        printf("  Author: %s\n", library[i].author);
        printf("  Year: %d\n", library[i].year);
    }

    return 0;
}
```

---
 기본 문법
 - [[C - 개요]]
 - [[C - 자료형]]
 - [[C - 변수]]
 - [[C - 조건문]]
 - [[C - 반복문]]
 - [[C - 함수]]

심화 문법
 - [[C - 구조체]]
 - [[C - 공용체]]
 - [[C - 열거형]]
 - [[C - 전처리기]]

 포인터
 - [[C - 포인터의 기본]]
 - [[C - 배열과 포인터]]
 - [[C - 함수 포인터]]
 - [[C - 구조체 포인터]]

 기타
 - [[C - 컴파일과 링크]]
 - [[C - IDE]]
 - [[C - 헤더 파일]]
 - [[C - 현대 C 언어와 C23 표준]]
 - [[C - 실무에서 사용하는 C 언어의 변형]]

```