# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**FRoM-W1** (Foundational Humanoid Robot Model - Whole-Body Control, Version 1) is a two-stage open-source framework for generating humanoid whole-body motions from natural language instructions and executing them on real robots.

### Two-Stage Architecture

1. **H-GPT** (`./H-GPT/`) — Language-driven motion generation module
   - **Stage 1 — VQ-VAE (Whole-Body Motion Tokenizer)**: Encodes full-body motion sequences (623-dim features, SMPL-X format) into discrete tokens via a convolutional VQ-VAE with residual blocks. Supports multiple codebook sizes (512, 1K, 2K) and code dimensions.
   - **Stage 2 — LLM (Motion Generator)**: An autoregressive language model (Llama-3.1-8B, with optional T5/GPT-2 backends) fine-tuned via LoRA to generate motion tokens conditioned on text instructions. Uses Chain-of-Thought (CoT) prompting for better generalization. Motion tokens are interleaved with text in a template-based format.

2. **H-ACT** (`./H-ACT/`) — Action execution module
   - **Retargeting**: Converts H-GPT's 623-dim SMPL-X motion representations to robot joint sequences for Unitree H1, G1, Inspire Hand, and Dex3 Hand.
   - **Policy Training**: Builds on Human2Humanoid, Beyondmimic, and TWIST to train motion tracking policies.
   - **Sim-to-Real**: Deploys policies via **RoboJuDo** (git submodule) in simulation and on real robots.

## Key Dependencies

- **PyTorch Lightning** — training loop, checkpointing, logging
- **OmegaConf** — hierarchical YAML-based config system
- **Transformers (HuggingFace)** — LLM backbone (Llama-3.1-8B, T5, GPT-2)
- **PEFT (LoRA)** — parameter-efficient fine-tuning of LLM
- **SMPL-X / MANO / SMPL** — body models for motion representation and retargeting
- **Mujoco** — physics simulation (H-ACT / RoboJuDo side)

## Commands

### Setup
```bash
conda create -n fromw1 python=3.10
conda activate fromw1
pip install -r requirements.txt
```

### Inference (H-GPT Motion Generation)
```bash
cd H-GPT
CUDA_VISIBLE_DEVICES=0 python -m scripts.demo \
  --cfg_assets ./configs/assets.yaml \
  --cfg configs/exp/1217_config_motionx_stage2_body_hands_llama_vqvae2kx1k_cotv3_t2mx.yaml \
  --task t2m \
  --example ./scripts/instructions.txt
```

### Visualize Generated Motions
```bash
cd H-GPT
python -m hGPT.data.motionx.visualization.plot_3d_global \
  --path ./results/<result_folder>
```

### Motion Retargeting (H-ACT)
```bash
cd H-ACT/retarget
# Edit main.py lines 47-48 to select target robot (H1, G1, H121)
python main.py
# Convert output to CSV for Beyondmimic
python scripts/pkl_2_csv.py
```

### Deploy via RoboJuDo
```bash
cd RoboJuDo
python scripts/run_pipeline.py -c g1_h2h
```

## Config System

OmegaConf YAML files in `./H-GPT/configs/`:
- `assets.yaml` — global paths (checkpoint folder, arch folder)
- `exp/` — experiment-specific configs (dataset, model, training hyperparameters)
- `archs/vq/` — VQ-VAE architecture configs (codebook sizes, resolutions)
- `archs/lm/` — LM architecture configs (Llama/T5/GPT-2 variants, LoRA, mask/pkeep settings)

Configs are loaded hierarchically: `assets.yaml` → experiment config → architecture configs from `archs/`, merged via `OmegaConf.merge()`. The `--cfg_assets` and `--cfg` flags are always required.

## Key Code Structure (H-GPT)

| Path | Purpose |
|---|---|
| `hGPT/config.py` | Config loading, CLI argument parsing, instantiation from config |
| `hGPT/models/hgpt.py` | `HumanoidGPT` — main LightningModule orchestrating VQ-VAE + LLM |
| `hGPT/models/archs/hgpt_vq.py` | `VQVae` — convolutional encoder/decoder with vector quantization |
| `hGPT/models/archs/hgpt_lm.py` | `MLM` — motion-language model wrapper (tokenization, template filling, generation) |
| `hGPT/models/base.py` | `BaseModel` — LightningModule base with metrics, logging, checkpointing |
| `hGPT/data/motionx/dataset.py` | Motion-X dataset loading (623-dim/263-dim features) |
| `hGPT/data/build_data.py` | Dataset instantiation from config |
| `hGPT/losses/hgpt.py` | VQ-VAE losses (reconstruction, velocity, commit) + GPT LM loss |
| `hGPT/metrics/` | Evaluation metrics (T2M, M2M, multimodal, retrieval) |
| `scripts/demo.py` | Demo inference entry point |
| `motionx_processing.md` | Detailed Motion-X dataset processing guide |

## Training Stages

The `TRAIN.STAGE` config field controls which stage runs:
- `"vae"` — Train the VQ-VAE motion tokenizer (reconstruction + velocity + commit losses)
- `"lm_pretrain"` — Pretrain the LLM with motion tokens (freezes VQ-VAE)
- `"lm_instruct"` — Instruction-tune the LLM with CoT data

The `DATASET.TASK_PATH` field points to a JSON file defining task templates (input/output templates with placeholders like `<Caption_Placeholder>`, `<Motion_Placeholder>`, `<CoT_Placeholder>`, `<Frame_Placeholder>`).

## Datasets

- **HumanML3D-X**: HumanML3D + whole-body extensions from Motion-X (623-dim representations, SMPL-X format)
- **δHumanML3D-X**: Perturbed instruction variants for robustness evaluation
- **Motion-X**: Large-scale whole-body motion dataset (81K+ clips across 13 subsets)
- **AMASS / AMASS-H1 / AMASS-G1**: Retargeted robot motion data for policy training

All dataset files (.npy, .txt, symlinks) are placed under `datasets/` (gitignored). COT data and perturbed instructions are on HuggingFace.

## H-ACT / RoboJuDo

The `H-ACT/` directory at this level contains only the `retarget` submodule (motion reconstruction + retargeting) and `RoboJuDo` as a git submodule. Policy training and sim-to-real deployment are handled entirely within RoboJuDo, which supports pluggable tracking strategies (Beyondmimic, Human2Humanoid, TWIST).
