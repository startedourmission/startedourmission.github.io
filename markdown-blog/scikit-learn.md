---
date: 2025-04-05
tags:
  - 머신러닝
aliases:
---

## 데이터셋 (datasets)
```python
# 내장 데이터셋
from sklearn.datasets import load_boston
from sklearn.datasets import load_iris
from sklearn.datasets import load_digits
from sklearn.datasets import load_breast_cancer
from sklearn.datasets import load_diabetes

# 데이터 생성
from sklearn.datasets import make_classification
from sklearn.datasets import make_regression
from sklearn.datasets import make_blobs
```

## 전처리 (preprocessing)
```python
# 스케일링
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import MaxAbsScaler
from sklearn.preprocessing import Normalizer

# 인코딩
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder

# 특성 처리
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import PowerTransformer
from sklearn.preprocessing import QuantileTransformer
from sklearn.preprocessing import KBinsDiscretizer
```

## 특성 선택 (feature_selection)
```python
# 단변량 선택
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import SelectPercentile
from sklearn.feature_selection import GenericUnivariateSelect

# 모델 기반 선택
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import RFE
from sklearn.feature_selection import RFECV
```

## 모델 선택 (model_selection)
```python
# 데이터 분할
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GroupKFold

# 하이퍼파라미터 튜닝
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import HalvingGridSearchCV
from sklearn.model_selection import HalvingRandomSearchCV
```

## 메트릭스 (metrics)
```python
# 분류 평가
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix

# 회귀 평가
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.metrics import explained_variance_score
```

## 선형 모델 (linear_model)
```python
# 회귀
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import SGDRegressor

# 분류
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import RidgeClassifier
```

## 앙상블 (ensemble)
```python
# 랜덤 포레스트
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor

# 그래디언트 부스팅
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import GradientBoostingRegressor
from xgboost import XGBClassifier
from xgboost import XGBRegressor

# 기타 앙상블
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import AdaBoostRegressor
```

## 트리 (tree)
```python
# 의사결정 트리
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import ExtraTreeClassifier
from sklearn.tree import ExtraTreeRegressor
```

## 서포트 벡터 머신 (svm)
```python
# SVM 모델
from sklearn.svm import SVC
from sklearn.svm import SVR
from sklearn.svm import LinearSVC
from sklearn.svm import LinearSVR
```

## 군집화 (cluster)
```python
# 군집 알고리즘
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import SpectralClustering
from sklearn.cluster import MiniBatchKMeans
```

## 차원 축소 (decomposition)
```python
# 차원 축소 기법
from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import FactorAnalysis
from sklearn.decomposition import FastICA
from sklearn.decomposition import NMF
```

## 파이프라인 (pipeline)
```python
# 파이프라인 도구
from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import make_pipeline
from sklearn.pipeline import make_union
```

## 결측치 처리 (impute)
```python
# 결측치 대체
from sklearn.impute import SimpleImputer
from sklearn.impute import IterativeImputer
from sklearn.impute import KNNImputer
from sklearn.impute import MissingIndicator
```

## 교차 분해 (cross_decomposition)
```python
# 교차 분해 모델
from sklearn.cross_decomposition import CCA
from sklearn.cross_decomposition import PLSRegression
from sklearn.cross_decomposition import PLSCanonical
```

## 매니폴드 학습 (manifold)
```python
# 매니폴드 알고리즘
from sklearn.manifold import TSNE
from sklearn.manifold import LocallyLinearEmbedding
from sklearn.manifold import Isomap
from sklearn.manifold import SpectralEmbedding
from sklearn.manifold import MDS
```

## 일괄 임포트
```python
# 전체 모듈 임포트
from sklearn import datasets
from sklearn import preprocessing
from sklearn import feature_selection
from sklearn import model_selection
from sklearn import metrics
from sklearn import linear_model
from sklearn import ensemble
from sklearn import tree
from sklearn import svm
from sklearn import cluster
from sklearn import decomposition
from sklearn import pipeline
from sklearn import impute
from sklearn import cross_decomposition
from sklearn import manifold
```


