#!/bin/bash

GPU_DEVICE=$1  
SEED=$2        
LR=$3

if [ -z "$GPU_DEVICE" ] || [ -z "$SEED" ]; then
  echo "Usage: $0 <GPU_DEVICE> <SEED>"
  exit 1
fi

CUDA_VISIBLE_DEVICES=$GPU_DEVICE python src/train.py \
  --date $(date +%Y-%m-%d_%H:%M:%S) \
  --project Neurips_lj55 \
  --data_dir data/lj55_3K/mala \
  --energy lj55 \
  --teacher mala \
  --time_scheduler random \
  --rnd_weight 1 \
  --max_grad_norm 1.0 \
  --ld_schedule \
  --mle_epoch 5000 \
  --lr_policy 0.00002 \
  --lr_flow 0.00002 \
  --burn_in 4000 \
  --max_iter_ls 10000 \
  --teacher_batch_size 1 \
  --batch_size 4 \
  --epochs 10000 30000 \
  --both_ways \
  --clipping \
  --seed $SEED \