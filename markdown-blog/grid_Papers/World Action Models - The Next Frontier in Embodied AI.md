---
date: 2026-05-15
tags:
  - 논문
  - 딥러닝
  - 머신러닝
  - 멀티모달
aliases:
  - "WAM Survey"
  - "World Action Models"
image: "![[wam-overview.png]]"
description: Vision-Language-Action 모델이 학습하는 reactive observation-to-action 매핑과 World Model 계열의 예측적 dynamics 모델링이 별도의 흐름으로 흘러오다가 한 모델 안에서 합쳐지기 시작했습니다. Fudan 신뢰성 임바디드 AI 연구소가 이 합류 지점을 World Action Models로 명명하고 정의·아키텍처·데이터·평가의 네 축으로 정리한 첫 서베이를 살펴봅니다.
buzz: 181
---

> S. Wang, J. Shi, Z. Fu, X. He, F. Liu, C. Yang, Y. Zhou, Z. Fei, J. Gong, J. Fu, M. Z. Shou, X. Huang, X. Qiu, Y.-G. Jiang, "World Action Models: The Next Frontier in Embodied AI," arXiv:2605.12090, 2026.

RT-2가 등장한 뒤로 임바디드 정책 학습은 *Vision-Language-Action 모델*이라는 한 단어로 압축되어 왔습니다. VLM 백본 위에 action token을 얹어서 *관측 → 행동* 매핑을 학습하는 방식인데, 사전학습된 의미 정보를 모터 제어로 그대로 끌어 쓸 수 있다는 점에서 이전 task-specific controller와는 분명히 다른 자리에 있습니다. 그런데 이 흐름이 정점을 찍을 즈음 *세계가 어떻게 변할지를 모델이 예측하지 않는다*는 한계가 점점 부각되기 시작했습니다.

World Model 쪽 흐름은 거의 같은 시기에 별도로 굴러갔습니다. Dreamer 계열의 latent dynamics 모델, [[Yann LeCun]]이 밀던 JEPA 계열의 예측적 표현 학습, Sora·Veo·Wan 같은 비디오 생성 기반 world model이 각각 *세계의 dynamics를 모델링한다*는 같은 목표를 다른 방식으로 풀어왔습니다. 이 두 흐름이 작년 한 해를 거치면서 한 모델 안으로 합쳐지기 시작했고, 그 합쳐진 모델을 부르는 이름이 논문마다 달랐습니다. UniPi, VPP, GR-2, FLARE, VLA-JEPA, Cosmos Policy, DreamZero, X-WAM — 모두 본질은 비슷한데 명명만 다른 상황입니다.

Fudan University의 신뢰성 임바디드 AI 연구소(Institute of Trustworthy Embodied AI)는 이 합류 지점을 *World Action Models(WAMs)*로 묶고 첫 서베이를 내놓았습니다. 단순히 "이런 모델들이 있다"가 아니라 *VLA·VAM·Video Policy·AWM과 어떻게 다른가*를 정의 단에서 정리하고, Cascaded와 Joint라는 두 축으로 아키텍처 공간을 나누고, 데이터 생태계 네 갈래와 평가 프로토콜 세 갈래를 정리한 뒤 미해결 과제를 던지는 구성입니다.

## 저자

1저자 Siyin Wang과 책임저자 Yu-Gang Jiang을 포함해 14명이 이름을 올렸습니다. 대부분 Fudan University 신뢰성 임바디드 AI 연구소·Shanghai Innovation Institute 소속이고 NUS의 Mike Zheng Shou가 합류했습니다. project lead는 Zhaoye Fei입니다.

책임저자 Yu-Gang Jiang은 Fudan 컴퓨터과학과 교수이자 신뢰성 임바디드 AI 연구소를 이끄는 인물입니다. 원래는 비디오 분석·멀티모달 인식 쪽에서 오래 일해온 비전 연구자인데, 작년에 새로 출범한 임바디드 AI 연구소를 맡으면서 *비디오 생성 모델의 dynamics를 정책 학습으로 연결하는* 방향으로 그룹의 무게중심을 옮겨온 모양새입니다. 본 서베이의 시각 — *비디오 foundation 모델을 world model로 보고 그것을 정책에 통합한다* — 이 그 궤적과 자연스럽게 맞물립니다.

