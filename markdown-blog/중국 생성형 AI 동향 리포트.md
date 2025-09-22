---
date: 2025-09-12
tags:
  - 생산성
aliases:
image: "![[]]"
description: 2025년 기준 중국 생성형 AI 기술 동향 리포트입니다. 텐센트, 알리바바, 딥시크 등 주요 12개 기업의 주력 모델과 제품을 분석하고, 오픈소스 전략, 가성비 경쟁 등 중국 AI 시장의 특징과 경쟁력을 조망합니다.
---
중국이 무섭습니다. 2025년 현재 중국에는 5,000개가 넘는 AI 기업이 활동하고 있으며[1], 많은 회사의 AI 기술력이 전 세계에서도 뛰어난 수준입니다. 그래서 퍼플렉시티에게 정리를 쭉 해보라고 시켰습니다. 이전에는 별 관심을 가지지 않았는데 이제 가질 필요가 있을 것 같습니다. 

## 주요 12개 회사 및 제품 분석

### 1. **Tencent (텐센트)**

**주력 모델**: Hunyuan (혼위안/混元) 시리즈  
**핵심 제품**:
- Hunyuan 3D World Model 1.0 - 세계 최초 오픈소스 3D 월드 생성[2],[3]
- Hunyuan Video-Foley - AI 영상에 사실적 음향 추가[4]
- Hunyuan Custom - 영상 제작의 게임체인저[5]
- Agent Development Platform 3.0 - 지능형 에이전트 개발 플랫폼[6]
- CodeBuddy - 개발자용 AI 코딩 도구로 코딩 시간 40% 단축[6]

텐센트는 2023년부터 훈위안 시리즈를 통해 포괄적인 AI 생태계를 구축했습니다[7],[8]. 특히 게임 산업에 특화된 AI 콘텐츠 생성 기술로 업계를 선도하고 있습니다. 지난 1년간 30개 이상의 신규 모델을 공개했습니다[6]. 1년에 30개는 정말 심하네요.
### 2. **Alibaba (알리바바)**

**주력 모델**: Tongyi Qianwen (통이치엔원/通義千問)  
**핵심 제품**:
- Tongyi Qianwen 2.0 - 수천억 개 매개변수 보유[9],[10]
- DingTalk AI - 회의록 요약, 비즈니스 제안서 작성[9]
- Tmall Genie - IoT 지원 스마트홈 기기[9]
- 산업별 맞춤형 모델 - 고객 지원, 법률, 의료, 금융 전용[10]

알리바바는 현재 중국 기술기업의 80%와 대형 모델 기업의 절반이 사용하는 클라우드 인프라를 제공해[10] B2B 입지가 강력합니다. 중국의 아마존이라고 생각하면 되겠죠. 

### 3. **ByteDance (바이트댄스)**

**주력 모델**: Doubao (도바오/豆包), Seedance, Seedream  
**핵심 제품**:
- Doubao - 중국에서 가장 많이 쓰이는 생성형 AI 서비스[11]
- Seedance 1.0 - 차세대 영상 생성 AI, 전 세계 최고 성능[12]
- Seedream 4.0 - 1.8초 만에 2K 이미지 생성[13],[14],[15]
- BAGEL-7B-MoT - 멀티모달 파운데이션 모델[16]
- Trae - AI 통합 개발환경[17]

틱톡으로 유명한 바이트댄스입니다. 영상과 이미지 생성 분야에서 독보적입니다. 특히 Seedream 4.0의 초고속 생성 능력은 구글의 나노바나나를 능가한다는 평가를 받고 있습니다[14]. 어..물론 내부 벤치마크입니다.

### 4. **Baidu (바이두)**

**주력 모델**: ERNIE (어니/文心) 시리즈  
**핵심 제품**:
- ERNIE 4.5 - 멀티모달 기반 모델, GPT-4 능가 주장[18],[19]
- ERNIE X1 - 추론 중심 모델, DeepSeek R1 성능에 절반 가격[18]
- ERNIE Bot - 무료 제공되는 AI 챗봇[18]
- Qianfan Platform - 기업용 AI 클라우드 플랫폼[18]

