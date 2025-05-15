#!/bin/bash

GPU_DEVICE=$1  
SEED=$2        

if [ -z "$GPU_DEVICE" ] || [ -z "$SEED" ]; then
  echo "Usage: $0 <GPU_DEVICE> <SEED>"
  exit 1
fi

CUDA_VISIBLE_DEVICES=$GPU_DEVICE python src/train.py \
  --method tb_ls \
  --date $(date +%Y-%m-%d_%H:%M:%S) \
  --project Neurips_lj55 \
  --teacher mala \
  --energy lj55 \
  --local_search \
  --both_ways \
  --epochs 10000 \
  --burn_in 2000 \
  --max_iter_ls 4000 \
  --max_grad_norm 1.0 \
  --ld_schedule \
  --batch_size 4 \
  --clipping \
  --reuse \
  --seed $SEED \
