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