# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**FRoM-W1** (Foundational Humanoid Robot Model - Whole-Body Control, Version 1) is a two-stage open-source framework for generating humanoid whole-body motions from natural language instructions and executing them on real robots.

### Two-Stage Architecture

1. **H-GPT** (`./H-GPT/`) — Language-driven motion generation module
   - **Stage 1 — VQ-VAE (Whole-Body Motion Tokenizer)**: Encodes full-body motion sequences (623-dim features, SMPL-X format) into discrete tokens via a convolutional VQ-VAE with residual blocks. Supports multiple codebook sizes (512, 1K, 2K) and code dimensions.
   - **Stage 2 — LLM (Motion Generator)**: An autoregressive language model (Llama-3.1-8B, with optional T5/GPT-2 backends) fine-tuned via LoRA to generate motion tokens conditioned on text instructions. Uses Chain-of-Thought (CoT) prompting for better generalization. Motion tokens are interleaved with text in a template-based format.

2. **H-ACT** (`./H-ACT/`) — Action execution module, composed of three git submodules:
   - **retarget** (HiRetarget): Converts H-GPT's 623-dim SMPL-X motion representations to robot joint sequences for Unitree H1, G1, Inspire Hand, and Dex3 Hand.
   - **human2humanoid**: Policy training framework (legged_gym + PHC + rsl_rl) for training motion tracking policies.
   - **RoboJuDo**: Sim-to-real deployment framework with pluggable tracking strategies (Beyondmimic, Human2Humanoid, TWIST, AMP, ASAP, KungFuBot).

## Key Dependencies

- **PyTorch Lightning** — training loop, checkpointing, logging
- **OmegaConf** — hierarchical YAML-based config system
- **Transformers (HuggingFace)** — LLM backbone (Llama-3.1-8B, T5, GPT-2)
- **PEFT (LoRA)** — parameter-efficient fine-tuning of LLM
- **SMPL-X / MANO / SMPL** — body models for motion representation and retargeting
- **Mujoco** — physics simulation (H-ACT / RoboJuDo side)

## Key Files at Root

