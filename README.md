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

> **📌 Status**: Research release — the initial codebase, model checkpoints, datasets, and deployment framework are fully open-source. More powerful models and improved training recipes are under development. Contributions, issues, and PRs are welcome!

## 🔥 Introduction

<div align="center">
  <img src="./assets/FRoM-W1-Teaser.png" alt="FRoM-W1" width="50%">
</div>

> For more information, refer to our [project page](https://openmoss.github.io/FRoM-W1/) and [technical report](https://arxiv.org/abs/2601.12799).

Humanoid robots can perform diverse actions — greeting, dancing, backflipping — but these motions are typically hard-coded or task-specific. **FRoM-W1** is an open-source framework for general humanoid whole-body motion control using natural language, operating in two stages:

1. **H-GPT** — A language-driven whole-body motion generation model trained on large-scale human motion data. Uses Chain-of-Thought (CoT) prompting to improve instruction understanding and generalization.

2. **H-ACT** — Retargets generated human motions into robot-specific actions, trains motion tracking policies via RL in simulation, and deploys them on real robots through a modular sim-to-real framework.

We evaluate FRoM-W1 on Unitree H1 and G1 robots. Results show strong performance on the HumanML3D-X benchmark for whole-body motion generation, and RL fine-tuning consistently improves both tracking accuracy and task success rates.

## 📑 Roadmap

- [x] 🎉 **H-GPT** and **H-ACT** module codebases ([H-GPT](./H-GPT/README.md), [H-ACT](./H-ACT/README.md))
- [x] 🎉 Sim-to-real deployment framework **[RoboJuDo](https://github.com/humanoidintelligence/RoboJuDo)**
- [x] CoT datasets (HumanML3D-X, Motion-X) and δHumanML3D-X benchmark
- [x] SMPL-X baselines and eval model checkpoints (T2M, MotionDiffuse, MLD, T2M-GPT)
- [x] 🎉 [Technical Report](https://arxiv.org/abs/2601.12799) and [Project Page](https://openmoss.github.io/FRoM-W1/)
- [ ] More powerful models (in progress)

## 💾 Datasets

Due to license restrictions, we cannot publicly share all data. Below are download and processing references.

<details>
<summary><b>H-GPT Module</b> (click to expand)</summary>

| Dataset | Download Guide |
|:-------:|:-------------:|
| HumanML3D | Original [HumanML3D](https://github.com/EricGuo5513/HumanML3D) repo — [backup link](https://drive.google.com/drive/folders/1OZrTlAGRvLjXhXwnRiOC-oxYry1vf-Uu) |
| KIT-ML | Original [KIT-ML](https://motion-annotation.humanoids.kit.edu/dataset/) repo — [backup link](https://drive.google.com/drive/folders/1D3bf2G2o4Hv-Ale26YW18r1Wrh7oIAwK) |
| Motion-X | Original [Motion-X](https://github.com/IDEA-Research/Motion-X) repo — processing guide [HERE](./H-GPT/motionx_processing.md) |
| HumanML3D-X | Process via the [Motion-X](https://github.com/IDEA-Research/Motion-X) repo + [this guide](./H-GPT/motionx_processing.md). Uses original HumanML3D split with re-calculated mean/std. CoT data [on HuggingFace](https://huggingface.co/datasets/OpenMOSS-Team/FRoM-W1-Datasets/tree/main/data). |
| δHumanML3D-X | Same as HumanML3D-X, with perturbed instruction variants [on HuggingFace](https://huggingface.co/datasets/OpenMOSS-Team/FRoM-W1-Datasets/tree/main/data). |

Expected structure for each dataset:

```
H-GPT/datasets/{dataset_name}/data/
├── new_joint_vecs/
├── new_joints/
├── texts/
├── cots/
├── Mean.npy
├── Std.npy
├── all.txt
├── train.txt
├── train_val.txt
├── val.txt
└── test.txt
```

</details>

<details>
<summary><b>H-ACT Module</b> (click to expand)</summary>

| Dataset | Download Guide |
|:-------:|:-------------:|
| AMASS | Download and processing procedures from [human2humanoid](https://github.com/LeCAR-Lab/human2humanoid?tab=readme-ov-file#amass-dataset-preparation) |
| AMASS-H1 | Retargeted for Unitree H1 — [box link](https://cmu.app.box.com/s/vfi619ox7lwf2hzzi710p3g2l59aeczv) (from human2humanoid) |
| AMASS-G1 | Retargeted for Unitree G1 — link coming soon |

</details>

## 📏 Baselines

We retrained these SMPL-X baseline models and fully open-sourced them:

**SMPL-X Baseline Codebases** (forked repos):
- [T2M](https://github.com/humanoidintelligence/text-to-motion-smplx) · [MotionDiffuse](https://github.com/humanoidintelligence/motion-diffuse-smplx) · [MLD](https://github.com/humanoidintelligence/motion-latent-diffusion-smplx) · [T2M-GPT](https://github.com/humanoidintelligence/t2m-gpt-smplx)

**Checkpoints** ([HuggingFace](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/baselines)):
- Eval model · T2M · MotionDiffuse · MLD · T2M-GPT (all SMPL-X format)

## 🧠 Models

<details>
<summary><b>H-GPT</b> (click to expand)</summary>

| Model | Download |
|:-----:|:--------:|
| H-GPT w.o. CoT | [LoRA weights](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hgpt/humanml3d-x/lora/llama-3.1-nocot_maskinput_pkeep) — merge with [Llama-3.1](https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md) via [this script](https://huggingface.co/OpenMOSS-Team/FRoM-W1/blob/main/lora_merge.py) |
| H-GPT | [LoRA weights](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hgpt/humanml3d-x/lora/llama-3.1-cot_maskinput_pkeep) — merge with Llama-3.1 |
| H-GPT++ w.o. CoT | [LoRA weights](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hgpt/motionx/lora/llama-3.1-nocot) — merge with Llama-3.1 |
| H-GPT++ | [LoRA weights](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hgpt/motionx/lora/llama-3.1-cot) — merge with Llama-3.1 |

</details>

<details>
<summary><b>H-ACT</b> (click to expand)</summary>

| Policy | Download |
|:------:|:--------:|
| H1-Full | Teacher (TBD), [Student](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hact/h1/25_12_10_14-16-23_OmniH2O_STUDENT) |
| H1-Clean | Teacher (TBD), [Student](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hact/h1/25_12_10_14-13-33_OmniH2O_STUDENT_filter) |
| G1-Full | Teacher (TBD), [Student](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hact/g1/25_12_11_18-16-37_OmniH2O_STUDENT) |
| G1-Clean | Teacher (TBD), [Student](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hact/g1/25_12_11_18-18-10_OmniH2O_STUDENT_FILTER) |

</details>

## 🏗️ Repository Structure

```
FRoM-W1/
├── H-GPT/                         # Motion generation module
│   ├── hGPT/                      #  Core package (models, data, metrics, losses)
│   ├── configs/                   #  OmegaConf YAML configs (exp + arch)
│   ├── scripts/                   #  Inference entry points
│   └── motionx_processing.md      #  Dataset preparation guide
├── H-ACT/                         # Action execution module
│   ├── retarget/                  #  SMPL-X → robot joint retargeting (submodule)
│   ├── human2humanoid/            #  RL policy training framework (submodule)
│   └── RoboJuDo/                  #  Sim-to-real deployment (submodule)
├── assets/                        #  Images and media
├── QUICKSTART.md                  #  Step-by-step setup guide
├── requirements.txt
├── LICENSE                        #  Apache 2.0
└── README.md
```

## 🚀 Quick Start

The **[QUICKSTART.md](./QUICKSTART.md)** guide walks through the full pipeline:

```
Text Instruction → H-GPT (motion generation) → Retarget (SMPL-X → robot joints)
 → Policy (RL training) → RoboJuDo (sim-to-real deployment) → Real Robot
```

### Minimal inference

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

# 3. Visualize
python -m hGPT.data.motionx.visualization.plot_3d_global \
  --path ./results/<result_folder>

# 4. Retarget to robot joints (H-ACT)
cd ../H-ACT/retarget
python main.py
```

> For dataset preparation, model downloads, deps folder setup, and full deployment, follow **[QUICKSTART.md](./QUICKSTART.md)**.

## 🛠️ Model Training and Evaluation

### H-GPT

Three training stages controlled by the `TRAIN.STAGE` config field:

| Stage | `TRAIN.STAGE` | Description |
|-------|:-------------:|-------------|
| VQ-VAE | `"vae"` | Train whole-body motion tokenizer (convolutional encoder/decoder + vector quantization) |
| LM Pretrain | `"lm_pretrain"` | Finetune Llama-3.1-8B via LoRA to generate motion tokens (VQ-VAE frozen) |
| LM Instruct | `"lm_instruct"` | Instruction-tune with Chain-of-Thought data |

See the [H-GPT README](./H-GPT/README.md) for detailed training commands and evaluation protocols.

### H-ACT

- **[human2humanoid](https://github.com/LeCAR-Lab/human2humanoid)** — RL-based motion tracking (primary framework)
- **[Beyondmimic](https://beyondmimic.github.io/)** — CSV-formatted motion data required; convert with `retarget/scripts/pkl_2_csv.py`
- **[TWIST](https://github.com/YanjieZe/TWIST)** — Alternative tracking strategy
- **[RoboJuDo](https://github.com/humanoidintelligence/RoboJuDo)** — Unified sim-to-real deployment with pretrained policies

## 🙏 Acknowledgements

We thank Biao Jiang for discussions on motion generation models, and Tairan He and Ziwen Zhuang for their help in motion tracking. We are grateful to all the open-source datasets and projects that made this work possible.

## 📄 Citation

If you find this work useful, please star ⭐ the repo and cite:

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
