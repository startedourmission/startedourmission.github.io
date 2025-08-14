---
date: 2025-06-30
tags:
  - C++
aliases:
---

# 현대 C++

C++는 지속적으로 발전하는 언어로, 몇 년마다 새로운 표준이 발표되어 새로운 기능과 개선 사항을 도입합니다. 다음은 C++11, C++14, C++17, C++20, C++23의 주요 특징입니다.

## C++11 (2011년 발표)
C++11은 C++ 언어에 혁신적인 변화를 가져온 주요 업데이트로, 현대 C++ 프로그래밍의 기반이 되었습니다.

*   **이동 시맨틱 (Move Semantics) 및 Rvalue 참조 (Rvalue References):** 불필요한 복사를 줄여 성능을 향상시킵니다.
    ```cpp
    #include <iostream>
    #include <vector>
    #include <string>

    void print_vector(std::vector<int> v) {
        for (int x : v) {
            std::cout << x << " ";
        }
        std::cout << std::endl;
    }

    int main() {
        std::vector<int> original = {1, 2, 3};
        std::vector<int> moved = std::move(original); // 이동
        print_vector(moved); // 출력: 1 2 3
        // original은 유효하지만, 내용은 이동되었을 수 있음 (상태는 정의되지 않음)
        return 0;
    }
    ```

*   **람다 표현식 (Lambda Expressions):** 익명 함수를 코드 내에서 직접 정의할 수 있게 하여 간결하고 유연한 코드를 작성할 수 있도록 합니다.
    ```cpp
    #include <iostream>
    #include <vector>
    #include <algorithm>

    int main() {
        std::vector<int> nums = {1, 2, 3, 4, 5};
        int factor = 10;
        // 람다 표현식: [캡처](매개변수) -> 반환타입 { 본문 }
        std::for_each(nums.begin(), nums.end(), [factor](int n) {
            std::cout << n * factor << " ";
        }); // 출력: 10 20 30 40 50
        std::cout << std::endl;
        return 0;
    }
    ```

*   **`auto` 키워드:** 변수의 타입을 컴파일러가 자동으로 추론하게 하여 코드 작성의 편의성을 높입니다.
    ```cpp
    #include <iostream>
    #include <vector>

    int main() {
        auto i = 10; // int
        auto d = 3.14; // double
        auto v = std::vector<int>{1, 2, 3}; // std::vector<int>

        std::cout << "i: " << i << ", d: " << d << std::endl;
        for (auto& elem : v) { // 범위 기반 for 루프와 함께 사용
            std::cout << elem << " ";
        }
        std::cout << std::endl;
        return 0;
    }
    ```

*   **`nullptr`:** 널 포인터를 명확하게 나타내는 키워드로, 기존의 `NULL` 매크로 사용으로 인한 타입 관련 모호성을 해결합니다.
    ```cpp
    #include <iostream>

    void func(int* p) { std::cout << "int* 버전" << std::endl; }
    void func(std::nullptr_t p) { std::cout << "nullptr_t 버전" << std::endl; }

    int main() {
        func(nullptr); // nullptr_t 버전 호출
        // func(NULL); // 컴파일러에 따라 int* 버전이 호출될 수 있음 (모호성)
        return 0;
    }
    ```

*   **범위 기반 `for` 루프 (Range-based for loop):** 컨테이너의 요소를 쉽게 순회할 수 있도록 합니다.
    ```cpp
    #include <iostream>
    #include <vector>

    int main() {
        std::vector<int> nums = {10, 20, 30, 40, 50};
        for (int n : nums) { // 각 요소를 n에 복사
            std::cout << n << " ";
        }
        std::cout << std::endl;

        for (int& n : nums) { // 각 요소를 참조로 접근 (수정 가능)
            n *= 2;
        }
        for (int n : nums) {
            std::cout << n << " ";
        } // 출력: 20 40 60 80 100
        std::cout << std::endl;
        return 0;
    }
    ```

*   **스마트 포인터 (Smart Pointers):** `std::unique_ptr`, `std::shared_ptr` 등을 도입하여 메모리 관리를 자동화하고 메모리 누수를 방지합니다.
    ```cpp
    #include <iostream>
    #include <memory> // unique_ptr, shared_ptr

    int main() {
        // unique_ptr: 단독 소유권
        std::unique_ptr<int> u_ptr = std::make_unique<int>(100);
        std::cout << "Unique ptr value: " << *u_ptr << std::endl;

        // shared_ptr: 공유 소유권
        std::shared_ptr<int> s_ptr = std::make_shared<int>(200);
        std::shared_ptr<int> s_ptr2 = s_ptr;
        std::cout << "Shared ptr value: " << *s_ptr << ", count: " << s_ptr.use_count() << std::endl;
        return 0;
    }
    ```

*   **동시성 지원 (Concurrency Support):** `std::thread`, `std::mutex` 등 멀티스레딩을 위한 라이브러리 지원을 추가했습니다.
    ```cpp
    #include <iostream>
    #include <thread>
    #include <mutex>

    std::mutex mtx;
    void print_message(int id) {
        std::lock_guard<std::mutex> lock(mtx);
        std::cout << "Hello from thread " << id << std::endl;
    }

    int main() {
        std::thread t1(print_message, 1);
        std::thread t2(print_message, 2);
        t1.join();
        t2.join();
        return 0;
    }
    ```

*   **`constexpr`:** 컴파일 타임에 평가될 수 있는 함수나 변수를 지정하여 성능을 최적화합니다.
    ```cpp
    #include <iostream>

    constexpr int factorial(int n) {
        return (n <= 1) ? 1 : (n * factorial(n - 1));
    }

    int main() {
        constexpr int result = factorial(5); // 컴파일 타임에 계산
        std::cout << "Factorial of 5: " << result << std::endl; // 출력: 120
        return 0;
    }
    ```

*   **초기화 리스트 (Initializer Lists):** 중괄호를 사용하여 객체를 통일된 방식으로 초기화할 수 있도록 합니다.
    ```cpp
    #include <iostream>
    #include <vector>

    int main() {
        std::vector<int> v = {1, 2, 3, 4, 5}; // 초기화 리스트 사용
        for (int n : v) {
            std::cout << n << " ";
        }
        std::cout << std::endl;

        class Point {
        public:
            int x, y;
            Point(int px, int py) : x(px), y(py) {}
        };
        Point p = {10, 20}; // 집합체 초기화 (C++11부터 가능)
        std::cout << "Point: (" << p.x << ", " << p.y << ")" << std::endl;
        return 0;
    }
    ```

