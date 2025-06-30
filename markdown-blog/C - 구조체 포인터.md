---
date: 2025-06-30
tags:
  - C
aliases:
---

# 구조체 포인터

C 언어에서 구조체 포인터는 구조체 변수의 메모리 주소를 저장하는 포인터입니다. 이를 통해 구조체 멤버에 간접적으로 접근할 수 있습니다.

주요 내용은 다음과 같습니다:

1.  **구조체 포인터 선언**:
    ```c
    struct 구조체이름 *포인터변수이름;
    ```
    예시: `struct Person *ptrPerson;`

2.  **구조체 포인터 초기화**:
    *   **기존 구조체 변수의 주소 할당**:
        ```c
        struct Person p1;
        struct Person *ptrPerson = &p1;
        ```
    *   **동적 메모리 할당**: `malloc` 함수를 사용하여 구조체 크기만큼 메모리를 할당하고, 그 주소를 포인터에 저장합니다.
        ```c
        #include <stdlib.h> // malloc, free 사용을 위해 필요

        struct Person *ptrPerson = (struct Person *)malloc(sizeof(struct Person));
        // 메모리 사용 후에는 반드시 free()로 해제해야 합니다.
        // free(ptrPerson);
        ```

3.  **구조체 멤버 접근**:
    구조체 포인터를 통해 멤버에 접근할 때는 `.` (점) 연산자 대신 `->` (화살표) 연산자를 사용합니다.
    ```c
    // 구조체 정의
    struct Person {
        char name[50];
        int age;
    };

    // ... (포인터 초기화 후)

    // 멤버 접근 예시
    strcpy(ptrPerson->name, "홍길동"); // 문자열 복사
    ptrPerson->age = 30;

    // 또는 (*ptrPerson).name, (*ptrPerson).age 와 같이 괄호를 사용하여 역참조 후 접근할 수도 있지만,
    // -> 연산자가 더 일반적이고 가독성이 좋습니다.
    ```

**예시 코드**:

```c
#include <stdio.h>
#include <stdlib.h> // malloc, free 사용을 위해
#include <string.h> // strcpy 사용을 위해

// 구조체 정의
struct Student {
    int id;
    char name[50];
    float score;
};

int main() {
    // 1. 구조체 변수 선언 및 초기화
    struct Student s1 = {101, "김철수", 85.5};

    // 2. 구조체 포인터 선언
    struct Student *ptrStudent;

    // 3. 포인터에 s1의 주소 할당
    ptrStudent = &s1;

    printf("--- 기존 구조체 변수 s1의 주소를 사용한 접근 ---\n");
    printf("ID: %d\n", ptrStudent->id);
    printf("Name: %s\n", ptrStudent->name);
    printf("Score: %.2f\n", ptrStudent->score);

    // 포인터를 통해 멤버 값 변경
    ptrStudent->score = 90.0;
    printf("\n--- 점수 변경 후 ---\n");
    printf("New Score (via pointer): %.2f\n", ptrStudent->score);
    printf("New Score (via s1): %.2f\n", s1.score); // s1의 값도 변경됨

    // 4. 동적 메모리 할당을 통한 구조체 포인터 사용
    struct Student *newStudent = (struct Student *)malloc(sizeof(struct Student));

    if (newStudent == NULL) {
        printf("메모리 할당 실패!\n");
        return 1; // 에러 코드 반환
    }

    // 동적으로 할당된 메모리에 값 할당
    newStudent->id = 202;
    strcpy(newStudent->name, "이영희");
    newStudent->score = 95.0;

    printf("\n--- 동적 할당된 구조체 포인터를 사용한 접근 ---\n");
    printf("ID: %d\n", newStudent->id);
    printf("Name: %s\n", newStudent->name);
    printf("Score: %.2f\n", newStudent->score);

    // 5. 동적으로 할당된 메모리 해제
    free(newStudent);
    newStudent = NULL; // 해제된 포인터가 댕글링 포인터가 되는 것을 방지

    return 0;
}
```

## 동적 할당된 구조체 배열

`malloc`을 사용하여 구조체 배열을 동적으로 할당할 수 있습니다. 이는 런타임에 필요한 만큼의 구조체 객체를 생성할 때 유용합니다.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Person {
    char name[50];
    int age;
};

int main() {
    struct Person *people;
    int num_people = 3;

    // Person 구조체 3개를 저장할 메모리 동적 할당
    people = (struct Person *)malloc(num_people * sizeof(struct Person));

    if (people == NULL) {
        printf("메모리 할당 실패!\n");
        return 1;
    }

    // 배열처럼 접근하여 값 할당
    strcpy(people[0].name, "Alice");
    people[0].age = 30;

    strcpy(people[1].name, "Bob");
    people[1].age = 25;

    strcpy(people[2].name, "Charlie");
    people[2].age = 35;

    // 값 출력
    for (int i = 0; i < num_people; i++) {
        printf("Name: %s, Age: %d\n", people[i].name, people[i].age);
    }

    // 동적 할당된 메모리 해제
    free(people);
    people = NULL;

    return 0;
}
```

## 포인터를 이용한 연결 리스트 (Linked List) 개념

연결 리스트는 노드(Node)들이 포인터를 통해 연결되어 있는 자료구조입니다. 각 노드는 데이터와 다음 노드를 가리키는 포인터(self-referential structure)를 포함합니다. 구조체 포인터는 이러한 연결 리스트를 구현하는 데 필수적입니다.

```c
#include <stdio.h>
#include <stdlib.h>

// 노드 구조체 정의
struct Node {
    int data;
    struct Node *next; // 다음 노드를 가리키는 포인터
};

int main() {
    // 첫 번째 노드 생성
    struct Node *head = (struct Node *)malloc(sizeof(struct Node));
    head->data = 10;
    head->next = NULL; // 아직 다음 노드가 없음

    // 두 번째 노드 생성 및 연결
    struct Node *second = (struct Node *)malloc(sizeof(struct Node));
    second->data = 20;
    second->next = NULL;
    head->next = second; // 첫 번째 노드가 두 번째 노드를 가리키도록 연결

    // 리스트 순회 및 출력
    struct Node *current = head;
    while (current != NULL) {
        printf("Node data: %d\n", current->data);
        current = current->next; // 다음 노드로 이동
    }

    // 메모리 해제 (실제 연결 리스트에서는 모든 노드를 순회하며 해제해야 함)
    free(head);
    free(second);

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
