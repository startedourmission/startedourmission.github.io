---
date: 2025-09-17
tags:
aliases:
image:
---
애플 실리콘 macOS에서 UTM으로 윈도우 11을 실행했습니다. 이게 뭐라고 시행 착오를 여럿 겪었다가 드디어 성공했습니다. 보통 macOS에서 다른 운영체제를 실행하기 위해 패러렐즈를 사용하지만 연에 65,000원 이상 요금제를 구독하기 싫어서 UTM을 고집했습니다. 불필요한 지출이라 생각하다보니 여태 패러렐즈를 사용해본 적은 없지만 UTM이 UI도 깔끔하고 윈도우, 리눅스 등 다양한 운영체제를 지원하기에 굳이 바꾸려는 생각은 안들었습니다. 다만 예전에 설치했던 과정이 기억나지 않아 똑같은 시행착오를 반복해서 이번에는 깔끔하게 기록해두려 합니다. 

이 글은 hyeoni님의 티스토리 게시글을 참고해 작성했습니다.
- https://dev-hyonie.tistory.com/44
## UTM 설치

 ~~UTM의 설치 과정이랄 것은 딱히 없습니다. 링크에 접속해서 다운로드 버튼만 누르면 끝이니까요. 
~ - [UTM 설치 링크](mac.getutm.app)~

UTM 4.7.1 버전부터 VHDX 파일을 사용할 수 없습니다. 마이크로소프트에서 공식 ISO 파일을 배포하기 시작했기 때문인데요. 어쩐지 ISO로는 부팅이 안됐습니다. 그래서 4.7.0 버전 UTM을 다운로드해서 원래 방식으로 사용하는 것이 좋겠습니다. 

다음 UTM 공식 깃허브의 릴리스 페이지에 접속하세요. 스크롤을 내려 4.7.0 버전을 찾아 [Assets]을 누르면 해당 버전 UTM의 dmg 설치 파일을 내려받을 수 있습니다.
- UTM 깃허브/릴리즈 : https://github.com/utmapp/UTM/releases 

![[Pasted image 20250917130820.png]]
최신 버전에서 VHDX를 사용하는 방법이나 ISO 부팅 절차를 잘 아시는 분이 계시면 알려주세요~
## Windows Insider Preview Downloads

애플 실리콘 맥은 ARM 기반 CPU입니다. ARM을 지원하는 윈도우를 다운받기 위해 인사이더 프리뷰 버전을 설치합니다. 원래는 얼리어답터나 개발자를 위한 기능이지만 무료이기도 하고 ARM 지원 윈도우를 내려받을 수 있는 다른 방법이 제한적이므로 여기서 VDHX 파일을 내려받아 사용합니다.

- [윈도우즈 인사이더 프리뷰 설치 링크]( [https://www.microsoft.com/en-us/software-download/windowsinsiderpreviewARM64](https://www.microsoft.com/en-us/software-download/windowsinsiderpreviewARM64))

링크에 접속하고 마이크로소프트 계정으로 로그인합니다. 옵션은 ARM64 Preview Dev 버전을 선택하세요. 

마이크로소프트 로그인을 안하거나 윈도우 인사이더 프로그램에 join하지 않으면 아래 화면이 표시됩니다. 인사이더 프로그램은 다음 링크에서 join할 수 있습니다.
- https://support.microsoft.com/en-us/windows/join-the-windows-insider-program-and-manage-insider-settings-ef20bb3d-40f4-20cc-ba3c-a72c844b563c

![[Pasted image 20250917130837.png]]
![[Pasted image 20250917130845.png]]

## 가상머신 만들기

UTM을 실행한 후, 새 가상머신(New Vitual Machine)을 생성합니다.

1. UTM 메인 화면에서 "+" 버튼을 클릭합니다.

2. "가상 머신 구성(Virtualize)" 옵션을 선택할 후 "다음(Next)" 버튼을 누릅니다.

3. 윈도우 10 이상 설치, VHDX 이미지 가져오기, 드라이버 및 SPICE 도구 설치를 모두 체크합니다.

4. 찾아보기를 눌러 내려받은 윈도우 VHDX 파일을 선택합니다.
![[Pasted image 20250917130859.png]]

메모리 용량은 윈도우 11이 원활하게 실행되도록 충분히 설정해야 합니다. 4GB 이상(권장 8GB)으로 설정합니다. 현재 컴퓨터의 램 용량의 절반 이하를 추천합니다. 최대 메모리를 초과하면 절대 안됩니다. 

## **윈도우 설치**

UTM에 생성된 윈도우 가상 머신을 실행합니다. 부팅 시 오류가 발생하면 VHDX 파일과 설정을 다시 확인해보세요.

윈도우 설치 화면의 첫 번째 단계에서 국가, 지역, 키보드 선택을 한국으로 합니다. 키보드 레이아웃 설정은 스킵으로 넘어갑니다.

**인터넷 설정 단계에서 Install Drive를 누르지 마세요.** 이 단계에서 인터넷을 설치할 수 없으므로 인터넷 연결 없이 진행해야 합니다.

1. \[Shift \+ F10\] 키를 눌러 명령 프롬프트를 엽니다.

2. 명령창에 다음 명령을 입력하고 엔터를 누릅니다 : oobe\\bypassnro

3. 명령이 실행되면 시스템이 재부팅되고, 동일한 네트워크 연결 화면으로 다시 돌아옵니다.

재부팅 후 다시 돌아오면 "I don't have internet" 옵션이 화면에 나타납니다. 이 옵션을 선택하여 인터넷 없이 설치를 진행할 수 있습니다.

사용자 이름과 비밀번호를 입력하여 계정을 설정합니다. 비밀번호는 공란으로 넘어갈 수 있습니다. 그 외 다른 설정은 No나 Skip을 눌러 빠르게 넘어갑니다.

![[Pasted image 20250917131115.png]]
![[Pasted image 20250917131126.png]]

## **UTM Guest Tools 설치** 

윈도우 가상머신이 잘 실행된다면 UTM Guest Tools를 설치합니다. 이 도구를 설치해야 인터넷을 포함한 디스플레이, 마우스 설정 등 편의 기능을 사용할 수 있습니다.   
윈도우 바탕화면에서 \[This PC ➝ CD Drive UTM Guest Tools\]에 들어갑니다. utm-guest-tools 파일을 찾아 실행하세요.

## **Display Output is not active 해결**

UTM Guest Tools를 설치하면 화면이 꺼지고 Display Output is not active라는 문구가 표시될 수 있습니다. UTM 설정에 들어가 \[디스플레이 \- 렌더링 백엔드\]를 ANGLE (OPENGL)로 변경하고 다시 부팅하세요.