## C++14 (2014년 발표)
C++14는 C++11의 확장으로, 주로 C++11의 기능을 개선하고 새로운 작은 기능들을 추가했습니다.

*   **일반화된 람다 (Generic Lambdas):** `auto`를 사용하여 람다 매개변수의 타입을 추론할 수 있게 합니다.
    ```cpp
    #include <iostream>

    int main() {
        auto add = [](auto a, auto b) { return a + b; };
        std::cout << add(1, 2) << std::endl; // 출력: 3
        std::cout << add(1.5, 2.5) << std::endl; // 출력: 4
        return 0;
    }
    ```

*   **람다 캡처 초기화 (Lambda Capture Initializers):** 람다 캡처 시 임의의 표현식으로 초기화할 수 있게 합니다.
    ```cpp
    #include <iostream>

    int main() {
        int x = 10;
        auto lambda = [y = x * 2]() { // y를 x * 2로 초기화하여 캡처
            std::cout << "y: " << y << std::endl;
        };
        lambda(); // 출력: y: 20
        return 0;
    }
    ```

*   **함수 반환 타입 추론 (Function Return Type Deduction):** 일반 함수에서도 `auto`를 사용하여 반환 타입을 추론할 수 있게 합니다.
    ```cpp
    #include <iostream>

    auto multiply(int a, int b) {
        return a * b; // int 타입으로 추론
    }

    int main() {
        std::cout << multiply(3, 4) << std::endl; // 출력: 12
        return 0;
    }
    ```

*   **`decltype(auto)`:** `auto`와 `decltype`의 조합으로, 복잡한 타입 추론을 더 유연하게 만듭니다. 특히 참조를 유지할 때 유용합니다.
    ```cpp
    #include <iostream>

    int global_var = 100;

    decltype(auto) get_global_var() {
        return global_var; // int&로 추론
    }

    int main() {
        decltype(auto) ref = get_global_var();
        ref = 200;
        std::cout << "global_var: " << global_var << std::endl; // 출력: 200
        return 0;
    }
    ```

*   **`constexpr` 함수의 제약 완화:** `constexpr` 함수 내에서 더 많은 종류의 문(statement)을 사용할 수 있게 합니다.
    ```cpp
    #include <iostream>

    constexpr int sum_up_to(int n) {
        int sum = 0;
        for (int i = 1; i <= n; ++i) { // C++14부터 constexpr 함수 내에서 루프 가능
            sum += i;
        }
        return sum;
    }

    int main() {
        constexpr int result = sum_up_to(10); // 컴파일 타임에 계산
        std::cout << "Sum up to 10: " << result << std::endl; // 출력: 55
        return 0;
    }
    ```

*   **`std::make_unique`:** `std::unique_ptr`를 생성하는 편리한 방법을 제공합니다.
    ```cpp
    #include <iostream>
    #include <memory>

    int main() {
        auto u_ptr = std::make_unique<int>(42); // new int(42) 대신
        std::cout << *u_ptr << std::endl; // 출력: 42
        return 0;
    }
    ```

## C++17 (2017년 발표)
C++17은 언어와 라이브러리 모두에 걸쳐 다양한 개선 사항을 도입했습니다.

*   **구조적 바인딩 (Structured Bindings):** 배열, 구조체, `std::pair`, `std::tuple` 등의 요소를 여러 변수로 쉽게 분해할 수 있게 합니다.
    ```cpp
    #include <iostream>
    #include <string>
    #include <tuple>

    struct Person {
        std::string name;
        int age;
    };

    int main() {
        Person p = {"Alice", 30};
        auto [name, age] = p; // 구조적 바인딩
        std::cout << "Name: " << name << ", Age: " << age << std::endl; // 출력: Name: Alice, Age: 30

        std::tuple<int, double, char> t = {1, 2.5, 'A'};
        auto [i, d, c] = t;
        std::cout << "Tuple: " << i << ", " << d << ", " << c << std::endl;
        return 0;
    }
    ```

*   **`if` 및 `switch` 문 내 초기화 (Initialization in if/switch statements):** 조건문 내에서 변수를 선언하고 초기화할 수 있게 합니다.
    ```cpp
    #include <iostream>
    #include <vector>

    int main() {
        std::vector<int> v = {1, 2, 3, 4, 5};
        if (const auto it = std::find(v.begin(), v.end(), 3); it != v.end()) {
            std::cout << "Found: " << *it << std::endl; // 출력: Found: 3
        } else {
            std::cout << "Not found" << std::endl;
        }
        return 0;
    }
    ```

*   **`constexpr if`:** 컴파일 타임에 조건에 따라 코드 블록을 선택적으로 컴파일할 수 있게 합니다.
    ```cpp
    #include <iostream>
    #include <type_traits>

    template <typename T>
    void process(T val) {
        if constexpr (std::is_integral_v<T>) { // T가 정수 타입이면
            std::cout << "Processing integral: " << val * 2 << std::endl;
        } else if constexpr (std::is_floating_point_v<T>) { // T가 부동 소수점 타입이면
            std::cout << "Processing floating point: " << val * 3.0 << std::endl;
        } else {
            std::cout << "Processing other type." << std::endl;
        }
    }

    int main() {
        process(10);   // 출력: Processing integral: 20
        process(3.14); // 출력: Processing floating point: 9.42
        process("hello"); // 출력: Processing other type.
        return 0;
    }
    ```

*   **중첩된 네임스페이스 (Nested Namespaces):** `namespace A::B { ... }`와 같이 중첩된 네임스페이스를 간결하게 정의할 수 있습니다.
    ```cpp
    #include <iostream>

    namespace MyProject::Networking {
        void connect() {
            std::cout << "Connecting to network..." << std::endl;
        }
    }

    int main() {
        MyProject::Networking::connect(); // 출력: Connecting to network...
        return 0;
    }
    ```

*   **파일 시스템 라이브러리 (`std::filesystem`):** 파일 및 디렉토리 경로를 조작하고 파일 시스템 작업을 수행하는 표준 방법을 제공합니다.
    ```cpp
    #include <iostream>
    #include <filesystem>

    namespace fs = std::filesystem;

    int main() {
        fs::path p = "./my_directory";
        if (!fs::exists(p)) {
            fs::create_directory(p);
            std::cout << "Directory created: " << p << std::endl;
        }
        return 0;
    }
    ```