바이두는 중국 검색 서비스 탑입니다. 구글 포지션이죠. ERNIE X1이 DeepSeek R1과 비슷한 성능을 절반 가격에 제공한다고 주장..하여 가성비 경쟁에서 우위를 점합니다[18].

### 5. **DeepSeek (딥시크)**

**주력 모델**: DeepSeek-V3, DeepSeek-R1  
**핵심 제품**:
- DeepSeek-V3 - 6,710억 개 매개변수, 멀티모달 기능[20]
- DeepSeek-R1 - 추론형 모델, OpenAI o1과 경쟁[20],[21]
- DeepSeek-Coder - 코딩 전문 모델 시리즈[22]
- HAI-LLM - 고효율 훈련 프레임워크[22]

딥시크는 약 560만 달러의 저비용으로 GPT-4 수준의 성능을 달성했습니다. 전 세계에 '딥시크 쇼크'를 일으켰죠[20],[23]. 성능도 준수한데 모든 모델과 가중치를 오픈소스로 공개해서 다른 나라 뿐만 아니라 우리나라도 많이 사용합니다. 

### 6. **SenseTime (센스타임)**

**주력 모델**: SenseNova (센스노바/日日新)  
**핵심 제품**:
- SenseNova 5.0 - GPT-4 Turbo와 전면 비교 가능[24]
- SenseChat - 대화형 AI 서비스[25]
- Wuneng (우넝) Intelligence Platform - 로봇 지능 플랫폼[26]
- SenseME Platform - 스마트 단말 플랫폼[27]

센스타임은 컴퓨터 비전을 잘합니다. 얼굴인식 기술에서 시작했고 지금은 종합적인 AI 플랫폼으로 발전했습니다. 특히 로봇과 AI의 통합 분야에서 성과를 보여주고 있습니다[26]. 

### 7. **Zhipu AI (Z.ai)**

**주력 모델**: GLM (ChatGLM), GLM-4  
**핵심 제품**:
- GLM-4.5 - 3,550억 개 파라미터 오픈소스 모델[28],[29]
- GLM-Z1-Air - 경량화된 고속 추론용 모델[30]
- AutoGLM Rumination - 무료 AI 에이전트[30],[31]
- ChatGLM - 대화형 AI 모델[28]

지푸 AI는 GLM-4가 여러 벤치마크에서 GPT-4를 능가한다고 주장합니다[30],[31]. 무료 AI 에이전트 서비스를 통해 가성비 시장에서 경쟁력을 확보하고 있습니다.

### 8. **01.AI (영일 AI)**
**주력 모델**: Yi 시리즈  
**핵심 제품**:
- Yi-Large - 글로벌 대규모 언어 모델[32],[33]
- Yi-Lightning - 전문가 혼합(MoE) LLM[33]
- Yi-VL - 멀티모달 버전[33]
- Yi-Coder - 코드 생성 전문 모델[33]

01.AI의 Yi-34B-Chat 모델은 AlpacaEval 리더보드에서 GPT-4 Turbo 다음으로 2위를 차지했습니다[34]. 경쟁력이 있고 상업용 무료 라이선스를 제공하여 접근성을 높이고 있습니다.

### 9. **iFlytek (아이플라이텍)**

**주력 모델**: Spark (스파크/讯飞星火)  
**핵심 제품**:
- Spark Desk 4.0 Turbo - GPT-4 Turbo 7개 성능에서 추월[35],[36]
- Spark X1 - 추론형 모델[37]
- Spark Super Digital Human - 디지털 휴먼 서비스[36]
- 37개 언어 지원 음성 인식 솔루션[37]

음성 처리 전문입니다. 중국 288개 도시와 202개 방언을 지원하는[36] 특화된 AI 서비스를 제공합니다. 

### 10. **MiniMax (미니맥스)**

**주력 모델**: MiniMax-M1, Video-01  
**핵심 제품**:
- MiniMax-M1 - 세계 최초 오픈소스 하이브리드 어텐션 추론 모델[38],[39]
- Video-01 - 영상 생성 모델, 손동작 표현에서 우수[40]
- Talkie - 1,500만 다운로드 달성한 AI 챗봇 앱[40]
- Hailuo AI - 멀티모달 소비자 플랫폼[41]

