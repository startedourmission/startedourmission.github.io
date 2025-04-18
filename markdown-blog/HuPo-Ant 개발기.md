---
date: 2025-04-05
tags:
  - 개발
aliases:
---

[Paper](https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE12014926) | [Github](https://github.com/InhaKMS/HuPo-AnT)

"밀집된 사람들이 등장하는 이미지는 어떻게 객체탐지를 수행해야하는가?" 이 문제는 객체 탐지 분야의 넘어야 할 산 중 하나이다. 일반적으로 군중 상황은 해상도에 비해 객체의 크기가 작고 그 수가 많다. 더욱 곤란한 점은 사람이 다른 사람이나 장애물에 의해 가려져있다는 것이다. 만일 포즈 추정까지 수행해야 한다면, 문제는 더욱 곤란해진다. 원래 인공지능 프로젝트가 그렇지만, 데이터셋의 질에 더 강하게 의존하게 된다. 

Human Object Detection과 Pose Estimation에 사용되는 데이터셋은 참 만들기가 번거롭다. 사진 속 객체의 Bounding Box 좌표와 관절 좌표가 필요한데,  보통 사진에 등장하는 사람 한 명당 15~20개 정도의 좌표를 사용한다. 우리는 군중 상황에서의 탐지를 주로 연구했기때문에, 단순히 기존 데이터셋을 분석하는것만 해도 상당한 시간을 소요했다. 

MS-COCO, CrowdPose 와 같은 훌륭한 연구의 도움을 크게 받았다. 특히 CrowdPose는 Crowd Index라는 지표를 사용하여 군중의 Occlusion 정도를 수치화하였다. 수많은 이미지 중 군중 상황에 부합하는 이미지가 무엇인지 필터링할 필요가 있었는데, 그때 Crowd Index의 도움을 많이 받았다. 


[![](https://github.com/jeffffffli/CrowdPose/raw/master/crowdpose.gif)](https://github.com/jeffffffli/CrowdPose/blob/master/crowdpose.gif)

Crowd Pose는 Crowd Index를 기반으로 이미지를 세가지로 분류하였다. 수치가 높은 데이터, 낮은 데이터, 중간 데이터로 나누었으며 데이터셋의 Crowd Index 분포도 일정하게 하였다. 즉 CrwodPose 데이터셋을 사용하여 모델을 학습시키면, 다양한 Occlusion에 강건한 Pose Estimation 모델을 만들 수 있다. 

### Crowd Index

Crowd Index는 두 객체가 겹쳐있을 때, 키포인트가 얼마나 다른 객체의 바운딩박스에 포함되는지에 대한 비율을 기반으로 계산한다. 수식은 논문에 공개되어있었지만, 실제 수치가 계산되는 코드는 구할 수 없었다. 그 수치를 직접 계산하며 Crowd Index를 계산하는 코드를 다시 구현할 수 있었다.

중요한 점은, Crowd Index가 높다 해서 만드시 군중 이미지인 것은 아니라는 점이다. 객체의 겹침 정도로 계산되는 수치이기 때문에, 이미지에 얼마나 많은 사람이 등장하는지는 알 수 없다. 다중 객체 인식에서는 Occlusion도 중요하지만 객체의 숫자도 중요하다. 우리의 관심사는 군중 이미지였기때문에, 사람 수를 반영한 새로운 데이터셋을 구축하기로 했다. 

### HuPoAnt

기존에 있던 라벨을 수정하는 것은 쉽지 않은 작업이다. 차라리 새로 만드는게 편할 수도 있다. 흔히 남의 코드를 수정하는 것보다 처음부터 만드는게 편한 것과 비슷한 느낌이다. 그래서 기존의 주석을 수정하는 것에 최적화된 라벨링 도구를 제작하였다. 


![hupoant2](images/hupoant_2.png)


### 추후 연구

필요한 개선 사항이 남아있다. 많은 데이터셋은 COCO의 형식을 따르지 않는다. JSON 파일이 아닌 경우도 있다. 일례로 Crowd Human 데이터셋은 OGDT라는 독자적인 파일 포맷을 사용한다. 다양한 형식이 호환되고 형식 변환까지 지원하는 프로그램을 만들고 싶었지만 시간이 부족했다. 비디오 데이터를 처리하는 기능도 끝내 추가되지 못한 것이 아쉽다. 