*   **`std::variant`, `std::optional`, `std::any`:** 다양한 유틸리티 타입을 도입하여 타입 안전성을 높이고 유연한 프로그래밍을 지원합니다.
    ```cpp
    #include <iostream>
    #include <variant> // std::variant
    #include <optional> // std::optional
    #include <any> // std::any

    int main() {
        // std::variant: 여러 타입 중 하나를 저장
        std::variant<int, std::string> v;
        v = 10;
        std::cout << "Variant (int): " << std::get<int>(v) << std::endl; // 출력: 10
        v = "hello";
        std::cout << "Variant (string): " << std::get<std::string>(v) << std::endl; // 출력: hello

        // std::optional: 값이 있을 수도, 없을 수도 있는 경우
        std::optional<int> opt_val;
        if (opt_val) {
            std::cout << "Optional has value: " << *opt_val << std::endl;
        } else {
            std::cout << "Optional has no value." << std::endl; // 출력: Optional has no value.
        }
        opt_val = 100;
        if (opt_val) {
            std::cout << "Optional has value: " << *opt_val << std::endl; // 출력: Optional has value: 100
        }

        // std::any: 어떤 타입의 값이라도 저장 가능 (런타임 타입 검사)
        std::any a;
        a = 10;
        std::cout << "Any (int): " << std::any_cast<int>(a) << std::endl; // 출력: 10
        a = std::string("world");
        std::cout << "Any (string): " << std::any_cast<std::string>(a) << std::endl; // 출력: world
        return 0;
    }
    ```

*   **병렬 알고리즘 (Parallel Algorithms):** STL 알고리즘의 병렬 실행 버전을 제공하여 멀티코어 프로세서의 이점을 활용할 수 있게 합니다.
    ```cpp
    #include <iostream>
    #include <vector>
    #include <algorithm>
    #include <execution> // 병렬 알고리즘을 위해 필요

    int main() {
        std::vector<int> v(1000000);
        // 벡터를 1부터 1000000까지 채움
        std::iota(v.begin(), v.end(), 1);

        // 병렬로 정렬
        std::sort(std::execution::par, v.begin(), v.end(), std::greater<int>());

        std::cout << "First 5 elements (descending): ";
        for (int i = 0; i < 5; ++i) {
            std::cout << v[i] << " ";
        } // 출력: 1000000 999999 999998 999997 999996
        std::cout << std::endl;
        return 0;
    }
    ```

## C++20 (2020년 발표)
C++20은 C++17 이후의 주요 버전으로, 특히 "빅 4"로 불리는 핵심 기능(Concepts, Modules, Coroutines, Ranges)을 포함하여 언어와 라이브러리에 큰 변화를 가져왔습니다.

*   **컨셉트 (Concepts):** 템플릿 매개변수에 대한 제약 조건을 명시적으로 정의하여 컴파일 타임에 더 나은 오류 메시지를 제공하고 템플릿 메타프로그래밍을 단순화합니다.
    ```cpp
    #include <iostream>
    #include <concepts> // std::integral, std::floating_point 등

    // 정수 타입만 허용하는 컨셉트
    template <typename T>
    concept IntegralType = std::is_integral_v<T>;

    template <IntegralType T>
    T add_one(T value) {
        return value + 1;
    }

    int main() {
        std::cout << add_one(5) << std::endl; // 출력: 6
        // add_one(5.5); // 컴파일 오류: IntegralType 컨셉트를 만족하지 않음
        return 0;
    }
    ```

*   **모듈 (Modules):** 헤더 파일의 한계를 극복하고 컴파일 시간을 단축하며, 매크로 오염을 줄여줍니다.
    ```cpp
    // my_module.ixx (모듈 인터페이스 단위)
    export module my_module;

    export int add(int a, int b) {
        return a + b;
    }

    // main.cpp
    import my_module;
    #include <iostream>

    int main() {
        std::cout << my_module::add(10, 20) << std::endl; // 출력: 30
        return 0;
    }
    ```

*   **코루틴 (Coroutines):** 비동기 프로그래밍을 위한 새로운 패러다임을 제공하여 비동기 코드를 동기 코드처럼 작성할 수 있게 합니다.
    ```cpp
    // 코루틴은 복잡하므로 간단한 예시로 대체
    // 실제 사용을 위해서는 <coroutine> 헤더와 비동기 프레임워크가 필요
    #include <iostream>
    #include <coroutine>

    struct MyAwaitable {
        bool await_ready() { return false; }
        void await_suspend(std::coroutine_handle<> h) { h.resume(); }
        void await_resume() {}
    };

    MyAwaitable my_coroutine() {
        std::cout << "Coroutine started" << std::endl;
        co_await MyAwaitable{}; // 일시 중지 및 재개
        std::cout << "Coroutine resumed" << std::endl;
    }

    int main() {
        my_coroutine();
        return 0;
    }
    ```

*   **레인지 (Ranges):** STL 알고리즘을 더욱 유연하고 조합 가능하게 만들어 데이터 시퀀스를 처리하는 새로운 방법을 제공합니다.
    ```cpp
    #include <iostream>
    #include <vector>
    #include <ranges> // std::views
    #include <algorithm>

    int main() {
        std::vector<int> nums = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

        // 짝수만 필터링하고 2배로 변환
        for (int i : nums | std::views::filter([](int n){ return n % 2 == 0; }) | std::views::transform([](int n){ return n * 2; })) {
            std::cout << i << " ";
        } // 출력: 4 8 12 16 20
        std::cout << std::endl;
        return 0;
    }
    ```

*   **삼방 비교 연산자 (`<=>`, "spaceship operator"):** `==`, `!=`, `<`, `<=`, `>`, `>=` 연산자를 한 번에 정의할 수 있게 하여 비교 연산자 오버로딩의 상용구 코드를 줄여줍니다.
    ```cpp
    #include <iostream>
    #include <compare> // std::strong_ordering

    struct Point {
        int x, y;
        // 삼방 비교 연산자
        auto operator<=>(const Point&) const = default;
    };

    int main() {
        Point p1 = {1, 2};
        Point p2 = {1, 2};
        Point p3 = {2, 1};

        if (p1 == p2) { std::cout << "p1 == p2" << std::endl; } // 출력: p1 == p2
        if (p1 < p3) { std::cout << "p1 < p3" << std::endl; } // 출력: p1 < p3
        return 0;
    }
    ```

