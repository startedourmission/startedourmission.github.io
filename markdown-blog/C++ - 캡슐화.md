---
date: 2025-06-30
tags:
  - C++
aliases:
---

# 캡슐화

C++에서 캡슐화(Encapsulation)는 객체 지향 프로그래밍(OOP)의 핵심 원칙 중 하나로, 데이터(속성)와 해당 데이터를 조작하는 메서드(함수)를 하나의 단위(클래스)로 묶는 것을 의미합니다. 또한, 외부에서 직접 접근할 수 없도록 데이터를 보호하고, 메서드를 통해서만 접근하도록 제한하는 정보 은닉(Information Hiding)의 개념을 포함합니다.

**캡슐화의 목적:**

1.  **데이터 보호 (정보 은닉):** 클래스 내부의 데이터를 외부에서 직접 변경하는 것을 막아 데이터의 무결성을 유지합니다.
2.  **유지보수성 향상:** 내부 구현이 변경되더라도 외부 인터페이스가 동일하게 유지되므로, 코드 변경의 파급 효과를 줄여 유지보수를 용이하게 합니다.
3.  **재사용성 증대:** 잘 캡슐화된 클래스는 독립적인 모듈로 작동하여 다른 프로젝트나 다른 부분에서 쉽게 재사용될 수 있습니다.
4.  **복잡성 감소:** 사용자는 클래스의 내부 구현을 알 필요 없이 제공되는 인터페이스(public 메서드)만 사용하여 객체를 조작할 수 있으므로, 코드의 복잡성을 줄입니다.

**C++에서 캡슐화를 구현하는 방법:**

C++에서는 주로 **접근 지정자(Access Specifiers)**를 사용하여 캡슐화를 구현합니다.

*   **`private`:**
    *   `private`으로 선언된 멤버(데이터 또는 함수)는 해당 클래스 내부에서만 접근할 수 있습니다.
    *   클래스 외부에서는 직접 접근할 수 없으며, `public` 메서드를 통해서만 간접적으로 접근하거나 수정할 수 있습니다. 이것이 정보 은닉의 핵심입니다.

*   **`protected`:**
    *   `protected`로 선언된 멤버는 해당 클래스 내부와 해당 클래스를 상속받은 파생 클래스에서만 접근할 수 있습니다.
    *   `private`보다는 넓고 `public`보다는 좁은 접근 범위를 가집니다.

*   **`public`:**
    *   `public`으로 선언된 멤버는 클래스 외부 어디에서든 접근할 수 있습니다.
    *   일반적으로 클래스의 인터페이스(외부에서 호출할 수 있는 함수)를 정의할 때 사용됩니다.

**예시:**

```cpp
#include <iostream>
#include <string>

class BankAccount {
private:
    std::string accountNumber; // 계좌 번호 (외부에서 직접 접근 불가)
    double balance;            // 잔액 (외부에서 직접 접근 불가)

public:
    // 생성자
    BankAccount(std::string accNum, double initialBalance) {
        accountNumber = accNum;
        if (initialBalance >= 0) {
            balance = initialBalance;
        } else {
            balance = 0;
            std::cout << "Initial balance cannot be negative. Setting to 0." << std::endl;
        }
    }

    // 잔액을 입금하는 public 메서드 (데이터 조작)
    void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            std::cout << "Deposited: " << amount << ". New balance: " << balance << std::endl;
        } else {
            std::cout << "Deposit amount must be positive." << std::endl;
        }
    }

    // 잔액을 출금하는 public 메서드 (데이터 조작)
    void withdraw(double amount) {
        if (amount > 0 && balance >= amount) {
            balance -= amount;
            std::cout << "Withdrew: " << amount << ". New balance: " << balance << std::endl;
        } else if (amount <= 0) {
            std::cout << "Withdraw amount must be positive." << std::endl;
        } else {
            std::cout << "Insufficient balance." << std::endl;
        }
    }

    // 잔액을 조회하는 public 메서드 (데이터 접근)
    double getBalance() const { // const는 이 함수가 멤버 변수를 변경하지 않음을 의미
        return balance;
    }

    // 계좌 번호를 조회하는 public 메서드 (데이터 접근)
    std::string getAccountNumber() const {
        return accountNumber;
    }
};

int main() {
    BankAccount myAccount("123-456-789", 1000.0);

    // private 멤버에 직접 접근 시도 (컴파일 오류 발생)
    // myAccount.balance = 5000.0; // Error: 'balance' is private

    // public 메서드를 통해 데이터에 접근 및 조작
    std::cout << "Account Number: " << myAccount.getAccountNumber() << std::endl;
    std::cout << "Current Balance: " << myAccount.getBalance() << std::endl;

    myAccount.deposit(500.0);
    myAccount.withdraw(200.0);
    myAccount.withdraw(2000.0); // 잔액 부족

    std::cout << "Final Balance: " << myAccount.getBalance() << std::endl;

    return 0;
}
```