미니맥스는 100만 토큰의 컨텍스트 창을 지원하는[38] 하이브리드 어텐션 기술과 자연스러운 인간 동작 생성 능력으로 주목받고 있습니다.

### 11. **Moonshot AI (문샷 AI)**
**주력 모델**: Kimi  
**핵심 제품**:
- Kimi K2 - 1조 파라미터 MoE 구조[42],[43]
- Kimi 2.0 - 에이전트형 자동화 특화[43]
- Kimi Chat - 128K 토큰 처리 가능[42]
- 긴 문맥 처리 전문 모델들[43]

Kimi는 유명하죠. Kimi K2가 다양한 벤치마크에서 서구 경쟁 모델과 DeepSeek를 능가하는 성능을 보여주어[44],[45] 충격이 컸습니다.

### 12. **Colossal-AI (콜로설 AI)**

**주력 모델**: 훈련 인프라 전문  
**핵심 제품**:
- ColossalAI - 대규모 모델 훈련 프레임워크[46],[47]
- Gemini 메커니즘 - 이종 메모리 관리 기술[47]
- Xverse 모델 지원 - 다양한 모델 훈련 지원[46]

콜로설 AI는 18B 파라미터 모델을 단일 GPU로 훈련 가능하게 하는[47] 신기한 훈련 기술을 가지고 있습니다. 

## 결론

인구가 많아서 그런지 정부에서 지원을 잘해주는 건지 대단하긴 하여간 대단합니다. 인프라와 학습 데이터 구하는 거는 물리적으로 따라갈 수가 없을테니, 그건 정말 부럽습니다. 보통 중국 AI의 경쟁력은 이런 것 같습니다:

**1. 오픈소스 전략**: DeepSeek, Zhipu AI, MiniMax 등 많은 기업이 오픈소스 모델을 공개

**2. 가성비 경쟁**: 딥시크의 저비용 고성능 모델을 시작으로 가격 경쟁력을 앞세운 서비스 급증

**3. 특화 분야 집중**: 음성 처리(iFlytek), 컴퓨터 비전(SenseTime), 영상 생성(ByteDance) 등 고유의 전문성을 바탕으로 차별화를 시도

**4. 급속한 성장**: 지난 5년간 AI 기업 수가 1,400개에서 5,000개로 증가하는[1] 등 폭발적인 성장세를 보임

읽어주셔서 감사합니다. 
## 출처