*   **지정된 초기화 (Designated Initializers):** 구조체나 클래스의 멤버를 이름으로 초기화할 수 있게 합니다.
    ```cpp
    #include <iostream>

    struct Point {
        int x;
        int y;
    };

    int main() {
        Point p = {.x = 10, .y = 20}; // 지정된 초기화
        std::cout << "Point: (" << p.x << ", " << p.y << ")" << std::endl; // 출력: Point: (10, 20)
        return 0;
    }
    ```

*   **`std::span`:** 연속된 메모리 영역을 참조하는 뷰(view)를 제공하여 배열이나 컨테이너의 일부를 안전하고 효율적으로 전달할 수 있게 합니다.
    ```cpp
    #include <iostream>
    #include <span> // std::span
    #include <vector>

    void print_elements(std::span<const int> s) {
        for (int x : s) {
            std::cout << x << " ";
        }
        std::cout << std::endl;
    }

    int main() {
        std::vector<int> v = {1, 2, 3, 4, 5};
        print_elements(v); // 벡터 전체
        print_elements({v.data() + 1, 3}); // 벡터의 일부 (2, 3, 4)
        return 0;
    }
    ```

## C++23 (2023년 발표)
C++23은 C++20만큼 큰 변화는 아니지만, 언어와 라이브러리에 걸쳐 다양한 개선 사항과 새로운 기능을 도입했습니다.

*   **명시적 객체 매개변수 (`deducing this`):** 멤버 함수에서 `this` 포인터를 명시적으로 매개변수로 받을 수 있게 하여, `const` 및 `volatile` 한정자를 더 유연하게 처리하고 재귀 람다를 가능하게 합니다.
    ```cpp
    #include <iostream>

    struct MyClass {
        int value = 10;

        // deducing this를 사용한 멤버 함수
        auto get_value(this auto& self) {
            return self.value;
        }
    };

    int main() {
        MyClass obj;
        const MyClass const_obj;

        std::cout << obj.get_value() << std::endl; // 출력: 10
        std::cout << const_obj.get_value() << std::endl; // 출력: 10 (const 버전 호출)
        return 0;
    }
    ```

*   **`if consteval` 및 `if not consteval`:** 컴파일 타임 평가 컨텍스트를 명확하게 구분하여 코드를 작성할 수 있게 합니다.
    ```cpp
    #include <iostream>

    consteval int compile_time_func(int x) {
        if consteval {
            return x * 2;
        } else {
            return x + 1;
        }
    }

    int main() {
        std::cout << compile_time_func(5) << std::endl; // 컴파일 타임에 5 * 2 = 10 계산
        return 0;
    }
    ```

*   **`std::flat_map`, `std::flat_set`:** `std::map` 및 `std::set`과 유사하지만, 내부적으로 연속된 메모리(예: `std::vector`)를 사용하여 캐시 효율성을 높인 컨테이너를 제공합니다.
    ```cpp
    #include <iostream>
    #include <flat_map> // C++23

    int main() {
        std::flat_map<int, std::string> fm;
        fm.insert({1, "one"});
        fm.insert({2, "two"});
        std::cout << fm[1] << std::endl; // 출력: one
        return 0;
    }
    ```

*   **`std::generator`:** 코루틴을 기반으로 하는 제너레이터 함수를 위한 표준 라이브러리 지원을 제공합니다.
    ```cpp
    #include <iostream>
    #include <generator> // C++23

    std::generator<int> fibonacci() {
        int a = 0, b = 1;
        while (true) {
            co_yield a;
            int next = a + b;
            a = b;
            b = next;
        }
    }

    int main() {
        int count = 0;
        for (int num : fibonacci()) {
            if (count++ >= 10) break;
            std::cout << num << " ";
        } // 출력: 0 1 1 2 3 5 8 13 21 34
        std::cout << std::endl;
        return 0;
    }
    ```

*   **문자열 포맷팅 개선:** `std::format`에 대한 개선 사항을 포함하여 문자열 포맷팅을 더욱 강력하고 유연하게 만듭니다.
    ```cpp
    #include <iostream>
    #include <format> // C++20 (C++23에서 개선)

    int main() {
        std::string s = std::format("Hello, {}! The answer is {}.
", "World", 42);
        std::cout << s; // 출력: Hello, World! The answer is 42.
        return 0;
    }
    ```

*   **`std::expected`:** 오류 처리 메커니즘으로, 성공적인 값 또는 오류를 나타낼 수 있는 타입을 제공하여 예외 처리의 대안을 제시합니다.
    ```cpp
    #include <iostream>
    #include <expected> // C++23
    #include <string>

    std::expected<int, std::string> divide(int a, int b) {
        if (b == 0) {
            return std::unexpected("Division by zero");
        }
        return a / b;
    }

    int main() {
        auto result1 = divide(10, 2);
        if (result1.has_value()) {
            std::cout << "Result: " << result1.value() << std::endl; // 출력: Result: 5
        } else {
            std::cout << "Error: " << result1.error() << std::endl;
        }

        auto result2 = divide(10, 0);
        if (result2.has_value()) {
            std::cout << "Result: " << result2.value() << std::endl;
        } else {
            std::cout << "Error: " << result2.error() << std::endl; // 출력: Error: Division by zero
        }
        return 0;
    }
    ```

*   **`std::mdspan`:** 다차원 배열을 위한 뷰를 제공하여 다차원 데이터에 대한 효율적인 접근을 가능하게 합니다.
    ```cpp
    #include <iostream>
    #include <vector>
    #include <mdspan> // C++23

    int main() {
        std::vector<int> data = {1, 2, 3, 4, 5, 6};
        // 2x3 행렬 뷰 생성
        std::mdspan<int, std::dextents<size_t, 2>> m(data.data(), 2, 3);

        std::cout << m[0, 0] << " " << m[0, 1] << " " << m[0, 2] << std::endl; // 출력: 1 2 3
        std::cout << m[1, 0] << " " << m[1, 1] << " " << m[1, 2] << std::endl; // 출력: 4 5 6
        return 0;
    }
    ```

*   **표준 라이브러리 모듈 (`std` 및 `std.compat`):** 표준 라이브러리를 모듈로 제공하여 컴파일 시간을 단축하고 모듈화된 프로그래밍을 지원합니다.
    ```cpp
    // main.cpp
    import std; // C++23

    int main() {
        std::cout << "Hello, C++23 Modules!" << std::endl;
        std::vector<int> v = {1, 2, 3};
        std::println("{}", v); // C++23의 std::println
        return 0;
    }
    ```

