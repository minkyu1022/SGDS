#!/bin/bash

GPU_DEVICE=$1  
SEED=$2        

if [ -z "$GPU_DEVICE" ] || [ -z "$SEED" ]; then
  echo "Usage: $0 <GPU_DEVICE> <SEED>"
  exit 1
fi

CUDA_VISIBLE_DEVICES=$GPU_DEVICE python src/train.py \
  --method tb_expl_ls_lp \
  --date $(date +%Y-%m-%d_%H:%M:%S) \
  --project Neurips_aldp \
  --teacher mala \
  --energy aldp \
  --langevin \
  --local_search \
  --both_ways \
  --burn_in 500 \
  --max_iter_ls 1000 \
  --exploratory \
  --exploration_wd \
  --exploration_factor 0.1 \
  --ld_schedule \
  --clipping \
  --hidden_dim 128 \
  --batch_size 16 \
  --reuse \
  --epochs 5000 \
  --seed $SEED \