# 사용 예시
### 1. 데이터 전처리 (Preprocessing)
```python
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 특성 스케일링
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 정규화
normalizer = preprocessing.Normalizer()
X_normalized = normalizer.fit_transform(X)

# 레이블 인코딩
label_encoder = preprocessing.LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# 원핫 인코딩
onehot_encoder = preprocessing.OneHotEncoder()
y_onehot = onehot_encoder.fit_transform(y.reshape(-1, 1))
```

### 2. 모델 선택 및 학습
```python
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

# 선형 회귀
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

# 로지스틱 회귀
logistic_model = LogisticRegression()
logistic_model.fit(X_train, y_train)

# 결정 트리
tree_model = DecisionTreeClassifier(max_depth=5)
tree_model.fit(X_train, y_train)

# 랜덤 포레스트
rf_model = RandomForestClassifier(n_estimators=100)
rf_model.fit(X_train, y_train)

# SVM
svm_model = SVC(kernel='rbf')
svm_model.fit(X_train, y_train)
```

### 3. 모델 평가
```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_squared_error, r2_score, confusion_matrix
)

# 예측
y_pred = model.predict(X_test)

# 분류 평가 지표
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# 회귀 평가 지표
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# 혼동 행렬
conf_matrix = confusion_matrix(y_test, y_pred)
```

### 4. 교차 검증
```python
from sklearn.model_selection import (
    cross_val_score, KFold, GridSearchCV
)

# K-폴드 교차 검증
kfold = KFold(n_splits=5, shuffle=True)
scores = cross_val_score(model, X, y, cv=kfold)

# 그리드 서치
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20, 30]
}
grid_search = GridSearchCV(model, param_grid, cv=5)
grid_search.fit(X_train, y_train)
```

### 5. 특성 선택과 차원 축소
```python
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.decomposition import PCA

# 특성 선택
selector = SelectKBest(chi2, k=5)
X_selected = selector.fit_transform(X, y)

# PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)
```

### 6. 파이프라인
```python
from sklearn.pipeline import Pipeline

# 파이프라인 구축
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('pca', PCA(n_components=2)),
    ('classifier', RandomForestClassifier())
])

# 파이프라인 실행
pipeline.fit(X_train, y_train)
```

### 7. 군집화
```python
from sklearn.cluster import KMeans, DBSCAN

# K-평균 군집화
kmeans = KMeans(n_clusters=3)
clusters = kmeans.fit_predict(X)

# DBSCAN
dbscan = DBSCAN(eps=0.5, min_samples=5)
clusters = dbscan.fit_predict(X)
```

### 8. 텍스트 처리
```python
from sklearn.feature_extraction.text import (
    CountVectorizer, TfidfVectorizer
)

# 카운트 벡터화
count_vec = CountVectorizer()
X_count = count_vec.fit_transform(texts)

# TF-IDF 벡터화
tfidf_vec = TfidfVectorizer()
X_tfidf = tfidf_vec.fit_transform(texts)
```

### 9. 모델 저장 및 로드
```python
from sklearn.externals import joblib

# 모델 저장
joblib.dump(model, 'model.pkl')

# 모델 로드
loaded_model = joblib.load('model.pkl')
```

### 10. 앙상블 방법
```python
from sklearn.ensemble import (
    VotingClassifier, BaggingClassifier, AdaBoostClassifier
)

# 보팅
voting_clf = VotingClassifier(
    estimators=[
        ('rf', RandomForestClassifier()),
        ('svm', SVC())
    ]
)

# 배깅
bagging = BaggingClassifier(
    base_estimator=DecisionTreeClassifier(),
    n_estimators=10
)

# 부스팅
boosting = AdaBoostClassifier(
    base_estimator=DecisionTreeClassifier(),
    n_estimators=50
)
```