| File | Purpose |
|---|---|
| `README.md` | Full project documentation (datasets, baselines, models, training) |
| `QUICKSTART.md` | Quick-start guide and pipeline overview |
| `requirements.txt` | Root pip dependencies shared with H-GPT |
| `LICENSE` | Apache License 2.0 |
| `assets/` | Images (FRoM-W1 overview, H-GPT, H-ACT diagrams, teaser) |

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
cd H-ACT/RoboJuDo
python scripts/run_pipeline.py -c g1_h2h
```

## Config System

OmegaConf YAML files in `./H-GPT/configs/`:

| Path | Purpose |
|---|---|
| `assets.yaml` | Global paths (CONFIG_FOLDER, ARCHS_FOLDER, FOLDER, TEST.FOLDER, DEMO settings) |
| `exp/` | Experiment-specific configs (~52 files: dataset, model, training hyperparameters) |
| `archs/vq/` | VQ-VAE architecture configs (codebook sizes: 512, 1K, 1K×2K, 2K×1K, 2K×2K) |
| `archs/lm/` | LM architecture configs (Llama, T5 variants; mask/pkeep/noise/rephrase settings) |
| `archs/eval/` | Evaluation model configs (`tm2t.yaml`, `tm2t_x.yaml`) |

Configs are loaded hierarchically: `assets.yaml` → experiment config → architecture configs from `archs/`, merged via `OmegaConf.merge()`. The `--cfg_assets` and `--cfg` flags are always required.

## Key Code Structure (H-GPT)

### Core framework

| Path | Purpose |
|---|---|
| `hGPT/config.py` | Config loading, CLI argument parsing, instantiation from config |
| `hGPT/logger.py` | Logging utilities |
| `hGPT/callback.py` | PyTorch Lightning callbacks |

### Data

| Path | Purpose |
|---|---|
| `hGPT/data/build_data.py` | Dataset instantiation from config |
| `hGPT/data/MotionX.py` | Alternative data module |
| `hGPT/data/default/` | Default dataset pipeline: dataset_t2m_{base,eval,token,train,vqvae}.py, word_vectorizer.py |
| `hGPT/data/motionx/dataset.py` | Motion-X dataset loading (623-dim/263-dim features) |
| `hGPT/data/motionx/common/` | Skeleton and quaternion utilities |
| `hGPT/data/motionx/scripts/` | Preprocessing scripts (motion_process.py, raw_pose_processing.py, cal_mean_variance.py) |
| `hGPT/data/motionx/smplx2smpl/` | SMPL-X to body-only conversion (joints, vectors, face) |
| `hGPT/data/motionx/visualization/` | Visualization tools (plot_3d_global, plot_feature_body, plot_feature_body_hands, plot_smplx) |

### Models

| Path | Purpose |
|---|---|
| `hGPT/models/hgpt.py` | `HumanoidGPT` — main LightningModule orchestrating VQ-VAE + LLM |
| `hGPT/models/base.py` | `BaseModel` — LightningModule base with metrics, logging, checkpointing |
| `hGPT/models/build_model.py` | Model factory instantiation from config |
| `hGPT/models/evaluator.py` | Evaluation model wrapper |
| `hGPT/models/archs/hgpt_vq.py` | `VQVae` — convolutional encoder/decoder with vector quantization |
| `hGPT/models/archs/hgpt_lm.py` | `MLM` — motion-language model wrapper (tokenization, template filling, generation) |

### Losses and Metrics

| Path | Purpose |
|---|---|
| `hGPT/losses/hgpt.py` | VQ-VAE losses (reconstruction, velocity, commit) + GPT LM loss |
| `hGPT/losses/base.py` | Base loss class |
| `hGPT/metrics/` | Evaluation metrics (t2m, m2m, m2t, mm, mr) and utils |
| `hGPT/metrics/base.py` | Base metric wrapper |

### Utilities

| Path | Purpose |
|---|---|
| `hGPT/utils/demo_utils.py` | Demo helper functions |
| `hGPT/utils/easyconvert.py` | SMPL-X parameter conversion |
| `hGPT/utils/sample_utils.py` | Motion sampling utilities |
| `hGPT/utils/load_checkpoint.py` | Checkpoint loading |
| `hGPT/utils/geometry_tools.py` / `geometry_conver.py` | Geometry computation |
| `hGPT/utils/temos_utils.py` | TeMoS (text-motion) utilities |

### Scripts

| Path | Purpose |
|---|---|
| `scripts/demo.py` | Demo inference entry point |
| `scripts/demo.sh` | Shell wrapper for demo.py |
| `scripts/instructions.txt` | Example text instructions for demo |
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

## H-ACT Submodules

The `H-ACT/` directory contains three git submodules:

| Submodule | Path | Purpose |
|---|---|---|
| HiRetarget | `H-ACT/retarget/` | Motion reconstruction + retargeting (body via gradient-fitting, hands via MANO) |
| human2humanoid | `H-ACT/human2humanoid/` | Policy training framework (legged_gym, PHC physics, rsl_rl reinforcement learning) |
| RoboJuDo | `H-ACT/RoboJuDo/` | Sim-to-real deployment (config-driven pipelines, controllers, policies, environments) |

- **retarget**: Body retargeting via `body_retarget/` (gradient-based fitting, robot configs for H1/G1/H121) and hand retargeting via `hand_retarget/` (MANO-based). Includes a pure-Python MANO model implementation in `mano/`. Output is converted via `scripts/pkl_2_csv.py`.
- **human2humanoid**: Contains `legged_gym/` (Isaac Gym environment setup), `phc/` (physics-based motion imitation), and `rsl_rl/` (RL algorithm implementations). Scripts for data processing (AMASS conversion, gradient fitting) and visualization.
- **RoboJuDo**: Config-driven pipeline system. Supports Mujoco simulation and real Unitree robot deployment. Pluggable controllers (motion_h2h, beyondmimic, twist, keyboard, joystick, unitree), environments (Mujoco, Unitree real, dummy), policies (AMO, ASAP, Beyondmimic, H2H Student, KungFuBot, Smooth, TWIST, Unitree), and tools (retargeting, kinematics, ZED odometry). Documented in `docs/`.

## H-GPT Directory Layout (Symlinks)

Three directories in `H-GPT/` are symlinks (gitignored targets):

| Symlink | Target |
|---|---|
| `H-GPT/datasets/` | Dataset files (.npy, .txt) |
| `H-GPT/deps/` | External dependencies |
| `H-GPT/experiments/` | Training outputs and checkpoints |