---
date: 2025-06-30
tags:
  - C++
aliases:
---

# 현대 C++

C++는 지속적으로 발전하는 언어로, 몇 년마다 새로운 표준이 발표되어 새로운 기능과 개선 사항을 도입합니다. 다음은 C++11, C++14, C++17, C++20, C++23의 주요 특징입니다.

## C++11 (2011년 발표)
C++11은 C++ 언어에 혁신적인 변화를 가져온 주요 업데이트로, 현대 C++ 프로그래밍의 기반이 되었습니다.

*   **이동 시맨틱 (Move Semantics) 및 Rvalue 참조 (Rvalue References):** 불필요한 복사를 줄여 성능을 향상시킵니다.
    ```cpp
    #include <iostream>
    #include <vector>
    #include <string>

    void print_vector(std::vector<int> v) {
        for (int x : v) {
            std::cout << x << " ";
        }
        std::cout << std::endl;
    }

    int main() {
        std::vector<int> original = {1, 2, 3};
        std::vector<int> moved = std::move(original); // 이동
        print_vector(moved); // 출력: 1 2 3
        // original은 유효하지만, 내용은 이동되었을 수 있음 (상태는 정의되지 않음)
        return 0;
    }
    ```

*   **람다 표현식 (Lambda Expressions):** 익명 함수를 코드 내에서 직접 정의할 수 있게 하여 간결하고 유연한 코드를 작성할 수 있도록 합니다.
    ```cpp
    #include <iostream>
    #include <vector>
    #include <algorithm>

    int main() {
        std::vector<int> nums = {1, 2, 3, 4, 5};
        int factor = 10;
        // 람다 표현식: [캡처](매개변수) -> 반환타입 { 본문 }
        std::for_each(nums.begin(), nums.end(), [factor](int n) {
            std::cout << n * factor << " ";
        }); // 출력: 10 20 30 40 50
        std::cout << std::endl;
        return 0;
    }
    ```

*   **`auto` 키워드:** 변수의 타입을 컴파일러가 자동으로 추론하게 하여 코드 작성의 편의성을 높입니다.
    ```cpp
    #include <iostream>
    #include <vector>

    int main() {
        auto i = 10; // int
        auto d = 3.14; // double
        auto v = std::vector<int>{1, 2, 3}; // std::vector<int>

        std::cout << "i: " << i << ", d: " << d << std::endl;
        for (auto& elem : v) { // 범위 기반 for 루프와 함께 사용
            std::cout << elem << " ";
        }
        std::cout << std::endl;
        return 0;
    }
    ```

*   **`nullptr`:** 널 포인터를 명확하게 나타내는 키워드로, 기존의 `NULL` 매크로 사용으로 인한 타입 관련 모호성을 해결합니다.
    ```cpp
    #include <iostream>

    void func(int* p) { std::cout << "int* 버전" << std::endl; }
    void func(std::nullptr_t p) { std::cout << "nullptr_t 버전" << std::endl; }

    int main() {
        func(nullptr); // nullptr_t 버전 호출
        // func(NULL); // 컴파일러에 따라 int* 버전이 호출될 수 있음 (모호성)
        return 0;
    }
    ```

*   **범위 기반 `for` 루프 (Range-based for loop):** 컨테이너의 요소를 쉽게 순회할 수 있도록 합니다.
    ```cpp
    #include <iostream>
    #include <vector>

    int main() {
        std::vector<int> nums = {10, 20, 30, 40, 50};
        for (int n : nums) { // 각 요소를 n에 복사
            std::cout << n << " ";
        }
        std::cout << std::endl;

        for (int& n : nums) { // 각 요소를 참조로 접근 (수정 가능)
            n *= 2;
        }
        for (int n : nums) {
            std::cout << n << " ";
        } // 출력: 20 40 60 80 100
        std::cout << std::endl;
        return 0;
    }
    ```

*   **스마트 포인터 (Smart Pointers):** `std::unique_ptr`, `std::shared_ptr` 등을 도입하여 메모리 관리를 자동화하고 메모리 누수를 방지합니다.
    ```cpp
    #include <iostream>
    #include <memory> // unique_ptr, shared_ptr

    int main() {
        // unique_ptr: 단독 소유권
        std::unique_ptr<int> u_ptr = std::make_unique<int>(100);
        std::cout << "Unique ptr value: " << *u_ptr << std::endl;

        // shared_ptr: 공유 소유권
        std::shared_ptr<int> s_ptr = std::make_shared<int>(200);
        std::shared_ptr<int> s_ptr2 = s_ptr;
        std::cout << "Shared ptr value: " << *s_ptr << ", count: " << s_ptr.use_count() << std::endl;
        return 0;
    }
    ```

*   **동시성 지원 (Concurrency Support):** `std::thread`, `std::mutex` 등 멀티스레딩을 위한 라이브러리 지원을 추가했습니다.
    ```cpp
    #include <iostream>
    #include <thread>
    #include <mutex>

    std::mutex mtx;
    void print_message(int id) {
        std::lock_guard<std::mutex> lock(mtx);
        std::cout << "Hello from thread " << id << std::endl;
    }

    int main() {
        std::thread t1(print_message, 1);
        std::thread t2(print_message, 2);
        t1.join();
        t2.join();
        return 0;
    }
    ```

*   **`constexpr`:** 컴파일 타임에 평가될 수 있는 함수나 변수를 지정하여 성능을 최적화합니다.
    ```cpp
    #include <iostream>

    constexpr int factorial(int n) {
        return (n <= 1) ? 1 : (n * factorial(n - 1));
    }

    int main() {
        constexpr int result = factorial(5); // 컴파일 타임에 계산
        std::cout << "Factorial of 5: " << result << std::endl; // 출력: 120
        return 0;
    }
    ```

*   **초기화 리스트 (Initializer Lists):** 중괄호를 사용하여 객체를 통일된 방식으로 초기화할 수 있도록 합니다.
    ```cpp
    #include <iostream>
    #include <vector>

    int main() {
        std::vector<int> v = {1, 2, 3, 4, 5}; // 초기화 리스트 사용
        for (int n : v) {
            std::cout << n << " ";
        }
        std::cout << std::endl;

        class Point {
        public:
            int x, y;
            Point(int px, int py) : x(px), y(py) {}
        };
        Point p = {10, 20}; // 집합체 초기화 (C++11부터 가능)
        std::cout << "Point: (" << p.x << ", " << p.y << ")" << std::endl;
        return 0;
    }
    ```

