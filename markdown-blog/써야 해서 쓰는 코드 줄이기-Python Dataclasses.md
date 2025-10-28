---
date: 2025-10-26
tags:
  - 정보
  - 파이썬
  - Headliner
aliases:
image: "![[1-python.png]]"
description: "클래스를 만들었으면 멤버 변수에 파라미터를 대입하고,  `__init__`, `__repr__`, `__eq__` 같은 특수 메서드를 정의합니다. 마치 Hello World를 프린트하기 위해 #include.. 로 시작하는 형식적인 코드를 줄줄 쓰듯이 말이죠. 이렇게 반복적이고 형식적인 클래스 정의 시 타입 힌트만 작성하면 반복적인 보일러플레이트 코드를 획기적으로 줄일 수 있습니다."
---
![[1-python.png|355x239]]
Dataclasses는 주로 데이터를 저장하는 용도의 클래스를 쉽게 만들 수 있게 해주는 Python 표준 라이브러리입니다. PEP 557에서 제안되어 Python 3.7부터 공식적으로 포함되었습니다.

일반적으로 클래스를 만들 때 우리는 다음과 같은 코드를 반복해서 작성합니다:

```python
class InventoryItem:
    def __init__(self, name, unit_price, quantity_on_hand=0):
        self.name = name
        self.unit_price = unit_price
        self.quantity_on_hand = quantity_on_hand
    
    def __repr__(self):
        return f"InventoryItem(name={self.name!r}, unit_price={self.unit_price!r}, quantity_on_hand={self.quantity_on_hand!r})"
    
    def __eq__(self, other):
        if not isinstance(other, InventoryItem):
            return NotImplemented
        return (self.name, self.unit_price, self.quantity_on_hand) == \
               (other.name, other.unit_price, other.quantity_on_hand)
```

Dataclasses를 사용하면 이 모든 것을 다음과 같이 간결하게 작성할 수 있습니다:

```python
from dataclasses import dataclass

@dataclass
class InventoryItem:
    name: str
    unit_price: float
    quantity_on_hand: int = 0
    
    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand
```

## 주요 기능

### 1. 자동 생성되는 특수 메서드

`@dataclass` 데코레이터는 다음 메서드들을 자동으로 생성합니다:

#### `__init__()`

클래스 변수로 정의된 필드들을 받아 초기화하는 생성자를 자동으로 만듭니다.

```python
@dataclass
class Point:
    x: float
    y: float

# 자동으로 다음과 같은 __init__이 생성됨
# def __init__(self, x: float, y: float):
#     self.x = x
#     self.y = y

p = Point(10.5, 20.3)
print(p.x, p.y)  # 10.5 20.3
```

#### `__repr__()`

객체의 문자열 표현을 자동으로 생성합니다.

```python
@dataclass
class Product:
    name: str
    price: float

p = Product("Laptop", 1299.99)
print(p)  # Product(name='Laptop', price=1299.99)
```

#### `__eq__()`

필드 값을 기준으로 동등성 비교를 수행합니다.

```python
p1 = Product("Mouse", 25.99)
p2 = Product("Mouse", 25.99)
p3 = Product("Keyboard", 79.99)

print(p1 == p2)  # True
print(p1 == p3)  # False
```

### 2. 데코레이터 매개변수로 동작 제어

`@dataclass`는 여러 매개변수를 통해 동작을 세밀하게 제어할 수 있습니다.

#### frozen: 불변 인스턴스 만들기

```python
@dataclass(frozen=True)
class ImmutablePoint:
    x: float
    y: float

p = ImmutablePoint(1.0, 2.0)
# p.x = 5.0  # FrozenInstanceError 발생!
```

불변성이 필요한 경우(예: 딕셔너리 키로 사용) 유용합니다.

#### order: 비교 연산자 자동 생성

```python
@dataclass(order=True)
class Student:
    name: str
    grade: float

students = [
    Student("Bob", 85.5),
    Student("Alice", 92.0),
    Student("Charlie", 78.3)
]

# grade 순서대로 정렬 가능
sorted_students = sorted(students)
for s in sorted_students:
    print(s)
# Student(name='Charlie', grade=78.3)
# Student(name='Bob', grade=85.5)
# Student(name='Alice', grade=92.0)
```

#### slots: 메모리 최적화

```python
@dataclass(slots=True)
class CompactPoint:
    x: float
    y: float

# __slots__를 사용하여 메모리 사용량 감소
# 대량의 인스턴스를 생성할 때 유용
```

Python 3.10부터 지원되며, `__dict__` 대신 `__slots__`를 사용하여 메모리를 절약합니다.

