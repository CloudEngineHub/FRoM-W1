import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel


def load_pretrained(cfg, model, logger=None, phase="train"):
    if logger is not None:
        logger.info(f"Loading pretrain model from {cfg.TRAIN.PRETRAINED}")

    if phase == "train":
        ckpt_path = cfg.TRAIN.PRETRAINED
    elif phase == "test":
        ckpt_path = cfg.TEST.CHECKPOINTS
    elif phase == "demo":
        ckpt_path = cfg.DEMO.CHECKPOINTS

    state_dict = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    if "state_dict" in state_dict.keys():
        state_dict = state_dict["state_dict"]
    elif "module" in state_dict.keys():
        state_dict = state_dict["module"]
    else:
        raise NotImplementedError

    model.load_state_dict(state_dict, strict=True)
    return model


def load_pretrained_lora_and_merge(cfg, model, logger=None, phase="test"):
    if logger is not None:
        logger.info(f"Loading pretrained lora model from {cfg.TEST.CHECKPOINTS}")

    if phase == "train":
        ckpt_path = cfg.TRAIN.PRETRAINED
    elif phase == "test":
        ckpt_path = cfg.TEST.CHECKPOINTS  # lora checkpoints
        # assert cfg.TEST.BASE_MODEL_PATH != '', "Base model path should be provided for lora merge!"
        base_path = "deps/Meta-Llama-3.1-8B"
    elif phase == "demo":
        ckpt_path = cfg.DEMO.CHECKPOINTS
        # assert cfg.DEMO.BASE_MODEL_PATH != '', "Base model path should be provided for lora merge!"
        base_path = "deps/Meta-Llama-3.1-8B"
    base_model = AutoModelForCausalLM.from_pretrained(
        base_path,
        # torch_dtype=torch.bfloat16,
        # device_map="auto",
        # low_cpu_mem_usage=True,
    )
    tokenizer = AutoTokenizer.from_pretrained(ckpt_path, legacy=True)
    tokenizer.pad_token = tokenizer.eos_token
    base_model.resize_token_embeddings(len(tokenizer))
    # w0_before = base_model.model.embed_tokens.weight.data.clone()
    # print(w0_before.dtype)
    # base_model.resize_token_embeddings(len(model.lm.tokenizer))
    peft_model = PeftModel.from_pretrained(base_model, ckpt_path)
    # peft_model.resize_token_embeddings(len(tokenizer))
    merged_model = peft_model.merge_and_unload()
    model.lm.tokenizer = tokenizer
    model.lm.language_model = merged_model.cuda()
    # breakpoint()
    return model

    # state_dict = torch.load(ckpt_path, map_location="cpu",weights_only=False)
    # if 'state_dict' in state_dict.keys():
    #     state_dict = state_dict['state_dict']
    # elif 'module' in state_dict.keys():
    #     state_dict = state_dict['module']
    # else:
    #     raise NotImplementedError

    # model.load_state_dict(state_dict, strict=True)
    # return model


def load_pretrained_vae(cfg, model, logger=None):
    if logger is not None:
        logger.info(f"Loading pretrain vae from {cfg.TRAIN.PRETRAINED_VAE}")

    state_dict = torch.load(
        cfg.TRAIN.PRETRAINED_VAE, map_location="cpu", weights_only=False
    )["state_dict"]

    from collections import OrderedDict

    vae_dict = OrderedDict()
    for k, v in state_dict.items():
        if "motion_vae" in k:
            name = k.replace("motion_vae.", "")
            vae_dict[name] = v
        elif "vae" in k:
            name = k.replace("vae.", "")
            vae_dict[name] = v

    if hasattr(model, "vae"):
        model.vae.load_state_dict(vae_dict, strict=True)
    else:
        model.motion_vae.load_state_dict(vae_dict, strict=True)

    return model