## C++14 (2014년 발표)
C++14는 C++11의 확장으로, 주로 C++11의 기능을 개선하고 새로운 작은 기능들을 추가했습니다.

*   **일반화된 람다 (Generic Lambdas):** `auto`를 사용하여 람다 매개변수의 타입을 추론할 수 있게 합니다.
    ```cpp
    #include <iostream>

    int main() {
        auto add = [](auto a, auto b) { return a + b; };
        std::cout << add(1, 2) << std::endl; // 출력: 3
        std::cout << add(1.5, 2.5) << std::endl; // 출력: 4
        return 0;
    }
    ```

*   **람다 캡처 초기화 (Lambda Capture Initializers):** 람다 캡처 시 임의의 표현식으로 초기화할 수 있게 합니다.
    ```cpp
    #include <iostream>

    int main() {
        int x = 10;
        auto lambda = [y = x * 2]() { // y를 x * 2로 초기화하여 캡처
            std::cout << "y: " << y << std::endl;
        };
        lambda(); // 출력: y: 20
        return 0;
    }
    ```

*   **함수 반환 타입 추론 (Function Return Type Deduction):** 일반 함수에서도 `auto`를 사용하여 반환 타입을 추론할 수 있게 합니다.
    ```cpp
    #include <iostream>

    auto multiply(int a, int b) {
        return a * b; // int 타입으로 추론
    }

    int main() {
        std::cout << multiply(3, 4) << std::endl; // 출력: 12
        return 0;
    }
    ```

*   **`decltype(auto)`:** `auto`와 `decltype`의 조합으로, 복잡한 타입 추론을 더 유연하게 만듭니다. 특히 참조를 유지할 때 유용합니다.
    ```cpp
    #include <iostream>

    int global_var = 100;

    decltype(auto) get_global_var() {
        return global_var; // int&로 추론
    }

    int main() {
        decltype(auto) ref = get_global_var();
        ref = 200;
        std::cout << "global_var: " << global_var << std::endl; // 출력: 200
        return 0;
    }
    ```

*   **`constexpr` 함수의 제약 완화:** `constexpr` 함수 내에서 더 많은 종류의 문(statement)을 사용할 수 있게 합니다.
    ```cpp
    #include <iostream>

    constexpr int sum_up_to(int n) {
        int sum = 0;
        for (int i = 1; i <= n; ++i) { // C++14부터 constexpr 함수 내에서 루프 가능
            sum += i;
        }
        return sum;
    }

    int main() {
        constexpr int result = sum_up_to(10); // 컴파일 타임에 계산
        std::cout << "Sum up to 10: " << result << std::endl; // 출력: 55
        return 0;
    }
    ```

*   **`std::make_unique`:** `std::unique_ptr`를 생성하는 편리한 방법을 제공합니다.
    ```cpp
    #include <iostream>
    #include <memory>

    int main() {
        auto u_ptr = std::make_unique<int>(42); // new int(42) 대신
        std::cout << *u_ptr << std::endl; // 출력: 42
        return 0;
    }
    ```

## C++17 (2017년 발표)
C++17은 언어와 라이브러리 모두에 걸쳐 다양한 개선 사항을 도입했습니다.

*   **구조적 바인딩 (Structured Bindings):** 배열, 구조체, `std::pair`, `std::tuple` 등의 요소를 여러 변수로 쉽게 분해할 수 있게 합니다.
    ```cpp
    #include <iostream>
    #include <string>
    #include <tuple>

    struct Person {
        std::string name;
        int age;
    };

    int main() {
        Person p = {"Alice", 30};
        auto [name, age] = p; // 구조적 바인딩
        std::cout << "Name: " << name << ", Age: " << age << std::endl; // 출력: Name: Alice, Age: 30

        std::tuple<int, double, char> t = {1, 2.5, 'A'};
        auto [i, d, c] = t;
        std::cout << "Tuple: " << i << ", " << d << ", " << c << std::endl;
        return 0;
    }
    ```

*   **`if` 및 `switch` 문 내 초기화 (Initialization in if/switch statements):** 조건문 내에서 변수를 선언하고 초기화할 수 있게 합니다.
    ```cpp
    #include <iostream>
    #include <vector>

    int main() {
        std::vector<int> v = {1, 2, 3, 4, 5};
        if (const auto it = std::find(v.begin(), v.end(), 3); it != v.end()) {
            std::cout << "Found: " << *it << std::endl; // 출력: Found: 3
        } else {
            std::cout << "Not found" << std::endl;
        }
        return 0;
    }
    ```

*   **`constexpr if`:** 컴파일 타임에 조건에 따라 코드 블록을 선택적으로 컴파일할 수 있게 합니다.
    ```cpp
    #include <iostream>
    #include <type_traits>

    template <typename T>
    void process(T val) {
        if constexpr (std::is_integral_v<T>) { // T가 정수 타입이면
            std::cout << "Processing integral: " << val * 2 << std::endl;
        } else if constexpr (std::is_floating_point_v<T>) { // T가 부동 소수점 타입이면
            std::cout << "Processing floating point: " << val * 3.0 << std::endl;
        } else {
            std::cout << "Processing other type." << std::endl;
        }
    }

    int main() {
        process(10);   // 출력: Processing integral: 20
        process(3.14); // 출력: Processing floating point: 9.42
        process("hello"); // 출력: Processing other type.
        return 0;
    }
    ```

*   **중첩된 네임스페이스 (Nested Namespaces):** `namespace A::B { ... }`와 같이 중첩된 네임스페이스를 간결하게 정의할 수 있습니다.
    ```cpp
    #include <iostream>

    namespace MyProject::Networking {
        void connect() {
            std::cout << "Connecting to network..." << std::endl;
        }
    }

    int main() {
        MyProject::Networking::connect(); // 출력: Connecting to network...
        return 0;
    }
    ```

*   **파일 시스템 라이브러리 (`std::filesystem`):** 파일 및 디렉토리 경로를 조작하고 파일 시스템 작업을 수행하는 표준 방법을 제공합니다.
    ```cpp
    #include <iostream>
    #include <filesystem>

    namespace fs = std::filesystem;

    int main() {
        fs::path p = "./my_directory";
        if (!fs::exists(p)) {
            fs::create_directory(p);
            std::cout << "Directory created: " << p << std::endl;
        }
        return 0;
    }
    ```

