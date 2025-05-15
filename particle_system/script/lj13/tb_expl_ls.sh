#!/bin/bash

GPU_DEVICE=$1  
SEED=$2        

if [ -z "$GPU_DEVICE" ] || [ -z "$SEED" ]; then
  echo "Usage: $0 <GPU_DEVICE> <SEED>"
  exit 1
fi

CUDA_VISIBLE_DEVICES=$GPU_DEVICE python src/train.py \
  --method tb_expl_ls \
  --date $(date +%Y-%m-%d_%H:%M:%S) \
  --project Neurips_lj13 \
  --teacher mala \
  --energy lj13 \
  --local_search \
  --both_ways \
  --burn_in 500 \
  --max_iter_ls 1000 \
  --exploratory \
  --exploration_wd \
  --exploration_factor 0.1 \
  --max_grad_norm 1.0 \
  --lr_policy 0.0002 \
  --ld_schedule \
  --clipping \
  --reuse \
  --epochs 10000 \
  --seed $SEED \