### 3. Field 함수로 세부 설정

`field()` 함수를 사용하면 각 필드의 동작을 더 세밀하게 제어할 수 있습니다.

#### default_factory: 가변 기본값 안전하게 사용하기

```python
from dataclasses import dataclass, field

@dataclass
class TodoList:
    owner: str
    tasks: list[str] = field(default_factory=list)  # ✅ 올바른 방법
    # tasks: list[str] = []  # ❌ 이렇게 하면 ValueError 발생

todo1 = TodoList("Alice")
todo2 = TodoList("Bob")

todo1.tasks.append("Buy groceries")
print(todo1.tasks)  # ['Buy groceries']
print(todo2.tasks)  # [] - 독립적인 리스트
```

#### init, repr, compare 옵션

```python
@dataclass
class Person:
    name: str
    age: int
    # 특정 필드를 초기화 매개변수에서 제외
    id: str = field(init=False, default="")
    # repr에서 제외 (비밀번호 등)
    password: str = field(repr=False, default="")
    # 비교 시 제외
    metadata: dict = field(compare=False, default_factory=dict)
```

### 4. 후처리: `__post_init__`

초기화 후 추가 처리가 필요할 때 `__post_init__` 메서드를 사용합니다.

```python
@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)
    
    def __post_init__(self):
        # 계산된 필드 설정
        self.area = self.width * self.height

r = Rectangle(5.0, 10.0)
print(r.area)  # 50.0
```

#### InitVar: 초기화 전용 변수

```python
from dataclasses import InitVar

@dataclass
class C:
    i: int
    j: int | None = None
    database: InitVar[object | None] = None
    
    def __post_init__(self, database):
        # database는 초기화에만 사용되고 필드로 저장되지 않음
        if self.j is None and database is not None:
            self.j = database.lookup('j')
```

## 실제 사용 예제

### 예제 1: API 응답 모델링

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class User:
    id: int
    username: str
    email: str
    is_active: bool = True
    roles: list[str] = field(default_factory=list)
    metadata: Optional[dict] = None

# JSON 응답을 쉽게 객체로 변환
user_data = {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "roles": ["admin", "user"]
}

user = User(**user_data)
print(user)
# User(id=1, username='alice', email='alice@example.com', 
#      is_active=True, roles=['admin', 'user'], metadata=None)
```

### 예제 2: 설정 관리

```python
@dataclass(frozen=True)
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    database: str = "mydb"
    username: str = field(repr=False)
    password: str = field(repr=False)
    
    def get_connection_string(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

config = DatabaseConfig(username="admin", password="secret123")
print(config)  # 비밀번호는 출력되지 않음
# DatabaseConfig(host='localhost', port=5432, database='mydb')
```

### 예제 3: 값 객체(Value Object) 패턴

```python
@dataclass(frozen=True, order=True)
class Money:
    amount: float
    currency: str
    
    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)

price1 = Money(100.50, "USD")
price2 = Money(50.25, "USD")
total = price1 + price2

print(total)  # Money(amount=150.75, currency='USD')
print(price1 < price2)  # False
```

## 유틸리티 함수

### asdict()와 astuple()

Dataclass 인스턴스를 딕셔너리나 튜플로 변환합니다.

```python
from dataclasses import asdict, astuple

@dataclass
class Point:
    x: int
    y: int

p = Point(10, 20)

print(asdict(p))   # {'x': 10, 'y': 20}
print(astuple(p))  # (10, 20)
```

중첩된 dataclass도 재귀적으로 변환됩니다:

```python
@dataclass
class Line:
    start: Point
    end: Point

line = Line(Point(0, 0), Point(10, 10))
print(asdict(line))
# {'start': {'x': 0, 'y': 0}, 'end': {'x': 10, 'y': 10}}
```

### replace()

불변 인스턴스의 일부 필드만 변경한 새 인스턴스를 생성합니다.

```python
from dataclasses import replace

@dataclass(frozen=True)
class Config:
    debug: bool
    port: int
    host: str

config = Config(debug=False, port=8000, host="localhost")
dev_config = replace(config, debug=True, port=3000)

print(config)      # Config(debug=False, port=8000, host='localhost')
print(dev_config)  # Config(debug=True, port=3000, host='localhost')
```

### make_dataclass()

동적으로 dataclass를 생성합니다.

```python
from dataclasses import make_dataclass

Point = make_dataclass('Point', [('x', int), ('y', int)])
p = Point(1, 2)
print(p)  # Point(x=1, y=2)
```

## 고급 기능

### 1. 상속

Dataclass는 일반 클래스처럼 상속할 수 있습니다.

```python
@dataclass
class Base:
    x: int = 15
    y: int = 0