*   **`std::variant`, `std::optional`, `std::any`:** 다양한 유틸리티 타입을 도입하여 타입 안전성을 높이고 유연한 프로그래밍을 지원합니다.
    ```cpp
    #include <iostream>
    #include <variant> // std::variant
    #include <optional> // std::optional
    #include <any> // std::any

    int main() {
        // std::variant: 여러 타입 중 하나를 저장
        std::variant<int, std::string> v;
        v = 10;
        std::cout << "Variant (int): " << std::get<int>(v) << std::endl; // 출력: 10
        v = "hello";
        std::cout << "Variant (string): " << std::get<std::string>(v) << std::endl; // 출력: hello

        // std::optional: 값이 있을 수도, 없을 수도 있는 경우
        std::optional<int> opt_val;
        if (opt_val) {
            std::cout << "Optional has value: " << *opt_val << std::endl;
        } else {
            std::cout << "Optional has no value." << std::endl; // 출력: Optional has no value.
        }
        opt_val = 100;
        if (opt_val) {
            std::cout << "Optional has value: " << *opt_val << std::endl; // 출력: Optional has value: 100
        }

        // std::any: 어떤 타입의 값이라도 저장 가능 (런타임 타입 검사)
        std::any a;
        a = 10;
        std::cout << "Any (int): " << std::any_cast<int>(a) << std::endl; // 출력: 10
        a = std::string("world");
        std::cout << "Any (string): " << std::any_cast<std::string>(a) << std::endl; // 출력: world
        return 0;
    }
    ```

*   **병렬 알고리즘 (Parallel Algorithms):** STL 알고리즘의 병렬 실행 버전을 제공하여 멀티코어 프로세서의 이점을 활용할 수 있게 합니다.
    ```cpp
    #include <iostream>
    #include <vector>
    #include <algorithm>
    #include <execution> // 병렬 알고리즘을 위해 필요

    int main() {
        std::vector<int> v(1000000);
        // 벡터를 1부터 1000000까지 채움
        std::iota(v.begin(), v.end(), 1);

        // 병렬로 정렬
        std::sort(std::execution::par, v.begin(), v.end(), std::greater<int>());

        std::cout << "First 5 elements (descending): ";
        for (int i = 0; i < 5; ++i) {
            std::cout << v[i] << " ";
        }
        std::cout << std::endl; // 출력: 1000000 999999 999998 999997 999996
        std::cout << std::endl;
        return 0;
    }
    ```

## C++20 (2020년 발표)
C++20은 C++17 이후의 주요 버전으로, 특히 "빅 4"로 불리는 핵심 기능(Concepts, Modules, Coroutines, Ranges)을 포함하여 언어와 라이브러리에 큰 변화를 가져왔습니다.

*   **컨셉트 (Concepts):** 템플릿 매개변수에 대한 제약 조건을 명시적으로 정의하여 컴파일 타임에 더 나은 오류 메시지를 제공하고 템플릿 메타프로그래밍을 단순화합니다.
    ```cpp
    #include <iostream>
    #include <concepts> // std::integral, std::floating_point 등

    // 정수 타입만 허용하는 컨셉트
    template <typename T>
    concept IntegralType = std::is_integral_v<T>;

    template <IntegralType T>
    T add_one(T value) {
        return value + 1;
    }

    int main() {
        std::cout << add_one(5) << std::endl; // 출력: 6
        // add_one(5.5); // 컴파일 오류: IntegralType 컨셉트를 만족하지 않음
        return 0;
    }
    ```

*   **모듈 (Modules):** 헤더 파일의 한계를 극복하고 컴파일 시간을 단축하며, 매크로 오염을 줄여줍니다.
    ```cpp
    // my_module.ixx (모듈 인터페이스 단위)
    export module my_module;

    export int add(int a, int b) {
        return a + b;
    }

    // main.cpp
    import my_module;
    #include <iostream>

    int main() {
        std::cout << my_module::add(10, 20) << std::endl; // 출력: 30
        return 0;
    }
    ```

*   **코루틴 (Coroutines):** 비동기 프로그래밍을 위한 새로운 패러다임을 제공하여 비동기 코드를 동기 코드처럼 작성할 수 있게 합니다.
    ```cpp
    // 코루틴은 복잡하므로 간단한 예시로 대체
    // 실제 사용을 위해서는 <coroutine> 헤더와 비동기 프레임워크가 필요
    #include <iostream>
    #include <coroutine>

    struct MyAwaitable {
        bool await_ready() { return false; }
        void await_suspend(std::coroutine_handle<> h) { h.resume(); }
        void await_resume() {}
    };

    MyAwaitable my_coroutine() {
        std::cout << "Coroutine started" << std::endl;
        co_await MyAwaitable{}; // 일시 중지 및 재개
        std::cout << "Coroutine resumed" << std::endl;
    }

    int main() {
        my_coroutine();
        return 0;
    }
    ```

*   **레인지 (Ranges):** STL 알고리즘을 더욱 유연하고 조합 가능하게 만들어 데이터 시퀀스를 처리하는 새로운 방법을 제공합니다.
    ```cpp
    #include <iostream>
    #include <vector>
    #include <ranges> // std::views
    #include <algorithm>

    int main() {
        std::vector<int> nums = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

        // 짝수만 필터링하고 2배로 변환
        for (int i : nums | std::views::filter([](int n){ return n % 2 == 0; }) | std::views::transform([](int n){ return n * 2; })) {
            std::cout << i << " ";
        }
        std::cout << std::endl; // 출력: 4 8 12 16 20
        return 0;
    }
    ```

*   **삼방 비교 연산자 (`<=>`, "spaceship operator"):** `==`, `!=`, `<`, `<=`, `>`, `>=` 연산자를 한 번에 정의할 수 있게 하여 비교 연산자 오버로딩의 상용구 코드를 줄여줍니다.
    ```cpp
    #include <iostream>
    #include <compare> // std::strong_ordering

    struct Point {
        int x, y;
        // 삼방 비교 연산자
        auto operator<=>(const Point&) const = default;
    };

    int main() {
        Point p1 = {1, 2};
        Point p2 = {1, 2};
        Point p3 = {2, 1};

        if (p1 == p2) { std::cout << "p1 == p2" << std::endl; } // 출력: p1 == p2
        if (p1 < p3) { std::cout << "p1 < p3" << std::endl; } // 출력: p1 < p3
        return 0;
    }
    ```

