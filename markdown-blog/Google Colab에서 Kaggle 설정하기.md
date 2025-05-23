---
date: 2025-04-05
tags:
  - 머신러닝
aliases:
---
## Google Colab 설정하기

Colab은 구글의 GPU/TPU 자원을 사용할 수 있는 클라우드 서비스와 Jupyter Notebook 형식의 대화형 인터페이스를 제공하는 개발 환경이다. 

### Colab의 장점
* GPU/TPU 무료 사용 가능
* 설치 없이 브라우저에서 바로 사용
* 구글 드라이브와 연동
* 코드와 마크다운을 혼합한 노트북 형식

### Colab 시작하기
1. Google 계정으로 로그인
2. [Google Colab](https://colab.research.google.com/) 접속
3. 새 노트 만들기 또는 기존 노트북 열기

## Kaggle 설정하기

Kaggle은 데이터 사이언스 경진대회 플랫폼이자 풍부한 데이터셋과 코드를 공유하는 커뮤니티이다.

### Kaggle 시작하기
4. [Kaggle](https://www.kaggle.com/) 계정 생성
5. 프로필 설정
6. API 토큰 발급받기
   * My Account → Create New API Token
   * kaggle.json 파일 다운로드

### Kaggle API

>  Colab에서 리눅스 쉘 명령어를 사용하기 위해서는 ! 를 사용한다.

```python
# Google Colab에서 Kaggle API 설정하기
!pip install kaggle
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

# 데이터셋 다운로드 예시
!kaggle datasets download -d dataset_name
```

### Kaggle 기능
* Competitions: 다양한 데이터 사이언스 경진대회 참여
* Datasets: 풍부한 데이터셋 검색 및 다운로드
* Notebooks: 다른 사용자의 코드 학습
* Discussions: 커뮤니티 참여


## Git/Github 설정하기

Git은 버전 관리 시스템이며, Github는 Git을 사용하는 프로젝트 호스팅 플랫폼이다.

### Git 설치 및 설정
7. [Git 공식 사이트](https://git-scm.com/)에서 설치 파일 다운로드
8. 기본 설정으로 설치 진행
9. 터미널/Git Bash에서 기본 설정
```bash
git config --global user.name "사용자이름"
git config --global user.email "이메일주소"
```

### Github 시작하기
10. [Github](https://github.com/) 계정 생성
11. 새로운 저장소(Repository) 만들기
12. 기본적인 Git 명령어
```bash
git init  # Git 저장소 초기화
git add .  # 변경사항 스테이징
git commit -m "커밋 메시지"  # 변경사항 커밋
git push origin main  # 원격 저장소에 푸시
```