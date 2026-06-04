<div align="center">

# FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions

  <img src="./assets/hi_logo.jpg" alt="FRoM-W1" width="7.5%">

  Core Contributors: [Peng Li](https://artpli.github.io/), [Zihan Zhuang](https://github.com/HansZ8), [Yangfan Gao](https://github.com/SchweitzerGAO), [Yi Dong](mailto:yidong25@m.fudan.edu.cn), [Sixian Li](mailto:sxli25@m.fudan.edu.cn), [Changhao Jiang](mailto:chjiang25@m.fudan.edu.cn), [Tao Gui](https://guitaowufeng.github.io/), [Xipeng Qiu](https://xpqiu.github.io/en.html)

  The [Humanoid Intelligence Team](https://github.com/humanoidintelligence) from [FudanNLP](https://nlp.fudan.edu.cn/nlpen/main.htm) and [OpenMOSS](https://openmoss.github.io/)

<p align="center">
  <a href="https://openmoss.github.io/FRoM-W1/">
    <img src="https://img.shields.io/badge/Project-Webpage-blue.svg" alt="Project Webpage"/>
  </a>
  <a href="https://arxiv.org/abs/2601.12799">
    <img src="https://img.shields.io/badge/arXiv-2601.12799-b31b1b.svg" alt="Paper on arXiv"/>
  </a>
  <a href="https://github.com/OpenMOSS/FRoM-W1">
    <img src="https://img.shields.io/badge/GitHub-Code-black.svg?logo=github" alt="GitHub Code"/>
  </a>
  <a href="https://huggingface.co/datasets/OpenMOSS-Team/FRoM-W1-Datasets">
    <img src="https://img.shields.io/badge/🤗%20Hugging%20Face-Data-yellow.svg" alt="Hugging Face Data"/>
  </a>
  <a href="https://huggingface.co/OpenMOSS-Team/FRoM-W1">
    <img src="https://img.shields.io/badge/🤗%20Hugging%20Face-Model-yellow.svg" alt="Hugging Face Model"/>
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License"/>
  </a>
</p>

</div>

> **📌 Status**: This is a **research release** of the FRoM-W1 framework. The initial codebase, model checkpoints, datasets, and deployment framework are all open-source. More powerful models and improved training recipes are under development. Contributions, issues, and PRs are welcome!

## 🔥 Introduction
<div align="center">
  <img src="./assets/FRoM-W1-Teaser.png" alt="FRoM-W1" width="50%">
</div>

> For more information, please refer to our [project page](https://openmoss.github.io/FRoM-W1/) and [technical report](https://arxiv.org/abs/2601.12799).

Humanoid robots are capable of performing various actions such as greeting, dancing and even backflipping. However, these motions are often hard-coded or specifically trained, which limits their versatility. In this work, we present **FRoM-W1**, an open-source framework designed to achieve general humanoid whole-body motion control using natural language.

To universally understand natural language and generate corresponding motions, as well as enable various humanoid robots to stably execute these motions in the physical world under gravity, **FRoM-W1** operates in two stages:

**(a) H-GPT**  
Utilizing massive human data, a large-scale language-driven human whole-body motion generation model is trained to generate diverse natural behaviors. We further leverage the Chain-of-Thought technique to improve the model's generalization in instruction understanding.

**(b) H-ACT**  
After retargeting generated human whole-body motions into robot-specific actions, a motion controller that is pretrained and further fine-tuned through reinforcement learning in physical simulation enables humanoid robots to accurately and stably perform corresponding actions. It is then deployed on real robots via a modular sim-to-real module.

We extensively evaluate **FRoM-W1** on Unitree H1 and G1 robots. Results demonstrate superior performance on the HumanML3D-X benchmark for human whole-body motion generation, and our introduced reinforcement learning fine-tuning consistently improves both motion tracking accuracy and task success rates of these humanoid robots. We open-source the entire **FRoM-W1** framework and hope it will advance the development of humanoid intelligence.

## 📑 Roadmap

- [x] 🎉 Release the initial codebase for the **[H-GPT](./H-GPT/README.md)** and **[H-ACT](./H-ACT/README.md)** modules
- [x] 🎉 Release the amazing humanoid-robot deployment framework **[RoboJuDo](https://github.com/HansZ8/RoboJuDo)**
- [x] Release the CoT datasets of the HumanML3D-X and Motion-X benchmarks, and the δHumanML3D-X benchmark
- [x] Release checkpoints for the baseline models, SMPL-X version of T2M, MotionDiffuse, MLD, T2M-GPT
- [x] 🎉 Release the **[Technical Report](https://arxiv.org/abs/2601.12799)** and **[Project Page](https://openmoss.github.io/FRoM-W1/)** of FRoM-W1!
- [ ] More powerful models are working in progress

## 💾 Datasets

Due to license restrictions, we cannot publicly share all of the data. Here are the reference download and processing links for the relevant datasets:

<details>
<summary><b>H-GPT Module</b> (click to expand)</summary>

| **Dataset Name** | **Download Guide** |
|:----------------:|:------------------:|
|     HumanML3D     | Please refer to the original [HumanML3D](https://github.com/EricGuo5513/HumanML3D) repo. This link [HumanML3D](https://drive.google.com/drive/folders/1OZrTlAGRvLjXhXwnRiOC-oxYry1vf-Uu) may be useful.|
|     KIT-ML     | Please refer to the original [KIT-ML](https://motion-annotation.humanoids.kit.edu/dataset/) repo. This link [KIT-ML](https://drive.google.com/drive/folders/1D3bf2G2o4Hv-Ale26YW18r1Wrh7oIAwK) may be useful.|
|     Motion-X     | Please refer to the original [Motion-X](https://github.com/IDEA-Research/Motion-X) repo. We add a Motion-X processing document [HERE](./H-GPT/motionx_processing.md).|
|    HumanML3D-X   | Please refer to the process in the [Motion-X](https://github.com/IDEA-Research/Motion-X) repo and [this document](./H-GPT/motionx_processing.md) to download and process the corresponding AMASS data. We re-calculate the mean and std for this dataset, and use the original HumanML3D train/dev/test split. The CoT part can be downloaded [here](https://huggingface.co/datasets/OpenMOSS-Team/FRoM-W1-Datasets/tree/main/data).|
|   δHumanML3D-X   | After obtaining the HumanML3D-X data, replace the textual instructions in it with the perturbed versions provided [here](https://huggingface.co/datasets/OpenMOSS-Team/FRoM-W1-Datasets/tree/main/data). |

Each dataset should be organized like the following structure,

```bash
H-GPT/datasets/{dataset_name}/data/
|-- new_joint_vecs
|-- new_joints
|-- texts
|-- cots
|-- Mean.npy
|-- Std.npy
|-- all.txt
|-- train.txt
|-- train_val.txt
|-- val.txt
`-- test.txt
```
</details>

<details>
<summary><b>H-ACT Module</b> (click to expand)</summary>

| **Dataset Name** | **Download Guide** |
|:----------------:|:------------------:|
|       AMASS      | Please refer to the download and processing procedures for the [AMASS](https://amass.is.tue.mpg.de/index.html) dataset in the [human2humanoid](https://github.com/LeCAR-Lab/human2humanoid?tab=readme-ov-file#amass-dataset-preparation) project. |
|     AMASS-H1     | The retargeted dataset for the Unitree H1 can be obtained from the [link](https://cmu.app.box.com/s/vfi619ox7lwf2hzzi710p3g2l59aeczv) provided by human2humanoid.|
|     AMASS-G1     | We provide a retargeted dataset for the Unitree G1, please refer to this [link](TBD). |
</details>

## 📏 Baselines
We have invested significant effort in retraining the following baseline models using the **SMPL-X** version of the data, and we have now **fully open-sourced** them.

**Our Codebases**

- [T2M: Generating Diverse and Natural 3D Human Motions from Texts](https://github.com/humanoidintelligence/text-to-motion-smplx)
- [MotionDiffuse: Text-Driven Human Motion Generation with Diffusion Model](https://github.com/humanoidintelligence/motion-diffuse-smplx)
- [MLD: Executing your Commands via Motion Diffusion in Latent Space](https://github.com/humanoidintelligence/motion-latent-diffusion-smplx)
- [T2M-GPT: Generating Human Motion from Textual Descriptions with Discrete Representations](https://github.com/humanoidintelligence/t2m-gpt-smplx)

**Baseline Models**
- Eval Model: [HuggingFace link](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/eval), which were trained following the [T2M](https://github.com/EricGuo5513/text-to-motion) pipeline with the SMPL-X format.
- Models: [HuggingFace link](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/baselines), including the SMPL-X version of the [T2M](https://github.com/EricGuo5513/text-to-motion), [MotionDiffuse](https://github.com/MotrixLab/MotionDiffuse), [MLD](https://github.com/ChenFengYe/motion-latent-diffusion/tree/main) and [T2M-GPT](https://github.com/Mael-zys/T2M-GPT) models.

## 🧠 Models

To keep this repo organized, we provide a subset of core model checkpoints below. If you require additional model checkpoints, please contact us.

<details>
<summary><b>H-GPT Module</b> (click to expand)</summary>

| **Model Name** | **Download Guide** |
|:--------------:|:------------------:|
|  H-GPT w.o. CoT  |  [HuggingFace link](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hgpt/humanml3d-x/lora/llama-3.1-nocot_maskinput_pkeep), you can refer to this [script](https://huggingface.co/OpenMOSS-Team/FRoM-W1/blob/main/lora_merge.py) to merge these LoRA parameters with the original [Llama-3.1](https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md) model. |
|       H-GPT      |  [HuggingFace link](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hgpt/humanml3d-x/lora/llama-3.1-cot_maskinput_pkeep), you can refer to this [script](https://huggingface.co/OpenMOSS-Team/FRoM-W1/blob/main/lora_merge.py) to merge these LoRA parameters with the original [Llama-3.1](https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md) model.  |
| H-GPT++ w.o. CoT |  [HuggingFace link](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hgpt/motionx/lora/llama-3.1-nocot), you can refer to this [script](https://huggingface.co/OpenMOSS-Team/FRoM-W1/blob/main/lora_merge.py) to merge these LoRA parameters with the original [Llama-3.1](https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md) model. |
|      H-GPT++     |  [HuggingFace link](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hgpt/motionx/lora/llama-3.1-cot), you can refer to this [script](https://huggingface.co/OpenMOSS-Team/FRoM-W1/blob/main/lora_merge.py) to merge these LoRA parameters with the original [Llama-3.1](https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md) model.    |
</details>

<details>
<summary><b>H-ACT Module</b> (click to expand)</summary>

| **Model Name** | **Download Guide** |
|:--------------:|:------------------:|
|      H1-Full     |   Teacher Policy (TBD), [Student Policy](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hact/h1/25_12_10_14-16-23_OmniH2O_STUDENT)      |
|      H1-Clean    |   Teacher Policy (TBD), [Student Policy](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hact/h1/25_12_10_14-13-33_OmniH2O_STUDENT_filter)      |
|      G1-Full     |   Teacher Policy (TBD), [Student Policy](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hact/g1/25_12_11_18-16-37_OmniH2O_STUDENT)      |
|      G1-Clean    |   Teacher Policy (TBD), [Student Policy](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hact/g1/25_12_11_18-18-10_OmniH2O_STUDENT_FILTER)      |

</details>

## 🏗️ Repository Structure

```
FRoM-W1/
├── H-GPT/           # Motion generation module
│   ├── hGPT/        #  Core Python package (models, data, metrics, losses)
│   ├── configs/     #  OmegaConf YAML configs (experiments + architectures)
│   ├── scripts/     #  Inference entry points
│   └── motionx_processing.md  # Dataset preparation guide
├── H-ACT/           # Action execution module
│   ├── retarget/    #  SMPL-X → robot joint retargeting
│   └── RoboJuDo/    #  Sim-to-real deployment framework (git submodule)
├── assets/          #  Images and media
├── requirements.txt
├── README.md
└── QUICKSTART.md
```

## 🚀 Quick Start

### Pipeline Overview

```
Text Instruction
      ↓
[1] H-GPT Motion Generation  (language → 623-dim SMPL-X motion features)
      ↓
[2] Human-to-Robot Retargeting  (SMPL-X → robot joint angles for H1/G1)
      ↓
[3] Policy Training  (RL in simulation via Human2Humanoid / Beyondmimic / TWIST)
      ↓
[4] Sim-to-Real Deployment  (RoboJuDo framework)
      ↓
  Real Humanoid Robot Execution
```

### Minimal Inference Pipeline

```bash
# 1. Setup
conda create -n fromw1 python=3.10
conda activate fromw1
pip install -r requirements.txt

# 2. Generate whole-body motion from text (H-GPT)
cd H-GPT
CUDA_VISIBLE_DEVICES=0 python -m scripts.demo \
  --cfg_assets ./configs/assets.yaml \
  --cfg configs/exp/1217_config_motionx_stage2_body_hands_llama_vqvae2kx1k_cotv3_t2mx.yaml \
  --task t2m \
  --example ./scripts/instructions.txt

# 3. Visualize the generated motion
python -m hGPT.data.motionx.visualization.plot_3d_global \
  --path ./results/<result_folder>

# 4. Retarget to robot joints (H-ACT)
cd ../H-ACT/retarget
python main.py
```

> Full setup instructions — including dataset preparation, model downloads, deps folder structure, and deployment — are in the **[QUICKSTART.md](./QUICKSTART.md)** guide.

## 🛠️ Model Training and Evaluation

### H-GPT

Training proceeds in two stages:

| Stage | Config Field | Description |
|---|---|---|
| **VQ-VAE** | `TRAIN.STAGE: "vae"` | Train the whole-body motion tokenizer (convolutional encoder/decoder + vector quantization) |
| **LM Pretrain** | `TRAIN.STAGE: "lm_pretrain"` | Finetune Llama-3.1-8B via LoRA to generate motion tokens (VQ-VAE frozen) |
| **LM Instruct** | `TRAIN.STAGE: "lm_instruct"` | Instruction-tune with Chain-of-Thought data |

Refer to the [H-GPT README](./H-GPT/README.md) for detailed training commands, dataset preparation, and evaluation protocols.

### H-ACT

Policy training options:

- **Human2Humanoid** — RL-based motion tracking policy. See the [official repo](https://github.com/LeCAR-Lab/human2humanoid) for training instructions.
- **Beyondmimic** — CSV-formatted motion data required; run `scripts/pkl_2_csv.py` first.
- **TWIST** — Refer to the [official TWIST docs](https://github.com/YanjieZe/TWIST).

For sim-to-real deployment and pretrained policies, refer to the **[RoboJuDo](https://github.com/HansZ8/RoboJuDo)** framework.

We extend our gratitude to Biao Jiang for discussions and assistance regarding the motion generation models, to Tairan He and Ziwen Zhuang for their discussions and help in the motion tracking section.

And we thank all the relevant open-source datasets and open-source codes; it is these open-source projects that have propelled the advancement of the entire field!

## 📄 Citation
If you find our work useful, please star ⭐ our GitHub Repo and cite it in the following way:

```bibtex
@article{DBLP:journals/corr/abs-2601-12799,
  author       = {Peng Li and
                  Zihan Zhuang and
                  Yangfan Gao and
                  Yi Dong and
                  Sixian Li and
                  Changhao Jiang and
                  Shihan Dou and
                  Zhiheng Xi and
                  Enyu Zhou and
                  Jixuan Huang and
                  Hui Li and
                  Jingjing Gong and
                  Xingjun Ma and
                  Tao Gui and
                  Zuxuan Wu and
                  Qi Zhang and
                  Xuanjing Huang and
                  Yu{-}Gang Jiang and
                  Xipeng Qiu},
  title        = {FRoM-W1: Towards General Humanoid Whole-Body Control with Language
                  Instructions},
  journal      = {CoRR},
  volume       = {abs/2601.12799},
  year         = {2026},
  url          = {https://doi.org/10.48550/arXiv.2601.12799},
  doi          = {10.48550/ARXIV.2601.12799},
  eprinttype   = {arXiv},
  eprint       = {2601.12799},
  timestamp    = {Tue, 24 Mar 2026 08:45:06 +0100},
  biburl       = {https://dblp.org/rec/journals/corr/abs-2601-12799.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```