[1] 中 인공지능 기업 5천개 돌파…1년새 500개 신규 설립 https://v.daum.net/v/20250909154549487
[2] 텐센트 '훈위안(Hunyuan) 3D 월드 모델' 상세 분석 및 경쟁 ... https://aiproductmanager.tistory.com/1426
[3] 댓글 : 3D 모델 작업 시간 몇 초로 단축하는 AI…텐센트, 훈위안 ... https://contents.premium.naver.com/aipostkorea/aipost/comment/250123052851495kb
[4] 텐센트, AI 영상에 사실적 음향 입히는 '훈위안 비디오-폴리' 공개 http://dpg.danawa.com/news/view?boardSeq=60&listSeq=5879385
[5] 🎬 중국 텐센트 'Hunyuan-Custom', 생성형 AI 영상의 새로운 ... https://kr.linkedin.com/pulse/%EC%A4%91%EA%B5%AD-%ED%85%90%EC%84%BC%ED%8A%B8-%EC%B4%88%EA%B1%B0%EB%8C%80-%EB%A9%80%ED%8B%B0%EB%AA%A8%EB%8B%AC-ai-hunyuan-custom-%EA%B3%B5%EA%B0%9C-%EC%98%81%EC%83%81-%EC%A0%9C%EC%9E%91%EC%9D%98-%EA%B2%8C%EC%9E%84%EC%B2%B4%EC%9D%B8%EC%A0%80-keonwoo-park-0nlvc
[6] 텐센트, 산업 효율성 가속화 위한 시나리오 기반 AI 기능 ... https://www.etnews.com/20250917000190
[7] 텐센트, 자체 개발 초거대 AI '훈위안' 공개 / 클럽하우스, 재기 ... https://www.openads.co.kr/content/contentDetail?contsId=11630
[8] 中 텐센트, 초거대AI 모델 '훈위안' 공개...생성형AI 경쟁전 ... https://wowtale.net/2023/09/08/63125/
[9] 알리바바클라우드, 대규모 AI 모델 '통이치엔원' 발표 https://byline.network/2023/04/0411_02/
[10] 알리바바 클라우드, 통이치엔원2.0 및 산업별 모델 출시... ... https://platum.kr/archives/216188
[11] 바이트댄스 https://namu.wiki/w/%EB%B0%94%EC%9D%B4%ED%8A%B8%EB%8C%84%EC%8A%A4
[12] 바이트댄스(ByteDance)차세대 영상 생성 AI 모델인 Seedance ... https://aimkt.biz/%EB%B0%94%EC%9D%B4%ED%8A%B8%EB%8C%84%EC%8A%A4bytedance%EC%B0%A8%EC%84%B8%EB%8C%80-%EC%98%81%EC%83%81-%EC%83%9D%EC%84%B1-ai-%EB%AA%A8%EB%8D%B8%EC%9D%B8-seedance-1-0%EC%B6%9C%EC%8B%9C-%EA%B5%AC/
[13] 바이트댄스 Seedream 4.0 프리뷰: 구글 나노바나나를 넘어설 수 ... https://digitalbourgeois.tistory.com/1927
[14] [AI 툴 활용팁] 나노바나나보다 낫다고? 바이트댄스 AI '시드림 ... https://aimatters.co.kr/ai-tool/ai-tool-how-to/31088/
[15] Seedream 4.0 출시 완전 리뷰 - fal.ai로 체험하는 바이트댄스 ... https://notavoid.tistory.com/553
[16] BAGEL-7B-MoT: 바이트댄스의 멀티모달 AI 혁신 돌파구 https://apidog.com/kr/blog/bagel-7b-mot-kr/
[17] 바이트댄스의 AI IDE '트레이(Trae)' 직접 써봤습니다 - 요즘IT https://yozm.wishket.com/magazine/detail/2993/
[18] Baidu, ERNIE 4.5 및 ERNIE X1로 GenAI 가속화, 두 가지 ... https://www.actuia.com/kr/news/baidu-ernie-45-ernie-x1-genai/
[19] 바이두의 ERNIE 4.5와 X1: 반값의 DeepSeek R1? https://apidog.com/kr/blog/baidu-ernie-4-5-x1-2-kr/
[20] 딥시크 (Deepseek) 요약, 이거 하나만 읽으세요! https://inblog.ai/letsur/%EB%94%A5%EC%8B%9C%ED%81%AC-deepseek-%EC%9A%94%EC%95%BD-%EC%9D%B4%EA%B1%B0-%ED%95%98%EB%82%98%EB%A7%8C-%EC%9D%BD%EC%9C%BC%EC%84%B8%EC%9A%94-41422
[21] DeepSeek https://namu.wiki/w/DeepSeek
[22] 딥시크(DeepSeek) 특허 분석으로 살펴보는 AI 챗봇 시대의 ... https://www.wertcorp.com/kr/resources/view?pkResources=213
[23] 인공지능: 세계를 놀라게 한 중국 AI 챗봇 '딥시크'... 그 파장은? https://www.bbc.com/korean/articles/clykdp2dyvvo
[24] SenseTime, “SenseNova 5.0” AI 거대 모델 전면 업그레이드! https://www.sensetime.com/kr/news-detail/51168190?categoryId=51172
[25] [중국 비즈니스 트렌드&동향] 중국 인공지능 기업 '센스타임 ... https://platum.kr/archives/205584
[26] '로봇이 프레젠테이션하고 농담까지'…센스타임, '우넝' AI ... https://www.g-enews.com/article/Global-Biz/2025/07/202507280639465363fbbec65dfb_1
[27] AI 인공지능 제품 및 서비스 - 센스타임 https://www.sensetime.com/kr/product-index
[28] 중국의 AI 스타트업 지푸(Zhipu), 오픈소스 모델 GLM-4.5 공개 https://neuron.expert/news/chinas-ai-startup-zhipu-releases-open-source-model-glm-45/13980/ko/
[29] [AI넷] ｢중국 AI 스타트업 Z.ai, 오픈소스 모델 `GLM-4.5` 공개｣ ... https://www.ainet.link/22055
[30] 중국판 GPT-4? '지푸 AI'의 초고속 AI 에이전트, 왜 주목받는가 https://digitalbourgeois.tistory.com/996
[31] 中 가성비 AI 시장 경쟁 심화…지푸 AI, 무료 AI 에이전트 출시 https://zdnet.co.kr/view/?no=20250401153744
[32] Yi-Large - Intelligence, Performance & Price Analysis https://artificialanalysis.ai/models/yi-large
[33] Yi Foundation Models - 零一万物-AI2.0大模型技术和应用的 ... http://www.01.ai/yi-models
[34] 01-ai/Yi: A series of large language models trained from ... https://github.com/01-ai/Yi
[35] 中 아이플라이텍, AI 모델 '스파크데스크 2.0' 공개…내년 ... https://korean.cri.cn/2023/08/17/ARTIXXB6XSGY49xnoqJOhsZD230817.shtml
[36] 中 아이플라이텍 "AI 초거대 모델, 'GPT-4 터보' 추월" https://zdnet.co.kr/view/?no=20241025022348
[37] 讯飞星火:텍스트 생성, 음성 합성 및 다양한 언어에 걸친 ... - MOGE https://moge.ai/ko/product/iflytek-spark
[38] MiniMax-M1: 궁극의 오픈 웨이트 하이브리드 어텐션 혁명 ... https://apidog.com/kr/blog/minimax-m1-kr/
[39] 세계 최초의 하이브리드 어텐션 오픈 모델, MiniMax-M1이 ... https://digitalbourgeois.tistory.com/1464
[40] 미니맥스(MiniMax), 동영상 생성형 AI 출시 - AI 매터스 https://aimatters.co.kr/news-report/ai-news/3340/
[41] 미니맥스(회사) - 위키피디아 https://translate.google.com/translate?u=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FMiniMax_%28company%29&hl=ko&sl=en&tl=ko&client=srp
[42] Kimi-K2: 에이전트형 인공지능을 위한 최신 MoE LLM (feat. ... https://discuss.pytorch.kr/t/kimi-k2-moe-llm-feat-moonshot-ai/7247
[43] Kimi-K2란? Moonshot AI가 만든 초대형 오픈소스 언어 모델 정리 https://marcus-story.tistory.com/221
[44] 또 한번의 '딥시크 모먼트'…中 문샷 AI, 키미 K2 출시 https://m.dongascience.com/news.php?idx=72910
[45] 중국발 AI 충격, 이번엔 '키미 K2' https://www.chosun.com/economy/science/2025/07/19/NK6RST7NVZFTHGV375NCMLT5C4/
[46] Colossal-AI: 대규모 모델 훈련을 위한 오픈 소스 솔루션 - aibars https://www.aibars.net/ko/library/open-source-ai/details/719948038415716352
[47] 18B 파라미터 GPT 모델을 Single GPU로 학습하기 (Colossal-AI) https://hellcat.tistory.com/10
[48] 2025 중국 AI 테크 기업 TOP 50 발표&rdquo - 해외경제정보드림 http://dream.kotra.or.kr/kotranews/cms/news/actionKotraBoardDetail.do?SITE_NO=3&MENU_ID=70&CONTENTS_NO=1&bbsGbn=00&bbsSn=506&pNttSn=229325
[49] 게임 산업에 칼 빼든 텐센트, AI로 전공정 대체 선언 https://www.thegmnews.com/news/article.html?no=2079
[50] 상위 AI 모델 25% 중국서 개발… 美-中 양강 구도 고착 https://biz.chosun.com/it-science/ict/2025/07/14/4JYREMHKHRBBRFG37US6L7EKPE/
[51] 빅테크 뺨치네… 가성비 좋은 중국산 AI 쏟아진다 https://www.chosun.com/economy/tech_it/2025/07/30/Y4QNWJ36JBC4FAYOWNI6SWW6ZA/
[52] 포브스 선정 2025년 AI 기업 Top 50… 올해 새롭게 ... - AI 매터스 https://aimatters.co.kr/news-report/ai-report/19627/
[53] [빅테크칼럼] 中 텐센트, 오픈AI에 필적하는 '소형 AI 모델 ... https://www.newsspace.kr/news/article.html?no=8431
[54] 텐센트, 훈위안3D 월드 모델 1.0 출시 - 최초의 오픈 소스 ... https://www.reddit.com/r/LocalLLaMA/comments/1mab2i2/tencent_releases_hunyuan3d_world_model_10_first/
[55] [북경사무소] 중국의 생성형 AI 주요 기업 현황 및 전망 https://www.emerics.org:446/issueInfoView.es?article_id=56362&mid=a20100000000&search_option=&search_year=&search_month=&currentPage=1&pageCnt=10&board_id=18
[56] 포브스 차이나, 2025 AI 선도 50대 기업 발표… 신흥 기업 약진 ... https://theplaza.global/m/view.php?idx=11023
[57] 텐센트 클라우드 인텔리전트 디지털 휴먼 https://www.tencentcloud.com/ko/products/ivh
[58] [보고서]중국의 AI혁신을 주도하는AI스타트업 분석 https://www.marketcast.co.kr/entry/%EB%B3%B4%EA%B3%A0%EC%84%9C%EC%A4%91%EA%B5%AD%EC%9D%98-AI%ED%98%81%EC%8B%A0%EC%9D%84-%EC%A3%BC%EB%8F%84%ED%95%98%EB%8A%94AI%EC%8A%A4%ED%83%80%ED%8A%B8%EC%97%85-%EB%B6%84%EC%84%9D-%EC%A4%91%EA%B5%AD-%EB%8C%80%ED%91%9C-6%EA%B0%9C-AI%EC%8A%A4%ED%83%80%ED%8A%B8%EC%97%85-%EA%B8%B0%EC%97%85-%EB%B6%84%EC%84%9D
[59] SPOT 뷰 [PLUS 차이나AI테크TOP10 ETF] 중국을 리드하는 ... https://www.plusetf.co.kr/insight/report/detail?n=684
[60] BaiDu ERNIE 4.5 MoE 모델 API가 이제 라이브로 제공 ... https://blogs.novita.ai/ko/ernie-4.5-on-novita-ai/
[61] 어니 봇 - 위키피디아 https://translate.google.com/translate?u=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FErnie_Bot&hl=ko&sl=en&tl=ko&client=srp
[62] Baidu AI Cloud, 모든 규모의 비즈니스를 위한 5가지 새로운 ... https://coolenjoy.net/bbs/38/5469982?sfl=wr_subject%7C%7Cwr_content&sop=and&page=2906
[63] “바이트댄스, AI 인재·GPU 대거 투자… 中 생성형 AI 경쟁 선두 ... https://it.chosun.com/news/articleView.html?idxno=2023092129444
[64] 중국, 바이두 신형 AI 모델 '어니 4.5' 공개…GPT-4.5 능가 주장 https://www.dongbooka.com/index.php?m=content&c=index&a=show&catid=69&id=15469
[65] 차이나 생성 AI의 강자, 변화는 이제 시작일 뿐이다 https://www.samsungpop.com/common.do?cmd=down&saveKey=research.pdf&fileName=3010%2F2023022016015783K_02_04.pdf&contentType=application%2Fpdf
[66] 바이두, 새 AI 모델 'ERNIE' 공개…DeepSeek 정조준 https://www.ainet.link/20199
[67] DeepSeek 딥시크, 우리도 깊게 살펴볼까요? https://selectstar.ai/blog/insight/deep-dive-deepseek-ko/
[68] 딥시크(DeepSeek)를 안전하게 활용하는 방법 - 요즘IT https://yozm.wishket.com/magazine/detail/2997/
[69] 딥시크(DeepSeek)가 주목받는 3가지 이유 :: 모델 연산 ... https://www.skelterlabs.com/blog/deepseek
[70] 딥시크 FAQ 30가지 리스트! (초등학생도 이해가능) https://news.aikoreacommunity.com/deepseek-faq-for-beginners-30-questions/
[71] 딥시크(DeepSeek)가 주목 받는 이유 3가지: 작동 원리부터 시장 ... https://community.heartcount.io/ko/deepseek-r1-review/
[72] 딥시크 DeepSeek 가 가져온 AI 프로덕트 시장의 변화 https://www.samsungsds.com/kr/insights/deepseek-to-change-the-ai-product-market.html
[73] 센스타임 SenseTime - 공식 사이트 https://www.sensetime.com/kr
[74] 딥시크 - 위키피디아 https://translate.google.com/translate?u=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FDeepSeek&hl=ko&sl=en&tl=ko&client=srp
[75] [보안 101] 딥시크(DeepSeek)란 무엇인가요? https://www.igloo.co.kr/security-information/%EB%B3%B4%EC%95%88-101-%EB%94%A5%EC%8B%9C%ED%81%ACdeepseek%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80%EC%9A%94/
[76] AI 자율주행 - 스마트 오토 - 센스타임 https://www.sensetime.com/kr/product-detail?categoryId=51132858
[77] 딥시크에 대해 “Deep Seek” 해보기 https://www.igloo.co.kr/security-information/%EB%94%A5%EC%8B%9C%ED%81%AC%EC%97%90-%EB%8C%80%ED%95%B4-deep-seek-%ED%95%B4%EB%B3%B4%EA%B8%B0/
[78] 센스타임 - 위키피디아 https://translate.google.com/translate?u=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FSenseTime&hl=ko&sl=en&tl=ko&client=srp
[79] 인공 지능 기능으로 기업 가치 높이는 대만의 Mediatek https://www.seminet.co.kr/channel_micro.html?menu=content_sub&com_no=817&category=event&no=3678
[80] Z.ai - 위키백과 https://translate.google.com/translate?u=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FZ.ai&hl=ko&sl=en&tl=ko&client=srp
[81] 중국은 어떻게 메타를 장악했나 https://maily.so/dividedbyzero/posts/10z36xg6zlw
[82] “中스타트업 개발한 AI 모델, 오픈AI보다 처리비용 46% 저렴” https://www.chosun.com/economy/tech_it/2024/10/20/YXNSSZ6VCFBELIDWMNAVPGMLCI/
[83] "100배 빠르다" 中 세계 최초 인간 뇌 닮은 AI모델 개발 https://www.ajunews.com/view/20250910142914850
[84] yi-large Model by 01-ai https://build.nvidia.com/01-ai/yi-large
[85] 中 '딥시크', 차세대 AI 칩 '공개 임박' 시사… 美 제재 속 '자체 ... https://www.g-enews.com/article/Global-Biz/2025/08/2025082312142858760c8c1c064d_1
[86] 01-ai https://huggingface.co/01-ai
[87] 개인용 AI 슈퍼컴퓨터를 찾는다면, 정답은 엔비디아 http://www.ainet.link/18351
[88] 零一万物-AI2.0大模型技术和应用的全球公司（01.AI） http://www.01.ai
[89] 딥시크, 차세대 중국산 칩 준비하며 AI 모델 V3.1 공개※ 해당 ... https://talk.heykorean.com/community/community/view/1640437
[90] Yi-01.AI (@01AI_Yi) / X https://x.com/01ai_yi
[91] 일론 머스크 xAI, AI 학습 시스템 '콜로서스' 공개…엔비디아와 ... https://m.news.zum.com/articles/93042377/%EC%9D%BC%EB%A1%A0-%EB%A8%B8%EC%8A%A4%ED%81%AC-xai-ai-%ED%95%99%EC%8A%B5-%EC%8B%9C%EC%8A%A4%ED%85%9C-%EC%BD%9C%EB%A1%9C%EC%84%9C%EC%8A%A4-%EA%B3%B5%EA%B0%9C-%EC%97%94%EB%B9%84%EB%94%94%EC%95%84%EC%99%80-%EA%B3%B5%EB%8F%99-%EA%B0%9C%EB%B0%9C
[92] 무료 강추! 요금 폭탄 방지! AI 에이전트 혁신기술 https://www.youtube.com/watch?v=kYiq-hj3pY0
[93] [아이플라이텍] Flytek Spark Desk AI - 기획은 검정색이다. https://thinkhubhee.tistory.com/94
[94] AI xAI, AI 학습 시스템 콜로서스 공개…엔비디아 공동 개발 https://meeco.kr/AI/39188268
[95] 최신 AI 기반 비디오 생성 및 사진 개선 플랫폼 - Minimax AI https://minimaxai.me/ko
[96] 아니 중국 AI기술 무엇..? 손 안대도 필기해주는 AI 노트 사봄 https://www.youtube.com/watch?v=PoegLq8nYm0
[97] 세계 최대 AI 슈퍼클러스터 xAI 콜로서스 내부 완전 분석 https://slashpage.com/senxation/qrx6zk25zxjgxmv314y5
[98] 벤처투자자 변신한 中지방정부…AI 정조준한 '허페이 모델' ... https://news.nate.com/view/20240415n00213
[99] MiniMax-M1: 긴 문맥과 복잡한 문제 해결을 위한 고효율 추론 모델 https://42morrow.tistory.com/entry/MiniMax-M1-%EA%B8%B4-%EB%AC%B8%EB%A7%A5%EA%B3%BC-%EB%B3%B5%EC%9E%A1%ED%95%9C-%EB%AC%B8%EC%A0%9C-%ED%95%B4%EA%B2%B0%EC%9D%84-%EC%9C%84%ED%95%9C-%EA%B3%A0%ED%9A%A8%EC%9C%A8-%EC%B6%94%EB%A1%A0-%EB%AA%A8%EB%8D%B8
[100] 中 아이플라이텍, 챗GPT 대항할 '스파크데스크' 공개 - IT조선 https://it.chosun.com/news/articleView.html?idxno=2023050801266
[101] 4. Minimax가 새로운 AI 동영상 생성 툴 "abab-video-1"을 ... https://www.threads.com/@choi.openai/post/C_m51w_SBCl?hl=ko
[102] 우리 자신에 대해 - 오리온스타 - OrionStar Robotics https://kr.orionstar.com/about-us.html
[103] AI 투자 뜨거운 가운데, Reka 1억1000만 달러 유치로 유니콘 ... https://hyper.ai/kr/headlines/70a782dba5b1990b6780159d24fc4aab
[104] AI Startups https://www.koraia.org/default/img/_des/mp3/2020_KOREAAI.pdf
[105] Reka AI 모델 - AI 기술의 혁신과 성능 최적화 https://www.toolify.ai/ko/ai-news-kr/reka-ai-ai-2351552
[106] Reka Core, Reka.AI에서 출시한 멀티모달 대규모 언어 모델 ... https://discuss.pytorch.kr/t/reka-core-reka-ai-mllm/4086
[107] Reka AI - 기업 상세 정보 https://engine.roa.ai/companies/7pU4QU4Bkx/summary
[108] Reka AI https://reka.ai
[109] DeepSeek? 이젠 Kimi Ai!! OpenAI o1 풀버전과 경쟁 https://contents.premium.naver.com/mizumi/mijumi/contents/250128090133501bz
[110] '또 다른 딥시크 순간': 중국 AI 모델 키미 K2, 설렘을 불러 ... https://www.ainet.link/21771
[111] 中 문샷AI, 1조개 매개변수 오픈소스 모델 '키미 K2' 공개 https://m.news.nate.com/view/20250714n10058?mid=m02&list=recent&cpcd=
[112] Kimi https://namu.wiki/w/Kimi
