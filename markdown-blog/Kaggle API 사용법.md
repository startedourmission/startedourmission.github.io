---
date: 2025-04-05
tags:
  - 머신러닝
aliases:
description: Kaggle API의 설치 및 사용법을 정리한 가이드입니다. API 토큰 설정 방법부터 CLI 또는 Python 코드를 사용하여 데이터셋과 대회 데이터를 다운로드하는 등 주요 기능을 예제와 함께 설명하여 Kaggle 환경 외부에서의 활용을 돕습니다.
image: "![[]]"
---

Kaggle은 문제 풀이와 대회 코드 제출을 위한 자체 노트북 환경을 제공한다. 하지만 로컬 환경이나 Colaboratory 등 다양한 환경에서 캐글의 기능을 사용할 수 있는 API를 제공한다.

---

## 1. 설치 및 설정
### 설치
Kaggle 라이브러리는 pip를 통해 설치할 수 있다.

```bash
pip install kaggle
```

### API 토큰 설정
1. Kaggle 계정에서 API 토큰(`kaggle.json`)을 생성한다.
2. 해당 파일을 다음 경로에 저장합니다:
   - Windows: `C:\Users\<username>\.kaggle\kaggle.json`
   - Mac/Linux: `~/.kaggle/kaggle.json`

---

## 2. 주요 기능
Kaggle 라이브러리는 다양한 기능을 제공하며, 이를 CLI(Command Line Interface) 또는 Python 코드로 사용할 수 있습니다.

### 데이터셋 다운로드
Kaggle에서 제공하는 데이터셋을 다운로드할 수 있습니다.
```bash
kaggle datasets download -d <dataset-name>
```

Python 코드로 실행:
```python
import os
os.system("kaggle datasets download -d <dataset-name>")
```

### 대회 정보 조회
현재 진행 중인 대회 목록을 확인:
```bash
kaggle competitions list
```

### 대회 데이터 다운로드
특정 대회의 데이터를 다운로드:
```bash
kaggle competitions download -c <competition-name>
```

---

## 3. Kaggle 환경 디렉토리 구조
Kaggle 노트북에서는 특정 디렉토리 구조가 기본적으로 제공됩니다:

| 디렉토리             | 설명                                                                 |
|----------------------|----------------------------------------------------------------------|
| `/kaggle/input`      | 읽기 전용 데이터셋 디렉토리 (업로드된 데이터 포함).                  |
| `/kaggle/working`    | 작업 디렉토리 (최대 20GB 저장 가능).                                |
| `/kaggle/temp`       | 임시 파일 저장소 (세션 종료 시 삭제됨).                             |

### 예제 코드: 디렉토리 탐색
```python
import os

for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
```

---

## 4. Python 코드 예제
### 데이터셋 다운로드 및 로드
```python
import pandas as pd

# 데이터셋 경로 출력
!kaggle datasets download -d <dataset-name>

# CSV 파일 읽기
df = pd.read_csv('/kaggle/input/<dataset-folder>/<file-name>.csv')
print(df.head())
```

### 제출 파일 생성 및 저장
```python
# 결과를 CSV로 저장
submission = pd.DataFrame({'Id': [1, 2], 'Prediction': [0, 1]})
submission.to_csv('/kaggle/working/submission.csv', index=False)
```

---

