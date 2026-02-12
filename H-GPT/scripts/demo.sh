python -m demo --cfg_assets ./configs/assets.yaml --cfg configs/exp/config_motionx_stage2_body_hands_llama_vqvae2kx1k_cotv3.yaml --task t2m --example scripts/demos/t2m.txt
# nocot
CUDA_VISIBLE_DEVICES=0 python -m demo --cfg_assets ./configs/assets.yaml --cfg configs/exp/1202_8gpu_config_t2mx_stage2_body_hands_llama_vqvae512x512_nocot_30fps_feat5.yaml --task t2m --example scripts/demos/cot_eval.txt
# cotv3
CUDA_VISIBLE_DEVICES=1 python -m demo --cfg_assets ./configs/assets.yaml --cfg configs/exp/1202_8gpu_config_t2mx_stage2_body_hands_llama_vqvae512x512_cotv3_30fps_feat5.yaml --task t2m --example scripts/demos/cot_eval.txt
# motionx nocot
CUDA_VISIBLE_DEVICES=0 python -m demo --cfg_assets ./configs/assets.yaml --cfg configs/exp/1217_config_motionx_stage2_body_hands_llama_vqvae2kx1k_nocot_t2mx.yaml --task t2m --example scripts/demos/cot_eval.txt
# motionx cotv3
CUDA_VISIBLE_DEVICES=1 python -m demo --cfg_assets ./configs/assets.yaml --cfg configs/exp/1217_config_motionx_stage2_body_hands_llama_vqvae2kx1k_cotv3_t2mx.yaml --task t2m --example scripts/demos/cot_eval.txt