저자들이 OpenMOSS와 함께 GitHub에 Awesome-WAM 리포지토리를 열고 본 서베이를 공식 랜드스케이프 페이지로 운영한다고 밝힌 점도 흥미롭습니다. 명명을 정착시키려는 의도가 분명히 느껴집니다.

## 배경

본 서베이는 두 갈래를 먼저 분리해서 정리합니다. 한쪽은 VLA, 다른 한쪽은 World Model입니다.

VLA 계열은 RT-2(2023), OpenVLA(2024), π₀(2024)를 큰 마일스톤으로 잡습니다. 셋 다 *o, l을 받아 a를 내는* 조건부 확률 p(a | o, l) 학습이라는 점이 같습니다. 행동 생성 방식만 갈리는데, autoregressive tokenization 계열은 action을 discrete token으로 다루고, diffusion synthesis 계열은 VLM 백본에 generative action expert를 붙여 continuous multi-modal 분포를 다룹니다. 본 서베이의 진단은 *VLA가 reactive observation-to-action 매핑에 갇혀 있다*는 것입니다. 환경이 개입에 어떻게 반응할지를 모델이 명시적으로 그리지 않으니 generalization에 한계가 생기고, action annotation이 붙은 데이터에만 의존하니 학습 자원이 제한된다는 두 문제로 정리됩니다.