@dataclass
class Derived(Base):
    z: int = 10
    x: int = 25  # 부모 클래스 필드 오버라이드

d = Derived()
print(d)  # Derived(x=25, y=0, z=10)
```

필드 순서는 MRO(Method Resolution Order)를 따라 병합됩니다.

### 2. 키워드 전용 필드 (kw_only)

Python 3.10부터 지원되며, 특정 필드를 키워드 인수로만 받도록 강제할 수 있습니다.

```python
from dataclasses import KW_ONLY

@dataclass
class User:
    name: str
    age: int
    _: KW_ONLY  # 이후 필드는 키워드 전용
    email: str
    phone: str

# User("Alice", 30, "alice@example.com", "123-456")  # ❌ 에러
user = User("Alice", 30, email="alice@example.com", phone="123-456")  # ✅
```

### 3. Descriptor와 함께 사용

Property나 custom descriptor와 함께 사용할 수 있습니다.

```python
class PositiveNumber:
    def __set_name__(self, owner, name):
        self.name = "_" + name
    
    def __get__(self, obj, type):
        if obj is None:
            return self
        return getattr(obj, self.name, 0)
    
    def __set__(self, obj, value):
        if value < 0:
            raise ValueError("Must be positive")
        setattr(obj, self.name, value)

@dataclass
class Product:
    name: str
    price: PositiveNumber = PositiveNumber()

p = Product("Widget", 10)
print(p.price)  # 10
# p.price = -5  # ValueError: Must be positive
```

## 다른 방식과의 비교

### Dataclasses vs NamedTuple

|특징|Dataclasses|NamedTuple|
|---|---|---|
|가변성|기본적으로 가변 (frozen 옵션으로 불변 가능)|항상 불변|
|상속|완전한 클래스 상속 지원|제한적|
|메서드 추가|자유롭게 추가 가능|가능하지만 제한적|
|기본값|복잡한 기본값 지원 (default_factory)|간단한 기본값만|
|타입 힌트|필수 (PEP 526)|선택적|
|메모리|약간 더 사용 (slots로 최적화 가능)|튜플처럼 경량|

**NamedTuple 예시:**

```python
from typing import NamedTuple

class PointNT(NamedTuple):
    x: int
    y: int

p = PointNT(1, 2)
# p.x = 5  # AttributeError (불변)
```

### Dataclasses vs attrs

attrs는 서드파티 라이브러리로, dataclasses보다 먼저 나왔으며 더 많은 기능을 제공합니다.

|특징|Dataclasses|attrs|
|---|---|---|
|Python 버전|3.7+ 표준 라이브러리|2.7+ 외부 라이브러리|
|검증(Validation)|직접 구현 필요|내장 validators|
|Converters|없음|있음|
|하위 호환성|3.7+|더 넓은 범위|
|생태계|표준 라이브러리|더 풍부한 플러그인|

**attrs 예시:**

```python
import attr

@attr.s
class Point:
    x = attr.ib(validator=attr.validators.instance_of(int))
    y = attr.ib(converter=int)
```

### Dataclasses vs 일반 클래스

**일반 클래스를 사용해야 할 때:**

- 복잡한 초기화 로직이 필요할 때
- 동적으로 속성이 추가/제거될 때
- 필드가 타입 힌트로 표현하기 어려울 때

**Dataclasses를 사용해야 할 때:**

- 주로 데이터를 저장하는 클래스일 때
- 보일러플레이트 코드를 줄이고 싶을 때
- 타입 힌트를 활용한 명확한 인터페이스가 필요할 때

## 언제 사용해야 하는가?

### 적합한 사용 사례

1. **데이터 전송 객체 (DTO)**: API 응답, 요청 모델
2. **설정 객체**: 애플리케이션 설정 관리
3. **값 객체**: 불변 값을 표현 (Money, Coordinate 등)
4. **간단한 모델**: ORM 없이 간단한 데이터 모델
5. **테스트 픽스처**: 테스트용 데이터 객체

### 피해야 할 상황

1. **복잡한 비즈니스 로직**: 많은 메서드가 필요한 경우
2. **동적 속성**: 런타임에 속성이 자주 변경되는 경우
3. **레거시 호환성**: Python 3.6 이하 지원이 필요한 경우
4. **고급 검증**: 복잡한 필드 검증이 필요하면 Pydantic 고려

## 실무 팁과 베스트 프랙티스

### 1. 타입 힌트 적극 활용

```python
from typing import Optional, List
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    tags: List[str] = field(default_factory=list)  # list[str] (3.9+)
    bio: Optional[str] = None  # str | None (3.10+)
