---
date: 2025-06-30
tags:
  - C
aliases:
---
공용체(union)는 여러 멤버 변수들이 **같은 메모리 공간을 공유**하도록 하는 사용자 정의 자료형입니다. 구조체(struct)와 유사하게 여러 타입의 변수들을 하나로 묶을 수 있지만, 구조체는 각 멤버가 독립적인 메모리 공간을 가지는 반면, 공용체는 모든 멤버가 시작 주소를 공유하며, 가장 큰 멤버의 크기만큼 메모리를 할당받습니다.

**주요 특징:**
*   **메모리 공유:** 공용체 내의 모든 멤버는 동일한 메모리 공간을 사용합니다.
*   **크기:** 공용체의 크기는 멤버 중 가장 큰 멤버의 크기와 같습니다.
*   **값 저장:** 한 번에 하나의 멤버만 유효한 값을 가질 수 있습니다. 즉, 특정 멤버에 값을 저장하면 이전에 저장된 다른 멤버의 값은 덮어쓰여집니다.

**선언 방법:**

```c
union UnionName {
    dataType member1;
    dataType member2;
    // ...
};
```

**사용 예시:**

```c
#include <stdio.h>
#include <string.h> // strcpy 함수를 사용하기 위해 필요

union Data {
    int i;
    float f;
    char str[20];
};

int main() {
    union Data data;

    data.i = 10;
    printf("data.i : %d\n", data.i); // 출력: data.i : 10

    data.f = 220.5;
    printf("data.f : %f\n", data.f); // 출력: data.f : 220.5
    // 이 시점에서 data.i의 값은 유효하지 않게 됩니다.

    strcpy(data.str, "C Programming");
    printf("data.str : %s\n", data.str); // 출력: data.str : C Programming
    // 이 시점에서 data.i와 data.f의 값은 유효하지 않게 됩니다.

    // 모든 멤버가 같은 메모리를 공유하므로, 마지막으로 할당된 멤버의 값만 유효합니다.
    printf("data.i : %d\n", data.i);   // 예상치 못한 값 출력 (메모리 오염)
    printf("data.f : %f\n", data.f);   // 예상치 못한 값 출력 (메모리 오염)

    return 0;
}
```

**사용 목적:**
공용체는 주로 메모리를 절약해야 할 때, 또는 여러 데이터 타입 중 **하나만** 사용될 것이 확실할 때 유용하게 사용됩니다. 예를 들어, 특정 상황에 따라 정수, 실수, 문자열 중 하나의 데이터만 저장해야 하는 경우에 활용될 수 있습니다. 또한, 서로 다른 데이터 타입으로 동일한 메모리 영역을 해석해야 할 때도 사용됩니다.

## 공용체의 활용 사례

공용체는 특히 다음과 같은 상황에서 유용하게 사용될 수 있습니다.

### 1. 다양한 타입의 데이터를 저장하는 단일 변수

어떤 변수가 여러 타입의 값을 가질 수 있지만, 특정 시점에는 오직 하나의 타입만 유효한 경우에 공용체를 사용하여 메모리를 절약할 수 있습니다. 예를 들어, 메시지 시스템에서 메시지 내용이 정수, 실수, 문자열 중 하나일 수 있을 때 유용합니다.

```c
#include <stdio.h>
#include <string.h>

enum MessageType {
    INT_MSG,
    FLOAT_MSG,
    STRING_MSG
};

struct Message {
    enum MessageType type;
    union {
        int i_val;
        float f_val;
        char s_val[50];
    } data;
};

void printMessage(struct Message msg) {
    switch (msg.type) {
        case INT_MSG:
            printf("Integer Message: %d\n", msg.data.i_val);
            break;
        case FLOAT_MSG:
            printf("Float Message: %.2f\n", msg.data.f_val);
            break;
        case STRING_MSG:
            printf("String Message: %s\n", msg.data.s_val);
            break;
    }
}

int main() {
    struct Message msg1;
    msg1.type = INT_MSG;
    msg1.data.i_val = 123;
    printMessage(msg1);

    struct Message msg2;
    msg2.type = FLOAT_MSG;
    msg2.data.f_val = 45.67f;
    printMessage(msg2);

    struct Message msg3;
    msg3.type = STRING_MSG;
    strcpy(msg3.data.s_val, "Hello Union!");
    printMessage(msg3);

    return 0;
}
```

### 2. 비트 필드 (Bit Fields)와 함께 사용

공용체는 비트 필드와 함께 사용하여 메모리 레이아웃을 정밀하게 제어하고, 동일한 메모리 영역을 다른 방식으로 해석할 때 유용합니다. 예를 들어, 네트워크 패킷 헤더를 파싱할 때 각 필드가 특정 비트 단위로 정의되어 있을 경우 공용체를 활용할 수 있습니다.

```c
#include <stdio.h>

// 1바이트 데이터를 다른 방식으로 해석
union ByteData {
    unsigned char byte;
    struct {
        unsigned char bit0 : 1;
        unsigned char bit1 : 1;
        unsigned char bit2 : 1;
        unsigned char bit3 : 1;
        unsigned char bit4 : 1;
        unsigned char bit5 : 1;
        unsigned char bit6 : 1;
        unsigned char bit7 : 1;
    } bits;
};

int main() {
    union ByteData data;
    data.byte = 0b10101010; // 170 (십진수)

    printf("Byte value: %d\n", data.byte);
    printf("Bit 0: %d\n", data.bits.bit0);
    printf("Bit 1: %d\n", data.bits.bit1);
    printf("Bit 2: %d\n", data.bits.bit2);
    printf("Bit 3: %d\n", data.bits.bit3);
    printf("Bit 4: %d\n", data.bits.bit4);
    printf("Bit 5: %d\n", data.bits.bit5);
    printf("Bit 6: %d\n", data.bits.bit6);
    printf("Bit 7: %d\n", data.bits.bit7);

    data.bits.bit0 = 1; // 0b10101011 (171)
    printf("\nNew byte value after changing bit0: %d\n", data.byte);

    return 0;
}
```
