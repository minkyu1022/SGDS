#!/bin/bash

GPU_DEVICE=$1  
SEED=$2        

if [ -z "$GPU_DEVICE" ] || [ -z "$SEED" ]; then
  echo "Usage: $0 <GPU_DEVICE> <SEED>"
  exit 1
fi

CUDA_VISIBLE_DEVICES=$GPU_DEVICE python src/train.py \
  --method ours \
  --date $(date +%Y-%m-%d_%H:%M:%S) \
  --project Neurips_aldp \
  --data_dir data/aldp_400K/md \
  --energy aldp \
  --time_scheduler random \
  --epochs 10000 30000 \
  --mle_epoch 5000 \
  --rnd_weight 10 \
  --burn_in 10000 \
  --lr_policy 0.00002 \
  --lr_flow 0.00002 \
  --temperature 300 \
  --max_iter_ls 110000 \
  --teacher_batch_size 4 \
  --hidden_dim 128 \
  --batch_size 16 \
  --both_ways \
  --clipping \
  --seed $SEED \