```

### 2. 불변성이 필요하면 frozen 사용

```python
@dataclass(frozen=True)
class Coordinate:
    latitude: float
    longitude: float

# 해시 가능하므로 딕셔너리 키나 세트에 사용 가능
locations = {
    Coordinate(37.7749, -122.4194): "San Francisco",
    Coordinate(40.7128, -74.0060): "New York"
}
```

### 3. 가변 기본값은 항상 default_factory 사용

```python
# ❌ 잘못된 방법
@dataclass
class Wrong:
    items: list = []  # ValueError 발생!

# ✅ 올바른 방법
@dataclass
class Correct:
    items: list = field(default_factory=list)
```

### 4. 계산된 필드는 property나 **post_init** 사용

```python
@dataclass
class Circle:
    radius: float
    
    @property
    def area(self) -> float:
        return 3.14159 * self.radius ** 2
    
    @property
    def circumference(self) -> float:
        return 2 * 3.14159 * self.radius
```

### 5. 직렬화가 필요하면 asdict() 활용

```python
import json
from dataclasses import dataclass, asdict

@dataclass
class Config:
    host: str
    port: int
    debug: bool

config = Config("localhost", 8000, True)
json_str = json.dumps(asdict(config))
print(json_str)  # {"host": "localhost", "port": 8000, "debug": true}
```

## 성능 고려사항

### 메모리 사용

일반 클래스는 인스턴스마다 `__dict__`를 사용하여 속성을 저장합니다. 대량의 인스턴스를 생성할 때는 `slots=True`를 사용하세요.

```python
import sys

@dataclass
class RegularPoint:
    x: float
    y: float

@dataclass(slots=True)
class SlottedPoint:
    x: float
    y: float

regular = RegularPoint(1.0, 2.0)
slotted = SlottedPoint(1.0, 2.0)

# SlottedPoint가 메모리를 덜 사용함
# Python 3.10+에서만 사용 가능
```

### 생성 속도

Dataclass의 `__init__`은 일반 클래스와 거의 동일한 속도로 동작합니다. 성능 차이는 미미합니다.

## 마이그레이션 가이드

기존 코드를 dataclass로 변환하는 방법:

**Before (일반 클래스):**

```python
class Employee:
    def __init__(self, name, employee_id, department, salary):
        self.name = name
        self.employee_id = employee_id
        self.department = department
        self.salary = salary
    
    def __repr__(self):
        return f"Employee({self.name}, {self.employee_id}, {self.department}, {self.salary})"
    
    def __eq__(self, other):
        if not isinstance(other, Employee):
            return NotImplemented
        return (self.name, self.employee_id, self.department, self.salary) == \
               (other.name, other.employee_id, other.department, other.salary)
```

**After (Dataclass):**

```python
from dataclasses import dataclass

@dataclass
class Employee:
    name: str
    employee_id: int
    department: str
    salary: float
```

20줄이 5줄로 줄어들었습니다!

## 결론

Python dataclasses는 데이터 중심 클래스를 작성할 때 보일러플레이트 코드를 극적으로 줄여주는 강력한 도구입니다. 타입 힌트와 함께 사용하면 코드의 가독성과 유지보수성이 크게 향상됩니다.

### 핵심 요약

- **자동 생성**: `__init__`, `__repr__`, `__eq__` 등이 자동으로 생성됨
- **유연성**: frozen, order, slots 등 다양한 옵션으로 동작 제어
- **타입 안전성**: 타입 힌트를 강제하여 명확한 인터페이스 제공
- **표준 라이브러리**: 외부 의존성 없이 Python 3.7+에서 바로 사용 가능

### 다음 단계

1. 기존 프로젝트에서 데이터 저장용 클래스를 dataclass로 리팩토링해보기
2. Pydantic과 비교하여 검증이 필요한 경우 어떤 것을 선택할지 고민하기
3. attrs 라이브러리와 비교하여 고급 기능이 필요한지 평가하기

## 참고자료

- [Python 공식 문서 - dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [PEP 557 - Data Classes](https://peps.python.org/pep-0557/)
- [PEP 526 - Syntax for Variable Annotations](https://peps.python.org/pep-0526/)
- [Real Python - Python Data Classes](https://realpython.com/python-data-classes/)
- [attrs 라이브러리](https://www.attrs.org/)
- [Pydantic 라이브러리](https://docs.pydantic.dev/)