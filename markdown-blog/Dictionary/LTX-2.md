---
type: model
description: Lightricks가 공개한 19B 파라미터 규모의 joint audio-video foundation model. asymmetric dual-stream(비디오·오디오) 구조에 bidirectional cross-attention으로 modality imbalance를 처리. OmniNFT의 backbone으로 사용됨.
tags:
  - 영상처리
  - 머신러닝
  - 오픈소스
aliases:
  - LTX-2
  - LTX2
---

LTX-2는 Lightricks 팀의 Yoav HaCohen 외가 2026년 공개한 *Efficient joint audio-visual foundation model*입니다(arXiv:2601.03233). 같은 팀의 LTX-Video(2024, arXiv:2501.00103)에서 비디오 전용 파이프라인을 다듬은 뒤, LTX-2에서 오디오 branch와 비디오 branch를 하나의 dual-stream Transformer로 묶어 joint generation을 지원하도록 확장했습니다.

핵심은 *asymmetric dual-stream* 디자인입니다. 비디오 branch와 오디오 branch가 각자의 self-attention과 FFN으로 intra-modal generation을 처리하면서, 중간·후반부 Transformer 블록에서 A2V·V2A bidirectional cross-attention으로 cross-modal alignment를 형성합니다. LTX-2는 약 19B 파라미터로 LTX-2.3(22B)과 함께 [[OmniNFT - Modality-wise Omni Diffusion Reinforcement for Joint Audio-Video Generation|OmniNFT]] 논문의 baseline·backbone으로 활용됩니다.

OmniNFT는 LTX-2의 weight를 그대로 받아 RL fine-tuning을 얹는 *post-training* 설정입니다. backbone을 갈아끼우지 않고도 perceptual quality(VQ, AQ), text-modal alignment(TA-IB, CLAP), audio-video synchronization(JavisScore, DeSync)을 동시에 끌어올리는 길이 있다는 것이 본 논문의 메시지입니다.
