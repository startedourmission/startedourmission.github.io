---
date: 2025-07-01
tags:
  - C++
aliases:
---

# 파일 입출력

C++에서 파일 입출력은 `<fstream>` 헤더 파일을 통해 제공되는 클래스들을 사용하여 수행됩니다. 이 클래스들은 `iostream` 라이브러리의 `cin` 및 `cout`과 유사하게 작동하여 친숙하게 사용할 수 있습니다.

주요 파일 스트림 클래스는 다음과 같습니다:
*   **`ofstream`**: 파일에 데이터를 쓰기 위한 출력 파일 스트림입니다. (Output File Stream)
*   **`ifstream`**: 파일에서 데이터를 읽기 위한 입력 파일 스트림입니다. (Input File Stream)
*   **`fstream`**: 파일에서 읽고 쓰는 작업을 모두 수행하기 위한 파일 스트림입니다.

### 파일 입출력의 기본 단계

1.  **헤더 포함**: `<fstream>` 헤더 파일을 프로그램에 포함합니다.
2.  **파일 스트림 객체 선언**: `ofstream`, `ifstream`, 또는 `fstream` 클래스의 객체를 선언합니다.
3.  **파일 열기**: `open()` 멤버 함수를 사용하거나 생성자에서 파일 이름을 지정하여 파일과 스트림 객체를 연결합니다.
    *   `ofstream`으로 파일을 열면, 파일이 이미 존재할 경우 기본적으로 이전 내용이 지워지고 새 내용으로 덮어쓰여집니다.
    *   `ifstream`으로 파일을 열 때, 파일이 존재하지 않으면 `open()` 함수가 실패하고 스트림은 실패 상태가 됩니다.
4.  **데이터 읽기/쓰기**: `<<` (삽입 연산자)를 사용하여 파일에 쓰고, `>>` (추출 연산자)를 사용하여 파일에서 읽습니다. 텍스트 파일의 경우 `getline()` 함수를 사용하여 한 줄씩 읽을 수도 있습니다.
5.  **파일 닫기**: `close()` 멤버 함수를 사용하여 파일을 닫습니다. 파일 스트림 객체가 범위를 벗어나 소멸될 때 자동으로 닫히기도 합니다.

### 예제: 파일에 쓰기 및 파일에서 읽기

다음은 `example.txt`라는 파일에 텍스트를 쓰고, 그 내용을 다시 읽어 콘솔에 출력하는 간단한 C++ 프로그램입니다.

```cpp
#include <iostream> // 콘솔 입출력을 위해
#include <fstream>  // 파일 입출력을 위해
#include <string>   // 문자열 처리를 위해

int main() {
    // 1. 파일에 쓰기 (ofstream 사용)
    std::ofstream outputFile("example.txt"); // example.txt 파일을 쓰기 모드로 엽니다.

    // 파일이 성공적으로 열렸는지 확인
    if (outputFile.is_open()) {
        outputFile << "Hello, C++ File I/O!" << std::endl; // 파일에 문자열을 씁니다.
        outputFile << "This is a second line." << std::endl;
        outputFile.close(); // 파일을 닫습니다.
        std::cout << "Data written to example.txt" << std::endl;
    } else {
        std::cerr << "Error opening file for writing!" << std::endl;
        return 1; // 오류 코드 반환
    }

    // 2. 파일에서 읽기 (ifstream 사용)
    std::ifstream inputFile("example.txt"); // example.txt 파일을 읽기 모드로 엽니다.
    std::string line; // 파일에서 읽은 한 줄을 저장할 변수

    // 파일이 성공적으로 열렸는지 확인
    if (inputFile.is_open()) {
        std::cout << "\nReading from example.txt:" << std::endl;
        while (std::getline(inputFile, line)) {
            std::cout << line << std::endl; // 읽은 줄을 콘솔에 출력합니다.
        }
        inputFile.close(); // 파일을 닫습니다.
    } else {
        std::cerr << "Error opening file for reading!" << std::endl;
        return 1; // 오류 코드 반환
    }

    return 0; // 성공적으로 프로그램 종료
}
```

### 추가 정보

*   **이진 파일 입출력**: 텍스트 파일과 달리 이진 파일은 `write()` 및 `read()` 멤버 함수를 사용하여 데이터를 순차적으로 읽고 씁니다. 이 함수들은 `char*` 타입의 메모리 블록과 읽거나 쓸 바이트 수를 인자로 받습니다.
*   **파일 모드**: `open()` 함수를 사용할 때 두 번째 인자로 파일 모드를 지정할 수 있습니다. 예를 들어, `std::ios::app`는 파일 끝에 내용을 추가하고, `std::ios::binary`는 이진 모드로 파일을 엽니다.
*   **오류 처리**: `is_open()`, `good()`, `fail()`, `eof()`와 같은 멤버 함수를 사용하여 파일 작업의 성공 여부를 확인하고 오류를 처리하는 것이 중요합니다.

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
