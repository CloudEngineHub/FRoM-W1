<div align="center">
<h1> H-GPT</h1>
</div>

# Overview

The motion-language model **H-GPT** is the central generative module of FRoM-W1, designed to produce diverse and semantically accurate whole-body motions conditioned on natural language instructions. It operates in two sub-stages:

1. **Whole-Body Motion Tokenizer (VQ-VAE)** — A convolutional encoder/decoder with residual blocks and vector quantization that encodes full-body motion sequences (623-dim SMPL-X features) into discrete tokens. Supports multiple codebook sizes (512, 1K, 2K).

2. **Motion Generator (LLM)** — An autoregressive language model (Llama-3.1-8B, with optional T5/GPT-2 backends) fine-tuned via LoRA to generate motion tokens conditioned on text instructions. Supports Chain-of-Thought (CoT) prompting for improved generalization.

# Model Checkpoints

All pretrained weights are released on [HuggingFace 🤗](https://huggingface.co/OpenMOSS-Team/FRoM-W1).

### VQ-VAE Tokenizers

| Config | Codebook | Download |
|:------:|:--------:|:--------:|
| `config_motionx_stage1_body_hands_vqvae2kx1k` | 2048×1024 | [HuggingFace](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hgpt) |
| `config_motionx_stage1_body_hands_vqvae1kx1k` | 1024×1024 | [HuggingFace](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hgpt) |
| `config_motionx_stage1_body_hands_vqvae512x512` | 512×512 | [HuggingFace](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hgpt) |
| `config_t2mx_stage1_body_hands_vqvae512x512` | 512×512 (20fps) | [HuggingFace](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hgpt) |
| `1114_8gpu_config_t2mx_stage1_body_hands_vqvae512x512_30fps` | 512×512 (30fps) | [HuggingFace](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hgpt) |

### Motion Generators (LoRA weights)

| Model | Base Dataset | CoT | Download |
|:-----:|:------------:|:---:|:--------:|
| H-GPT w.o. CoT | HumanML3D-X | No | [LoRA](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hgpt/humanml3d-x/lora/llama-3.1-nocot_maskinput_pkeep) |
| H-GPT | HumanML3D-X | Yes | [LoRA](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hgpt/humanml3d-x/lora/llama-3.1-cot_maskinput_pkeep) |
| H-GPT++ w.o. CoT | Motion-X | No | [LoRA](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hgpt/motionx/lora/llama-3.1-nocot) |
| H-GPT++ | Motion-X | Yes | [LoRA](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/hgpt/motionx/lora/llama-3.1-cot) |

These are LoRA adapters for [Llama-3.1-8B](https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md). Use the [merge script](https://huggingface.co/OpenMOSS-Team/FRoM-W1/blob/main/lora_merge.py) to merge them with the base model.

# Training

## 🧩 Environment Setup

```bash
conda create -n hgpt python=3.10
conda activate hgpt
pip install -r requirements.txt
```

## 📁 Data Preparation

H-GPT supports two primary datasets: **Motion-X** (81K+ clips across 13 subsets) and **HumanML3D-X** (the HumanML3D benchmark with whole-body extensions). The `TRAIN.STAGE` config field determines which data is loaded — `"vae"` reads raw motion features from `MOTION_FEAT_PATH`, while `"lm_pretrain"` / `"lm_instruct"` reads pre-computed motion tokens from `MOTION_TOKEN_PATH`.

### Prerequisites: Dependencies

Before preparing any dataset, download the following and arrange them under `H-GPT/deps/`:

```
deps/
├── Meta-Llama-3.1-8B/           # [HuggingFace](https://huggingface.co/meta-llama/Llama-3.1-8B)
├── body_models/
│   ├── dmpls/                    # [SMPL DMPLs](https://smpl.is.tue.mpg.de/download.php)
│   ├── smplh/                    # [SMPL+H](https://mano.is.tue.mpg.de/download.php)
│   └── smplx/                    # [SMPL-X v1.1](https://smpl-x.is.tue.mpg.de/download.php)
├── glove_motionx/                # GloVe for Motion-X
│   ├── our_vab_data.npy
│   ├── our_vab_idx.pkl
│   └── our_vab_words.pkl
├── glove_t2m/                    # GloVe for HumanML3D-X
│   ├── our_vab_data.npy
│   ├── our_vab_idx.pkl
│   └── our_vab_words.pkl
└── t2m/                          # Eval models (from [HuggingFace](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/eval))
    ├── t2m/
    ├── t2mx/
    ├── t2mx-noise/
    ├── t2mx-rephrase/
    ├── kit/
    └── .../text_mot_match/
```

All data files go under `H-GPT/datasets/` (gitignored). See the **[QUICKSTART.md](../QUICKSTART.md)** for detailed guidance on constructing the deps folder.

### Dataset: Motion-X

> The full processing workflow is documented in **[motionx_processing.md](./motionx_processing.md)**. This is a tedious process — we recommend reading the original [Motion-X](https://github.com/IDEA-Research/Motion-X) paper, repo, and all known issues before starting.

**Step 1 — Download raw data:**
Follow the official [Motion-X download guide](https://github.com/IDEA-Research/Motion-X?tab=readme-ov-file#1-request-authorization) (authorization required). Apply updates per the News section up to `[2024.1.9]` (sequential text v1.1, frame-level descriptions).

**Step 2 — Process subsets:**
- Process non-mocap datasets per the [Motion-X non-mocap guide](https://github.com/IDEA-Research/Motion-X?tab=readme-ov-file#2-non-mocap-subsets)
- Process mocap datasets per the [Motion-X mocap guide](https://github.com/IDEA-Research/Motion-X?tab=readme-ov-file#3-mocap-subsets)
  - **EgoBody**: use numpy == 1.23.5
  - **GRAB**: don't rename files; stop after getting `grab/s1,s2,...` (skip `grab_process.py`); fix [issue-29](https://github.com/IDEA-Research/Motion-X/issues/29)
  - **AMASS**: rename subfolders per [instructions](https://github.com/IDEA-Research/Motion-X/tree/main/mocap-dataset-process#1-data-preparing); remove unused subsets (BMLhandball, GRAB, WEIZMANN); skip problematic motions from [issue-56](https://github.com/IDEA-Research/Motion-X/issues/56), [issue-43](https://github.com/IDEA-Research/Motion-X/issues/43); keep unaugmented face per [issue-97](https://github.com/IDEA-Research/Motion-X/issues/97)

Expected clip counts after processing (Motion-X 1.0): `humanml: 26292, HAA500: 5231, aist: 1470, GRAB: 1335, EgoBody: 980, idea400: 12513, fitness: 16730, dance: 163, animation: 329, game_motion: 10217, perform: 475, kungfu: 1040, music: 3565` (total **81,084**).

**Step 3 — Motion representation:**
Follow the [Motion-X representation pipeline](https://github.com/IDEA-Research/Motion-X/tree/main/tomato_represenation):

```bash
# 1. Raw pose processing → joints_322/
python raw_pose_processing.py

# 2. Motion representation → joints_623/ + vectors_623/
#    (skip the ~7 motions with shape (1,52,3) that can't be processed)
python motion_representation.py

# 3. Compute mean/variance for the 623-dim vectors
python cal_mean_var.py
#    (skip the ~10 .npy files that error out)
```

Scripts for step 3 are in `hGPT/data/motionx/scripts/`:
- `motion_process.py` — motion feature processing and `recover_from_ric()` helper
- `cal_mean_variance.py` — compute dataset-level mean and std
- `raw_pose_processing.py` — convert raw SMPL-X parameters to joint positions
- `smplx2smpl/` — helpers for SMPL-X to body-only conversion (`transfer_to_body_only_joints.py`, `transfer_to_body_only_vectors.py`, `smplx2joints.py`, `add_face_vectors.py`)

**Step 4 — Expected structure:**

```
datasets/motionx/
└── data/
    ├── motion_data/
    │   ├── vectors_623/          # 623-dim motion features (VQ-VAE training)
    │   ├── vectors_263/          # body-only 263-dim (optional)
    │   ├── joints_623/           # 623-dim joint positions
    │   ├── joints_322/           # 322-dim joints (from raw_pose_processing)
    │   └── joints_263/           # body-only joints (optional)
    ├── mean_std/
    │   └── vectors_623/Mean.npy  # computed by cal_mean_var.py
    │   └── vectors_623/Std.npy
    ├── texts/
    │   ├── semantic_labels/      # text annotations
    │   ├── body_texts/
    │   ├── hand_texts/
    │   ├── cot/                  # CoT annotations (v1/v2/v3)
    │   └── ...
    ├── split/                    # train/val/test/all splits
    │   ├── train.txt
    │   ├── val.txt
    │   └── test.txt
    ├── instructions/             # task templates for LM training
    │   ├── template_pretrain.json
    │   └── template_pretrain_cot.json
    └── TOKENS/                   # VQ-VAE tokenized motions (after Stage 1)
```

### Dataset: HumanML3D-X

HumanML3D-X is the whole-body extension of HumanML3D, built by combining the original HumanML3D data with the `humanml` subset from Motion-X. It uses the original HumanML3D train/dev/test split with re-calculated mean/std for 623-dim features.

**Preparation:**
1. Download the original [HumanML3D](https://github.com/EricGuo5513/HumanML3D) dataset
2. Process the Motion-X dataset (above) to get the `humanml` subset with 623-dim vectors
3. Create symlinks to combine both:

```
datasets/humanml3d-x/
└── data/
    ├── Mean.npy                  # re-calculated for HumanML3D-X
    ├── Std.npy
    ├── all.txt -> ../humanml3d/data/all.txt
    ├── train.txt -> ../humanml3d/data/train.txt
    ├── train_val.txt -> ../humanml3d/data/train_val.txt
    ├── val.txt -> ../humanml3d/data/val.txt
    ├── test.txt -> ../humanml3d/data/test.txt
    ├── texts -> ../humanml3d/data/texts
    ├── new_joint_vecs -> ../motionx/data/motion_data/vectors_623/humanml/
    ├── new_joints -> ../motionx/data/motion_data/joints_623/humanml/
    └── cot-v3/                   # CoT annotations from [HuggingFace](https://huggingface.co/datasets/OpenMOSS-Team/FRoM-W1-Datasets/tree/main/data)
```

### Dataset: δHumanML3D-X

A robustness evaluation benchmark with perturbed text instructions. After setting up HumanML3D-X, replace the text files with the perturbed variants from [HuggingFace](https://huggingface.co/datasets/OpenMOSS-Team/FRoM-W1-Datasets/tree/main/data).

### Motion Tokenization (for LM Training)

After training the VQ-VAE (Stage 1), tokenize the motion features for LM training. Tokens are stored as `.npy` files per clip under `MOTION_TOKEN_PATH`:

```
datasets/motionx/data/TOKENS/
├── EgoBody/*.npy
├── GRAB/*.npy
├── humanml/*.npy
└── ...
```

During inference/demo, pre-computed tokens are not needed — the VQ-VAE encoder runs live to tokenize features on the fly.

## 🚀 Train H-GPT

Training uses [PyTorch Lightning](https://lightning.ai/docs/pytorch/stable/) with OmegaConf YAML configs. The `TRAIN.STAGE` config field selects the component to train: `"vae"` trains the motion tokenizer, `"lm_pretrain"` trains the motion generator without CoT, and `"lm_instruct"` trains it with CoT.

### VQ-VAE Motion Tokenizer

Train the convolutional encoder/decoder with vector quantization to reconstruct whole-body motion features.

```bash
cd H-GPT

# Single-GPU (debug)
CUDA_VISIBLE_DEVICES=0 python -m scripts.demo \
  --cfg_assets ./configs/assets.yaml \
  --cfg configs/exp/config_motionx_stage1_body_hands_vqvae2kx1k.yaml \
  --task vae \
  --nodebug
```

> **Note**: For actual training, use PyTorch Lightning's `Trainer` directly. The `scripts/demo.py` with `--task vae` runs inference/validation on a trained VQ-VAE. Training is launched via a Lightning `Trainer` script (not included in this repo — follow the pattern below):

```python
# Example training launcher pattern:
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import ModelCheckpoint
from hGPT.config import parse_args
from hGPT.data.build_data import build_data
from hGPT.models.build_model import build_model

cfg = parse_args(phase="train")
cfg.TRAIN.STAGE = "vae"

datamodule = build_data(cfg)
model = build_model(cfg, datamodule)

trainer = Trainer(
    accelerator="gpu",
    devices=cfg.DEVICE,
    num_nodes=cfg.NUM_NODES,
    strategy="deepspeed_stage_2" if len(cfg.DEVICE) > 1 else "auto",
    precision="32",
    max_epochs=cfg.TRAIN.END_EPOCH,
    callbacks=[ModelCheckpoint(save_last=True)],
)
trainer.fit(model, datamodule=datamodule)
```

Key config options for VQ-VAE training:
- `configs/exp/config_motionx_stage1_body_hands_vqvae512x512.yaml` (512×512 codebook)
- `configs/exp/config_motionx_stage1_body_hands_vqvae2kx1k.yaml` (2048×1024 codebook)
- `configs/exp/config_motionx_stage1_body_hands_vqvae1kx1k.yaml` (1024×1024 codebook)
- `configs/exp/config_motionx_stage1_body_hands_vqvae1kx2k.yaml` (1024×2048 codebook)
- `configs/exp/config_humanml3d_stage1_body_vqvae512x512.yaml` (HumanML3D, body-only, 263-dim)
- `configs/exp/1113_8gpu_config_t2mx_stage1_body_hands_vqvae512x512.yaml` (HumanML3D-X, 20fps)
- `configs/exp/1114_8gpu_config_t2mx_stage1_body_hands_vqvae512x512_30fps.yaml` (HumanML3D-X, 30fps)

Losses configured in `hGPT/losses/hgpt.py`:
- **Reconstruction loss** (Smooth-L1 on 623-dim features) — weight `LAMBDA_FEATURE: 1.0`
- **Velocity loss** (Smooth-L1 on temporal velocity) — weight `LAMBDA_VELOCITY: 0.5`
- **Commit loss** (VQ codebook commitment) — weight `LAMBDA_COMMIT: 0.02`

Validated with `MRMetrics` (joint reconstruction error).

### Motion Generator (LM)

Finetune Llama-3.1-8B via LoRA to generate motion tokens (VQ-VAE frozen). The motion generator comes in two variants:

- **Without CoT** (`lm_pretrain`) — trains the LM to autoregressively predict motion tokens from text instructions directly.
- **With CoT** (`lm_instruct`) — instruction-tunes with Chain-of-Thought data for better generalization on unseen instructions.

Both variants share the same launcher; the task template (`TASK_PATH`) determines whether CoT annotations are included.

```bash
cd H-GPT

# Multi-GPU with DeepSpeed (8 GPUs)
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python -m scripts.demo \
  --cfg_assets ./configs/assets.yaml \
  --cfg configs/exp/1217_config_motionx_stage2_body_hands_llama_vqvae2kx1k_cotv3_t2mx.yaml \
  --task t2m \
  --nodebug
```

The difference between the two variants in config:

```yaml
# Without CoT:
TRAIN:
  STAGE: lm_pretrain
DATASET:
  TASK_PATH: 'datasets/motionx/data/instructions/template_pretrain.json'

# With CoT:
TRAIN:
  STAGE: lm_instruct
DATASET:
  TASK_PATH: 'datasets/motionx/data/instructions/template_pretrain_cot.json'
```

Key config options for LM training:
- `configs/exp/config_motionx_stage2_body_hands_llama_vqvae2kx1k.yaml` — Motion-X, Llama, no CoT
- `configs/exp/config_motionx_stage2_body_hands_llama_vqvae2kx1k_cotv3.yaml` — Motion-X, Llama, CoT v3
- `configs/exp/1217_config_motionx_stage2_body_hands_llama_vqvae2kx1k_cotv3_t2mx.yaml` — Motion-X→T2M-X transfer, CoT
- `configs/exp/1217_config_motionx_stage2_body_hands_llama_vqvae2kx1k_nocot_t2mx.yaml` — Motion-X→T2M-X transfer, no CoT
- `configs/exp/1113_8gpu_config_t2mx_stage2_body_hands_llama_vqvae512x512_nocot.yaml` — T2M-X, 20fps, no CoT
- `configs/exp/1113_8gpu_config_t2mx_stage2_body_hands_llama_vqvae512x512_cotv3.yaml` — T2M-X, 20fps, CoT
- `configs/exp/config_humanml3d_stage2_body_hands_vqvae512x512.yaml` — HumanML3D, no CoT
- `configs/exp/config_motionx_stage2_body_hands_t5_vqvae2kx1k_nocot.yaml` — Motion-X, T5 backbone

LM architecture variants (in `configs/archs/lm/`):
- `llama.yaml` — standard Llama-3.1-8B with LoRA
- `llama_maskinput.yaml` — with mask input strategy
- `llama_pkeep.yaml` — with pkeep (token keep probability)
- `llama_maskinput_pkeep.yaml` — combined masking
- `llama_cont.yaml` — with contrastive loss
- `t5.yaml` — T5 encoder-decoder backbone

The LM loss (`GPTLosses`) uses the LM's built-in cross-entropy (from HuggingFace `transformers`), weighted by `LAMBDA_CLS: 1.0`.

### Multi-GPU Training Tips

- Set `NUM_NODES`, `DEVICE`, and `STRATEGY` in the experiment config:
  - 1 GPU: `STRATEGY: 'auto'`, `DEVICE: [0]`
  - 8 GPUs: `STRATEGY: 'deepspeed_stage_2'`, `DEVICE: [0,1,2,3,4,5,6,7]`
- For VQ-VAE training with large batch sizes, set `BATCH_SIZE: 2048` and `ACCUMULATE_GRAD_BATCHES: 1`
- For LM training, use smaller per-GPU batch sizes with gradient accumulation: `BATCH_SIZE: 2`, `ACCUMULATE_GRAD_BATCHES: 8`
- The `PRECISION` field controls training precision: `'32'` (VQ-VAE), `'bf16-mixed'` (LM)
- Debug mode (`DEBUG: True`) limits data to 100 samples and forces single-GPU — override with `--nodebug`

# Evaluation

### Evaluate a Trained Model

Run evaluation using `scripts/demo.py` with `--task t2m` and the appropriate config and checkpoint:

```bash
cd H-GPT

# Evaluate with TM2TMetrics
CUDA_VISIBLE_DEVICES=0 python -m scripts.demo \
  --cfg_assets ./configs/assets.yaml \
  --cfg configs/exp/1217_config_motionx_stage2_body_hands_llama_vqvae2kx1k_cotv3_t2mx.yaml \
  --task t2m
```

Set `TEST.CHECKPOINTS` in the config to point to the trained checkpoint. Results (motion features, joints, text) are saved under `results/hgpt/<experiment_name>/samples_<timestamp>/`.

The config's `METRIC.TYPE` field controls which metrics are computed:

| Metric | Description | Used In |
|:------:|-------------|:-------:|
| `TM2TMetrics` | Text-to-motion: matching score, FID, diversity, top-k retrieval | LM stages |
| `MRMetrics` | Motion reconstruction: joint error | VQ-VAE stage |
| `MMMetrics` | Multi-modality: diversity across repeated samples | LM stages |
| `PredMetrics` | Prediction error metrics | VQ-VAE stage |
| `TemosMetric` | TeMoS embedding distance | (legacy) |

For retrieval-based metrics (`TM2TMetrics`), the evaluator requires the `deps/t2m/text_mot_match/` model files (from [HuggingFace](https://huggingface.co/OpenMOSS-Team/FRoM-W1/tree/main/eval)).

### Config Fields for Evaluation

- `TEST.SPLIT` — which split to evaluate (`'test'`, `'val'`)
- `TEST.BATCH_SIZE` — evaluation batch size
- `TEST.REPLICATION_TIMES` — number of repeated evaluations (for robustness)
- `TEST.SAVE_PREDICTIONS` — whether to save `.npy` outputs
- `METRIC.DIVERSITY_TIMES` — number of samples for diversity computation
- `METRIC.MM_NUM_SAMPLES` / `MM_NUM_REPEATS` / `MM_NUM_TIMES` — multi-modality evaluation parameters

# Inference / Demo

Run the demo to generate motions from text instructions:

```bash
cd H-GPT

CUDA_VISIBLE_DEVICES=0 python -m scripts.demo \
  --cfg_assets ./configs/assets.yaml \
  --cfg configs/exp/1217_config_motionx_stage2_body_hands_llama_vqvae2kx1k_cotv3_t2mx.yaml \
  --task t2m \
  --example ./scripts/instructions.txt
```

Input: one text instruction per line in `--example` file.
Output: `.npy` joint sequences saved to `results/hgpt/<experiment_name>/samples_<timestamp>/`.

Pre-configured demo commands are also in `scripts/demo.sh`.

### Visualize Generated Motions

```bash
cd H-GPT
python -m hGPT.data.motionx.visualization.plot_3d_global \
  --path ./results/<result_folder>
```

Additional visualization scripts in `hGPT/data/motionx/visualization/`:
- `plot_feature_body.py` — plot body-only motion features
- `plot_feature_body_hands.py` — plot body + hand features
- `plot_smplx.py` — render SMPL-X mesh overlay

# Deployment (Gradio App)

Deploy H-GPT as a Gradio web application:

```bash
cd H-GPT

# 1. Set up deployment environment
conda create -n hgpt_deploy python=3.10
conda activate hgpt_deploy
pip install -r requirements_deploy.txt

# 2. Download the VQ-VAE tokenizer and motion generator from HuggingFace
#    and set their paths in hGPT/configs/config_deployment_cot.yaml (lines 55, 78)

# 3. Launch the app
sh app.sh
```

This starts a Gradio interface for interactive text-to-motion generation.

# Code Structure

```
H-GPT/
├── hGPT/                              # Core Python package
│   ├── config.py                      # Config loading, CLI parsing, instantiation
│   ├── logger.py                      # Logging utilities
│   ├── callback.py                    # PyTorch Lightning callbacks
│   ├── data/
│   │   ├── build_data.py              # Dataset instantiation from config
│   │   ├── MotionX.py                 # MotionXDataModule (main data module)
│   │   ├── base.py                    # BASEDataModule + collate
│   │   ├── default/                   # Dataset classes:
│   │   │   ├── dataset_t2m_vqvae.py   #   MotionDatasetVQVAE (VQ-VAE training)
│   │   │   ├── dataset_t2m_train.py   #   Text2MotionDatasetTrain (LM training)
│   │   │   ├── dataset_t2m_eval.py    #   Text2MotionDatasetEval (evaluation)
│   │   │   ├── dataset_t2m_token.py   #   Text2MotionDatasetToken (token I/O)
│   │   │   ├── dataset_t2m_base.py    #   Base dataset with text/motion loading
│   │   │   └── word_vectorizer.py     #   GloVe-based word embedding
│   │   └── motionx/                   # Motion-X specific code
│   │       ├── dataset.py             # Raw motion feature dataset (V2)
│   │       ├── common/                # Skeleton + quaternion utilities
│   │       ├── scripts/               # Preprocessing scripts
│   │       ├── smplx2smpl/            # SMPL-X to body-only conversion
│   │       └── visualization/         # Motion visualization
│   ├── models/
│   │   ├── hgpt.py                    # HumanoidGPT (main LightningModule)
│   │   ├── base.py                    # BaseModel (optimizer, metrics, logging)
│   │   ├── build_model.py             # Model factory
│   │   ├── evaluator.py               # Evaluation networks
│   │   └── archs/
│   │       ├── hgpt_vq.py             # VQVae (encoder/decoder + quantization)
│   │       ├── hgpt_lm.py             # MLM (motion-language model wrapper)
│   │       └── utils/                 # ResNet, quantizer, token embedding
│   ├── losses/
│   │   ├── hgpt.py                    # GPTLosses (VQ-VAE + LM losses)
│   │   └── base.py                    # Base loss class
│   ├── metrics/                       # Evaluation metrics
│   │   ├── t2m.py                     # TM2TMetrics (matching, FID, diversity)
│   │   ├── m2m.py / m2t.py / mm.py   # Other metric variants
│   │   └── mr.py                      # MRMetrics (reconstruction)
│   └── utils/                         # Utilities (demo_utils, geometry, checkpoint, sample)
├── configs/
│   ├── assets.yaml                    # Global paths
│   ├── exp/                           # 50+ experiment configs
│   └── archs/                         # Model architecture configs (vq, lm, eval)
├── scripts/
│   ├── demo.py                        # Inference/demo entry point
│   ├── demo.sh                        # Pre-configured demo commands
│   └── instructions.txt               # Example text instructions
├── motionx_processing.md              # Motion-X dataset processing guide
└── datasets/ -> ...                   # Dataset files (symlink, gitignored)
```