*   **지정된 초기화 (Designated Initializers):** 구조체나 클래스의 멤버를 이름으로 초기화할 수 있게 합니다.
    ```cpp
    #include <iostream>

    struct Point {
        int x;
        int y;
    };

    int main() {
        Point p = {.x = 10, .y = 20}; // 지정된 초기화
        std::cout << "Point: (" << p.x << ", " << p.y << ")" << std::endl; // 출력: Point: (10, 20)
        return 0;
    }
    ```

*   **`std::span`:** 연속된 메모리 영역을 참조하는 뷰(view)를 제공하여 배열이나 컨테이너의 일부를 안전하고 효율적으로 전달할 수 있게 합니다.
    ```cpp
    #include <iostream>
    #include <span> // std::span
    #include <vector>

    void print_elements(std::span<const int> s) {
        for (int x : s) {
            std::cout << x << " ";
        }
        std::cout << std::endl;
    }

    int main() {
        std::vector<int> v = {1, 2, 3, 4, 5};
        print_elements(v); // 벡터 전체
        print_elements({v.data() + 1, 3}); // 벡터의 일부 (2, 3, 4)
        return 0;
    }
    ```

## C++23 (2023년 발표)
C++23은 C++20만큼 큰 변화는 아니지만, 언어와 라이브러리에 걸쳐 다양한 개선 사항과 새로운 기능을 도입했습니다.

*   **명시적 객체 매개변수 (`deducing this`):** 멤버 함수에서 `this` 포인터를 명시적으로 매개변수로 받을 수 있게 하여, `const` 및 `volatile` 한정자를 더 유연하게 처리하고 재귀 람다를 가능하게 합니다.
    ```cpp
    #include <iostream>

    struct MyClass {
        int value = 10;

        // deducing this를 사용한 멤버 함수
        auto get_value(this auto& self) {
            return self.value;
        }
    };

    int main() {
        MyClass obj;
        const MyClass const_obj;

        std::cout << obj.get_value() << std::endl; // 출력: 10
        std::cout << const_obj.get_value() << std::endl; // 출력: 10 (const 버전 호출)
        return 0;
    }
    ```

*   **`if consteval` 및 `if not consteval`:** 컴파일 타임 평가 컨텍스트를 명확하게 구분하여 코드를 작성할 수 있게 합니다.
    ```cpp
    #include <iostream>

    consteval int compile_time_func(int x) {
        if consteval {
            return x * 2;
        } else {
            return x + 1;
        }
    }

    int main() {
        std::cout << compile_time_func(5) << std::endl; // 컴파일 타임에 5 * 2 = 10 계산
        return 0;
    }
    ```

*   **`std::flat_map`, `std::flat_set`:** `std::map` 및 `std::set`과 유사하지만, 내부적으로 연속된 메모리(예: `std::vector`)를 사용하여 캐시 효율성을 높인 컨테이너를 제공합니다.
    ```cpp
    #include <iostream>
    #include <flat_map> // C++23

    int main() {
        std::flat_map<int, std::string> fm;
        fm.insert({1, "one"});
        fm.insert({2, "two"});
        std::cout << fm[1] << std::endl; // 출력: one
        return 0;
    }
    ```

*   **`std::generator`:** 코루틴을 기반으로 하는 제너레이터 함수를 위한 표준 라이브러리 지원을 제공합니다.
    ```cpp
    #include <iostream>
    #include <generator> // C++23

    std::generator<int> fibonacci() {
        int a = 0, b = 1;
        while (true) {
            co_yield a;
            int next = a + b;
            a = b;
            b = next;
        }
    }

    int main() {
        int count = 0;
        for (int num : fibonacci()) {
            if (count++ >= 10) break;
            std::cout << num << " ";
        }
        std::cout << std::endl;
        return 0;
    }
    ```

*   **문자열 포맷팅 개선:** `std::format`에 대한 개선 사항을 포함하여 문자열 포맷팅을 더욱 강력하고 유연하게 만듭니다.
    ```cpp
    #include <iostream>
    #include <format> // C++20 (C++23에서 개선)

    int main() {
        std::string s = std::format("Hello, {}! The answer is {}.
", "World", 42);
        std::cout << s; // 출력: Hello, World! The answer is 42.
        return 0;
    }
    ```

*   **`std::expected`:** 오류 처리 메커니즘으로, 성공적인 값 또는 오류를 나타낼 수 있는 타입을 제공하여 예외 처리의 대안을 제시합니다.
    ```cpp
    #include <iostream>
    #include <expected> // C++23
    #include <string>

    std::expected<int, std::string> divide(int a, int b) {
        if (b == 0) {
            return std::unexpected("Division by zero");
        }
        return a / b;
    }

    int main() {
        auto result1 = divide(10, 2);
        if (result1.has_value()) {
            std::cout << "Result: " << result1.value() << std::endl; // 출력: Result: 5
        } else {
            std::cout << "Error: " << result1.error() << std::endl;
        }

        auto result2 = divide(10, 0);
        if (result2.has_value()) {
            std::cout << "Result: " << result2.value() << std::endl;
        } else {
            std::cout << "Error: " << result2.error() << std::endl; // 출력: Error: Division by zero
        }
        return 0;
    }
    ```

*   **`std::mdspan`:** 다차원 배열을 위한 뷰를 제공하여 다차원 데이터에 대한 효율적인 접근을 가능하게 합니다.
    ```cpp
    #include <iostream>
    #include <vector>
    #include <mdspan> // C++23

    int main() {
        std::vector<int> data = {1, 2, 3, 4, 5, 6};
        // 2x3 행렬 뷰 생성
        std::mdspan<int, std::dextents<size_t, 2>> m(data.data(), 2, 3);

        std::cout << m[0, 0] << " " << m[0, 1] << " " << m[0, 2] << std::endl; // 출력: 1 2 3
        std::cout << m[1, 0] << " " << m[1, 1] << " " << m[1, 2] << std::endl; // 출력: 4 5 6
        return 0;
    }
    ```

*   **표준 라이브러리 모듈 (`std` 및 `std.compat`):** 표준 라이브러리를 모듈로 제공하여 컴파일 시간을 단축하고 모듈화된 프로그래밍을 지원합니다.
    ```cpp
    // main.cpp
    import std; // C++23

    int main() {
        std::cout << "Hello, C++23 Modules!" << std::endl;
        std::vector<int> v = {1, 2, 3};
        std::println("{}", v); // C++23의 std::println
        return 0;
    }
    ```

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
