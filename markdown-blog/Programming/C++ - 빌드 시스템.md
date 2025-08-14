---
date: 2025-07-01
tags:
  - C++
aliases:
---

# 빌드 시스템 (Make, CMake)

C++ 프로젝트에서 "Make"와 "CMake"는 모두 빌드 시스템과 관련된 도구입니다. 하지만 역할과 사용 방식에는 중요한 차이가 있습니다.

## Make (메이크)

*   **개념:** Make는 빌드 자동화 도구입니다. 소스 코드를 실행 가능한 프로그램으로 변환하는 컴파일, 링크, 리소스 결합 등의 과정을 자동화합니다.
*   **동작 방식:** `Makefile`이라는 스크립트 파일에 정의된 규칙에 따라 소스 파일을 컴파일하고 빌드합니다. `Makefile`은 파일 간의 종속성을 명시하여 변경된 파일만 재컴파일하도록 하여 빌드 시간을 단축시킵니다 (증분 빌드).
*   **장점:** 간단한 프로젝트에서는 Make를 사용하여 컴파일 및 빌드 작업을 간편하게 관리할 수 있습니다.
*   **단점:** 프로젝트 규모가 커지고 파일 간의 의존성이 복잡해지면 `Makefile`을 직접 작성하고 관리하는 것이 어려워집니다. 또한, 주로 유닉스 계열 운영체제에서 사용됩니다.

### `Makefile` 예시

```makefile
# Makefile 예시

# 컴파일러 설정
CXX = g++

# 컴파일 옵션
CXXFLAGS = -Wall -std=c++17

# 링크 옵션
LDFLAGS =

# 소스 파일
SRCS = main.cpp my_lib.cpp

# 오브젝트 파일 (소스 파일에서 .cpp를 .o로 변경)
OBJS = $(SRCS:.cpp=.o)

# 실행 파일 이름
TARGET = my_program

# 기본 타겟: 모든 오브젝트 파일을 링크하여 실행 파일 생성
all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(OBJS) -o $(TARGET) $(LDFLAGS)

# .cpp 파일을 .o 파일로 컴파일하는 규칙
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# 정리 타겟: 생성된 오브젝트 파일과 실행 파일 삭제
clean:
	rm -f $(OBJS) $(TARGET)

.PHONY: all clean
```

## CMake (씨메이크)

*   **개념:** CMake는 크로스 플랫폼 빌드 시스템 생성기입니다. 직접 빌드를 수행하는 것이 아니라, `Makefile`이나 Visual Studio 프로젝트 파일, Xcode 프로젝트 파일 등 특정 플랫폼에 맞는 빌드 파일을 자동으로 생성해주는 도구입니다.
*   **동작 방식:** `CMakeLists.txt` 파일에 프로젝트의 빌드 설정을 정의하며, CMake는 이 파일을 기반으로 사용자가 지정한 빌드 시스템(예: Make, Ninja, Visual Studio)에 맞는 빌드 파일을 생성합니다. 이렇게 생성된 빌드 파일을 통해 실제 컴파일 및 링크가 이루어집니다.
*   **장점:**
    *   **크로스 플랫폼:** 단일 `CMakeLists.txt` 파일을 사용하여 Windows, Linux, macOS 등 다양한 운영체제에서 프로젝트를 빌드할 수 있습니다.
    *   **컴파일러 독립적:** 특정 컴파일러에 종속되지 않고, 다양한 컴파일러 도구 체인에 대한 빌드 스크립트를 생성할 수 있습니다.
    *   **추상화:** 개발자가 특정 플랫폼의 빌드 방식보다 더 높은 추상화 수준에서 C++ 프로젝트를 빌드하는 방법을 정의할 수 있도록 합니다.
    *   **대규모 프로젝트 관리:** 여러 파일로 구성된 대규모 프로젝트를 관리하고, 다른 프로젝트에서 해당 프로젝트를 사용하는 것을 용이하게 합니다.
    *   **CI/CD 통합:** 테스트 및 빌드를 위한 CI/CD 자동화를 지원합니다.
*   **단점:** `CMakeLists.txt` 작성법을 익혀야 하며, 간단한 프로젝트에는 다소 복잡하게 느껴질 수 있습니다.

### `CMakeLists.txt` 예시

```cmake
# CMakeLists.txt 예시

# CMake의 최소 버전 지정
cmake_minimum_required(VERSION 3.10)

# 프로젝트 이름 지정
project(MyCppProject VERSION 1.0)

# 실행 파일 추가
# add_executable(실행파일이름 소스파일1 소스파일2 ...)
add_executable(my_program main.cpp my_lib.cpp)

# C++ 표준 지정 (예: C++17)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)
set(CMAKE_CXX_EXTENSIONS OFF)

# 라이브러리 추가 (예: Boost 라이브러리 사용 시)
# find_package(Boost COMPONENTS system filesystem REQUIRED)
# target_link_libraries(my_program Boost::system Boost::filesystem)

# 서브디렉토리 추가 (하위 CMakeLists.txt 파일이 있는 경우)
# add_subdirectory(sub_dir)
```

### CMake 빌드 프로세스:

1.  **Configure (구성):** `cmake -S . -B build`와 같은 명령을 통해 CMake는 `CMakeLists.txt` 파일을 읽고 사용 가능한 도구 체인을 검색하여 빌드 파일을 생성합니다. 예를 들어, Unix 시스템에서는 `Makefile`을 생성하고, Visual Studio가 감지되면 `.sln` 파일을 생성합니다.
2.  **Build (빌드):** `make` (Unix) 또는 Visual Studio (Windows)와 같은 명령을 통해 CMake가 생성한 빌드 파일을 실행하여 바이너리를 컴파일하고 링크합니다.

## Make와 CMake의 관계 및 차이점 요약

*   **Make는 빌드 도구**이며, `Makefile`에 정의된 규칙에 따라 소스 코드를 실행 파일로 컴파일하고 링크합니다.
*   **CMake는 빌드 시스템 생성기**이며, `CMakeLists.txt` 파일을 기반으로 Makefiles 또는 Visual Studio 프로젝트 파일과 같은 다른 빌드 시스템을 위한 구성 파일을 생성합니다.
*   즉, CMake는 Make를 포함한 다양한 빌드 도구를 위한 "청사진"을 만드는 역할을 하며, 실제 빌드 작업은 Make와 같은 하위 수준 빌드 도구가 수행합니다.
*   CMake는 크로스 플랫폼 개발에 특히 유용하며, 복잡한 프로젝트의 빌드 프로세스를 단순화하고 표준화하는 데 도움을 줍니다. 반면, Make는 특정 플랫폼에 대한 빌드 스크립트를 직접 작성할 때 사용됩니다.

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