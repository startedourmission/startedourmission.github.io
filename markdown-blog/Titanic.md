---
date: 2025-04-05
tags:
  - 머신러닝
aliases:
---

**Kaggle  :** [Titanic - Machine Learning from Disaster](https://www.kaggle.com/c/titanic)

타이타닉 생존자 예측 문제는 머신러닝을 처음 접할 때 자주 사용되는 예제입니다. 문제를 이해하기 쉽고 간단한 예측 모델로도 높은 성능을 달성할 수 있습니다.

이 문제를 해결하면서 데이터분석 수행 절차와 기초적인 머신러닝 기법을 배울 수 있습니다. 

## Dataload

주어진 파일은 다음의 구조를 가집니다.

```
kaggle/
	input/
		titanic/
			train.csv
			test.csv
			gender_submission.csv
```

다음은 데이터를 불러오는 코드입니다. csv 파일은 표 형식으로 저장되어있는 데이터입니다. 파이썬에서는 csv, 엑셀 등의 스프레드시트 데이터를 Pandas 라이브러리로 다룰 수 있습니다.

```
import pandas as pd

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

train = pd.read_csv("/kaggle/input/titanic/train.csv")
test = pd.read_csv("/kaggle/input/titanic/test.csv")
gs= pd.read_csv("/kaggle/input/titanic/gender_submission.csv")
```

gender_submission.csv는 Kaggle에 제출해야할 파일의 형식을 보여줍니다. 

|    |   PassengerId |   Survived |
|---:|--------------:|-----------:|
|  0 |           892 |          0 |
|  1 |           893 |          1 |
|  2 |           894 |          0 |
|  3 |           895 |          0 |
|  4 |           896 |          1 |
## Features

아래는 train 데이터의 상위 5개 행과 각 특성에 대한 설명입니다. Kaggle에 기재되어있는 설명을 기준으로 합니다.

**train.head()**

|     | PassengerId | Survived | Pclass | Name                                                | Sex    | Age | SibSp | Parch | Ticket           |    Fare | Cabin | Embarked |
| --: | ----------: | -------: | -----: | :-------------------------------------------------- | :----- | --: | ----: | ----: | :--------------- | ------: | :---- | :------- |
|   0 |           1 |        0 |      3 | Braund, Mr. Owen Harris                             | male   |  22 |     1 |     0 | A/5 21171        |    7.25 | nan   | S        |
|   1 |           2 |        1 |      1 | Cumings, Mrs. John Bradley (Florence Briggs Thayer) | female |  38 |     1 |     0 | PC 17599         | 71.2833 | C85   | C        |
|   2 |           3 |        1 |      3 | Heikkinen, Miss. Laina                              | female |  26 |     0 |     0 | STON/O2. 3101282 |   7.925 | nan   | S        |
|   3 |           4 |        1 |      1 | Futrelle, Mrs. Jacques Heath (Lily May Peel)        | female |  35 |     1 |     0 | 113803           |    53.1 | C123  | S        |
|   4 |           5 |        0 |      3 | Allen, Mr. William Henry                            | male   |  35 |     0 |     0 | 373450           |    8.05 | nan   | S        |

0. 

1. PassengerId

승객의 고유 번호입니다. 1부터 순차적으로 매겨져 있습니다.

2. **Survived (목표변수)**
	타이타닉 문제에서 최종적으로 예측해야 할 변수입니다. 0은 사망, 1은 생존입니다.

3. Pclass
	선박 좌석의 등급입니다. 1등급부터 3등급까지 나뉘어져있으며, 가장 좋은 좌석은 1등급입니다.

4. Name
	승객의 이름입니다. Mr, Mrs, Miss 등의 호칭을 포함합니다.

5. Sex
	승객의 성별입니다. male, female로 나뉘어져 있습니다.

6. Age
	승객의 나이입니다. 

7. SibSp
	Sibling은 형제자매, Spouse는 배우자라는 뜻입니다. 동승한 형제자매의 수입니다. 의붓형제와 의붓자매를 포함합니다. 약혼자는 포함되지 않습니다. 

8. Parch
	Parent는 부모, Child는 자녀라는 뜻입니다. 함께 탑승한 부모, 자녀 수입니다. 양자를 포함합니다. 
	일부 아이들은 Parch가 0인데, 유모와 여행을 왔기 때문입니다.

9. Ticket
	선박 탑승 티켓의 번호입니다. 문자와 숫자가 섞여있는데, 같은 티켓번호라면 함께 여행하는 그룹입니다.

10. Fare
	티켓의 요금입니다.

11. Cabin
	객실 번호입니다. 알파벳과 숫자로 조합되어있습니다.

12. Embarked
	어떤 항구에서 탑승했는지 나타냅니다. 
	- C = Cherbourg (프랑스)
	- Q = Queenstown (아일랜드)
	- S = Southampton (영국)