World Model 계열은 더 다양한 정의가 공존하던 영역입니다. 본 서베이는 *환경의 forward dynamics를 모델링하는 함수* — p(o' | o, a) — 로 통일하고 세 갈래로 나눕니다.

- *action-conditioned world model*: 행동 a로 조건화해서 다음 관측 o'를 예측합니다. Explicit pixel-level 계열에는 ACVP·CDNA·iVideoGPT·Genie·Diffusion World Model이 있고, implicit latent dynamics 계열에는 PlaNet의 RSSM, Dreamer 시리즈, TransDreamer의 TSSM, JEPA·V-JEPA 2·LeWorldModel이 들어갑니다.
- *language-conditioned world model*: a 대신 l로 조건화하는 흐름입니다. MoCoGAN·U-Net·Latte·Wan·Sora 2 같은 video foundation model이 여기 들어갑니다.
- *embodied world model*: 임바디드 환경 특화. SWIM·DreamDojo·DexWM·RoboDreamer·RoboScape·WoW가 사례입니다.

이 두 갈래가 만나는 첫 시도가 *VLA를 위한 World Model* 사용입니다. Imitation learning에서는 Ctrl-World가 π₀.₅-DROID 정책의 downstream 성공률을 *44.7%* 끌어올리며 imagination에서의 fine-tuning이 실제로 효과적임을 보였습니다. RL 쪽에서는 Dreamer 계열을 surrogate environment로 쓰는 흐름, VIPER·Diffusion Reward·GenReward·SRPO처럼 video generation을 reward 신호로 쓰는 흐름이 같이 갔습니다. 평가 측면에서는 Ctrl-World·Veo Robotics·Interactive World Simulator처럼 world model을 *시뮬레이터*로 쓰는 흐름이 자리잡았습니다.

그러나 여기까지는 world model이 정책 *바깥*에 있는 도구로 쓰였습니다. WAM은 그 도구를 정책 *안*으로 가져오는 단계의 모델들을 가리킵니다.

## 어떻게 정의했나

본 서베이의 WAM 정의는 두 조건으로 압축됩니다.

- **Forward Predictive Modeling**: 모델이 미래 상태 o'의 양화 가능한 표현을 *생성하거나 활용*해야 합니다. 픽셀 수준 비디오, dense optical flow, physics-grounded latent 무엇이든 됩니다.
- **Coupled Action Generation**: 모델이 motor command a를 *예측된 미래 상태 o'에 정렬*시켜야 합니다. joint probabilistic output이든, cascaded·unified latent 안의 policy conditioning이든 결합 방식은 자유롭게 둡니다.

수식으로는 다음 joint(또는 조건부) 분포를 학습한다는 것입니다.

$$\mathcal{L}_{\text{WAM}} = \mathbb{E}_{(o, l, o', a) \sim \mathcal{D}} \left[ -\log p(o', a \mid o, l) \right]$$

VLA는 p(a | o, l)만 학습하고, World Model은 p(o' | o, a)만 학습하던 자리에 *둘을 함께 학습하는* 객체로 WAM이 들어가는 셈입니다.

비슷한 명명이 이미 있었습니다. *Action World Model(AWM)*은 같은 객체를 다른 위계로 부른 단어입니다. AWM은 "World Model"이 주어 자리에 있어서 *행동으로 augment된 시뮬레이터*라는 뉘앙스가 강하고, WAM은 "Action"과 "World"를 동격에 두어 *에이전트가 본체*라는 뉘앙스가 강합니다. 저자들은 이 차이를 *VLA 계보의 직접 후계자*임을 분명히 하려는 의도라고 명시합니다. 이 점은 [[Yann LeCun]]이 밀어온 *world model 중심 에이전트* 비전과 미묘하게 다릅니다. LeCun식 비전은 world model을 핵심으로 두고 정책을 그 위에서 planning으로 풀자는 입장에 가깝습니다. WAM은 *world와 action을 동시에 학습 객체로 두는* 합류점입니다. 명명이 정착할지는 별도로 봐야 할 부분입니다.

WAM과 인접 개념의 경계도 따로 정리됩니다. *Video Action Models(VAMs)*는 video 합성과 action 생성을 정렬하는 모델이라 WAM의 부분집합입니다. *Video Policies*는 video diffusion backbone을 정책으로 직접 쓰는 모델인데, world modeling objective로 *명시적으로* supervise되어야 WAM이 됩니다. backbone의 implicit 정보만 활용하면 video policy로 분류됩니다.

## 무엇으로 구성돼 있나

서베이는 WAM을 두 paradigm으로 나눕니다.

**Cascaded WAM**은 *p(o', a | o, l) = p(a | o', o, l)·p(o' | o, l)*로 명시적으로 factorize합니다. world model이 먼저 미래를 합성하고, 그 미래를 보고 action model이 행동을 뽑는 구조입니다. 두 모델이 따로 학습됩니다.

Cascaded 안에서 다시 두 갈래로 나뉩니다.

- *Explicit Planning via Pixel-Space Representations*: UniPi(T2V 비디오 + IDM), VLP(VLM hierarchy + tree search), RoboEnvision(OpenSora DiT), ThisThat(deictic gesture 조건), Say Dream and Act(adversarial distillation), TesserAct(RGB+depth+normal 4D), MVISTA-4D(WAN2.2 TI2V), Vidar(human → robot), Gen2Act(VideoPoet zero-shot), Veo-Act(Veo-3 + π₀.₇), VAG, π₀.₇. action 추출은 학습된 IDM이거나 geometric pipeline(AVDC, Im2Flow2Act, 3DFlowAction, NovaFlow, Dream2Flow, Dreamitate, 4DGen, RIGVid, LVP)입니다.
- *Implicit Planning via Latent Representations*: pixel 합성 비용을 피하고 diffusion intermediate latent를 planning carrier로 씁니다. VPP, VILP, S-VAM, Video Policy, ARDuP, mimic-video, MWM, OmniVTA, LAPA, villa-X가 있습니다. VPP는 *pretrained VAE 인코더 + single-step latent 예측 + lightweight policy*로 real-time inference에 성공한 첫 사례로 정리됩니다.

**Joint WAM**은 *p(o', a | o, l)*을 단일 모델에서 직접 다룹니다. world prediction과 action generation이 같은 객체 안에서 *공동 최적화*됩니다.

Joint 안에서 다시 두 갈래입니다.

- *Autoregressive Generation*: causal sequence modeling으로 둘을 한 트랜스포머에 넣습니다.
  - *Explicit Decoupled*: GR-1(195M), GR-MG, GR-2(30~719M)처럼 visual patch와 continuous action을 분리된 head로 디코딩합니다.
  - *Unified Discrete*: CoT-VLA(7B), WorldVLA(7B), RynnVLA-002(5B), F₁(4.2B MoT)처럼 vision과 action을 같은 discrete token 공간에 집어넣어 next-token prediction으로 다룹니다.
  - *Predictive Latent*: VLA-JEPA(2B, Qwen3-VL-2B 기반)는 latent space에서만 transition을 예측해 pixel reconstruction을 우회합니다.
- *Diffusion-based Generation*: multi-step denoising으로 future state와 action을 *동시에* 생성합니다. 본 서베이 분류에서 가장 풍성한 줄기입니다.
  - *Unified Stream*: 하나의 DiT 안에 world와 action을 같이 흘립니다. PAD, VideoVLA(5B, CogVideoX-5B), UWM(독립 noise schedule), DreamZero(14B, Wan2.1-I2V-14B-480P), Cosmos Policy(2B), GigaWorld-Policy(5B), X-WAM(5B RGB-D 분기), FLARE, FRAPPE(1B), UD-VLA가 들어갑니다.
  - *Multi-Stream*: video DiT와 action DiT를 따로 두고 cross-attention(CoVAR·LDA-1B·DUST·LingBot-VA(5.3B Wan2.2-5B)·DexWorldModel·AIM·Motus(8B)·MotuBrain·AdaWorldPolicy)·hidden state(DiT4DiT·Fast-WAM(6B)·WAV(2.2B)·Act2Goal(1.76B))·shared representation(UVA(0.5B)·PhysGen(0.73B)) 중 하나로 결합합니다.

본 서베이가 강조하는 *축*은 두 가지입니다. backbone scale은 0.5B(UVA)부터 14B(DreamZero)까지 한 자릿수 차이로 벌어지고, world representation은 RGB·RGB-D·latent·flow·tactile로 다양화되고 있다는 점입니다. 한 표(Table 3)에 들어가는 diffusion-based joint WAM만 21개입니다.

## 데이터

WAM 훈련 데이터는 네 갈래로 정리됩니다.

- **Robot-centric Teleoperation**: action-state pair가 가장 정확합니다. QT-Opt(580k traj), MIME(8,260 traj), RoboNet(약 162k traj), BridgeData(7.2k), MT-Opt(800k), BC-Z(25.9k), RT-1(130k+), Language-Table(594k), BridgeData v2(60k+), RH20T(110k), OXE(*1M+ trajectories, 22개 로봇, 60개 환경*), DROID(76k), ARIO(3M+, 35 robots, 378 envs), AgiBot World(1M+, AgiBot G1, 87 skills), UnifoLM-WBT(1,892,118 traj, Unitree G1)까지 스케일이 확장됩니다.
- **Portable Human Demonstrations (UMI-style)**: UMI 핸드헬드 그리퍼 계열입니다. FastUMI-Data(10k+ traj), FastUMI-100K(*100k+ traj*), RealOmin(1M traj, *3,000+ 환경*), Hoi!(3,048 traj), RDT2(*10,000시간*)까지 갑니다. *환경 다양성은 인터넷 비디오에 가깝고 action 정밀도는 로봇에 가까운* 중간 지점을 차지합니다.
- **Simulation**: MimicGen·ManiSkill2·RoboCasa(100k+ traj, 120 envs)·RoboTwin·DexMimicGen·QUARD-Auto·TesserAct(285k clips)·RoboCerebra·SynGrasp-1B(*10M traj*)·RoboTwin 2.0·TLA Dataset(24k tactile-action pairs)·InternData-M1(244k)·InternData-A1(*630k traj, 227 envs*). privileged information(정확한 depth·접촉 위치·다중 시점)을 거의 무한히 뽑을 수 있다는 점이 강점입니다.
- **Human and Ego-Centric Data**: SSv2(108,499 clips), EPIC-KITCHENS(55h), HowTo100M(*136M clips*), Kinetics-700(650k), Ego4D(*3,670h*), HOI4D, EgoVid-5M, COM Kitchens, Egocentric-10K, DreamDojo-HV(*43,827h*), Assembly101, H2O, EgoPAT3D(1M frames), Ego-Exo4D(1,286h), ARCTIC, HOT3D, TACO, Aria Everyday Activities(7.3h), OAKINK2, Nymeria(300h), HD-EPIC(41.3h), EgoDex(829h, 194 tasks), EgoScale(20,854h, 9,869 envs), HumanNet(*1M hours*). action annotation은 없지만 *세계 dynamics 자체*는 가장 풍부합니다.

저자들이 그리는 그림(Figure 7)은 두 축 — Transfer Difficulty(로봇으로 옮기기 어려움)와 Scaling Difficulty(데이터 모으기 어려움) — 의 trade-off에 네 데이터 paradigm이 정확히 반대편에 놓인다는 것입니다. teleop은 *transfer는 쉽고 scaling이 어렵고*, ego는 *scaling은 쉽고 transfer가 어려운* 극단입니다. WAM의 강점은 *unpaired data*(action 없이 o, o'만 있는 데이터)도 joint training으로 흡수할 수 있다는 점에서 옵니다. PAD가 video co-training을 ablation으로 검증한 사례, DreamDojo의 44,000시간 crowdsourced 데이터가 그 가능성을 보여줍니다.

## 평가

본 서베이는 평가를 두 축으로 분리합니다.

**World Modeling Capability**는 다시 셋으로 나뉩니다.

- *Visual Fidelity*: PSNR, SSIM, LPIPS, DreamSim, DINO similarity, FVD. 가장 표면적인 평가입니다.
- *Physical Commonsense*: VideoPhy, PhyGenBench(PhyGenEval), VBench-2.0(mechanical·thermal·material state changes), WorldModelBench(*Newton 1st law·mass conservation·rigid body·fluid·impenetrability·gravity 5개 binary check*), Physics-IQ(Spatial IoU·Spatiotemporal IoU·Weighted Spatial IoU·MSE). object dynamics와 trajectory plausibility의 *물리적 일관성*을 봅니다.
- *Action Plausibility*: WorldSimBench(Implicit Manipulative Evaluation), Wow, wo, val!(Inverse Dynamics Modeling Turing Test). *생성된 비디오가 그럴듯해 보여도 실제로 IDM을 통과해 실행 가능한 action으로 변환되는가*를 봅니다. Wow 결과는 *시각적으로 그럴듯한 모델이 IDM Turing Test에서 거의 0에 가까운 성공률로 무너지는* 경우가 많다는 점을 짚습니다. action plausibility가 visual realism과 *별개 축*이라는 핵심 관찰입니다.

**Action Policy Capability**는 다섯 갈래로 정리됩니다.

- *General Manipulation*: MetaWorld(50 tasks)·RLBench(100 tasks)·CALVIN·LIBERO(67 obj, 130 tasks)·LIBERO-plus(10,030 tasks)·COLOSSEUM·LIBERO-pro·Libero-X(60+ obj, 600 tasks)·AGNOSTOS·GemBench·SimplerEnv·RoboCasa·VLABench(2000+ obj, 100 tasks)·RoboMME·RoboVerse(5,500 obj, 276 tasks, 500K traj)·PolaRiS 등 40개 이상.
- *Bimanual and Humanoid*: RoboTwin(Aloha-AgileX), BiGym(Unitree H1, 40 tasks), HumanoidBench(Unitree H1 + Shadow-Hand, *448 tactile sensing points*, 27 tasks + 12 locomotion), HumanoidGen(*200K+ traj*).
- *Mobile Manipulation*: ManipulaTHOR(28 tasks), HomeRobot(7,892 obj), BEHAVIOR-1K(*1,000 tasks*, OmniGibson).
- *Contact and Deformation*: SoftGym, PlasticineLab, DaXBench, TacSL, ManiFeel.
- *Real-Robot*: RoboArena, RoboChallenge(30 tasks), Maniparena(X2Robot·Quanta X1 dual platform, *10,812 trajectories*).

저자들의 진단은 분명합니다. *visual metric은 physical correctness를 못 잡고*, *action success는 imagined future와의 alignment를 못 잡는다*. 둘이 분리되어 leaderboard로 굴러가는 동안 *causal consistency*는 빠져 있다는 게 결정적 gap입니다. Counterfactual Consistency, Foresight-Conditioned Success 같은 *coupled* metric이 필요하다는 게 본 서베이의 제안입니다.

## 회고

저자들이 직접 짚는 open challenge가 일곱입니다.

- **Architectural Coupling**: cascade vs joint, autoregressive vs diffusion, unified stream vs multi-stream을 *동일 조건에서* 비교한 ablation이 없습니다. 어떤 inductive bias가 어떤 task에 유리한지 empirical하게 불분명합니다. 한 단계 더 나아가 *그래서 explicit pixel prediction이 필요하긴 한가*가 진짜 질문입니다. test time에 future prediction head를 떼어도 control 성능이 안 떨어진다는 보고가 늘고 있고, 그게 사실이라면 JEPA 같은 latent-predictive 접근이 핵심이 됩니다.
- **Multimodal Physical State Representation**: 거의 모든 WAM이 RGB future만 예측합니다. 그런데 contact-rich 조작에 결정적인 정보 — tactile distribution, contact force, acoustic signature, material compliance — 는 픽셀에 안 보입니다. 정작 가장 필요한 자리에서 *예측의 사각지대*가 생긴다는 지적입니다.
- **Data Mixture Design**: human video를 *얼마나*, *어느 단계에*, *어떤 비율로* 섞을지에 대한 원리가 없습니다. 본 서베이는 transferable knowledge를 *low-level physical priors*(중력·항존성), *mid-level causal dynamics*(접촉 → 반응), *high-level task logic* 셋으로 위계화합니다. 각 층이 어디서 학습되는 게 효율적인지는 미해결입니다.
- **Long-Horizon Planning and Temporal Abstraction**: 현재 WAM은 *single interaction context* 안의 단기 조작에서 평가됩니다. 누적 drift, action error compounding, 긴 trajectory의 generative 표현 자체가 풀리지 않습니다. 저자들은 modular hierarchy, intrinsic hierarchical WAM, temporal context scaling 셋을 가능한 방향으로 제시합니다.
- **Inference Latency**: DreamZero가 system-level 최적화로 *7Hz*까지 끌어왔지만 *non-generative VLA의 50Hz*에 한참 못 미칩니다. *high-fidelity prediction vs real-time control*의 trade-off가 본질 문제입니다. task-adaptive predictive fidelity가 해법 후보로 제시됩니다.
- **Evaluation Methodology**: 위에서 정리한 *causal consistency* 부재 문제입니다. Counterfactual Consistency, Foresight-Conditioned Success 같은 coupled metric이 필요합니다.
- **Safety**: world model이 *틀린 미래*에 confidently 정렬해 긴 action sequence를 실행하면 reactive policy보다 *복구 어려운* 실패가 납니다. 같은 예측 capacity가 prediction-integrated safety — 실행 전에 imagined future를 physical constraint로 검증 — 의 자원이 될 수 있다는 양면성을 짚습니다.

휴머노이드·자율주행·게임 에이전트 같은 응용 도메인 관점에서 보면 다음이 직접 따라옵니다. 휴머노이드는 HumanoidBench·HumanoidGen·UnifoLM-WBT 라인이 *full-body·tactile-rich* 평가를 표준화하는 중이고, 본 서베이는 RDT2·EgoDex·HumanNet 같은 human ego 데이터가 휴머노이드 morphology에 가장 자연스럽게 정렬된다는 흐름을 짚습니다. 자율주행은 본 서베이가 직접 다루지 않지만, 같은 *p(o', a | o, l)* 객체가 driving scene으로 옮겨오면 GAIA·DriveDreamer 계열과 자연스럽게 연결됩니다. 게임 에이전트는 Genie 계열이 이미 보여준 *latent action* 추출 방식이 본 서베이의 Implicit Planning과 같은 구조라서 둘이 합쳐질 여지가 큽니다.

## 정리

- *WAM*은 VLA의 reactive 한계와 World Model의 분리 학습 한계를 동시에 푸는 합류점이고, 본 서베이는 Cascaded(Explicit·Implicit)와 Joint(Autoregressive·Diffusion×Unified·Multi-Stream)로 약 90개의 최근 모델을 정리한 첫 체계화입니다.
- 데이터·평가 정리가 더 실용적입니다. teleop·UMI·simulation·human ego 네 갈래의 trade-off 그림, 그리고 *visual fidelity·physical commonsense·action plausibility* 평가 3축 — 특히 visual quality와 IDM Turing Test 사이의 큰 gap을 *분명히 분리해 평가하라*는 지적이 핵심입니다.
- 미해결 과제 중 *explicit pixel prediction이 정말 필요한가*, *RGB 외 modality를 어떻게 잡을 것인가*, *causal consistency를 어떻게 측정할 것인가* 셋이 다음 한 해의 방향을 가를 자리에 있습니다. WAM 명명이 정착하든 안 하든, *p(o', a | o, l) 객체로 묶어 보는 시각* 자체는 더 빨리 정착할 가능성이 큽니다.
