#!/bin/bash

GPU_DEVICE=$1  
SEED=$2        

if [ -z "$GPU_DEVICE" ] || [ -z "$SEED" ]; then
  echo "Usage: $0 <GPU_DEVICE> <SEED>"
  exit 1
fi

CUDA_VISIBLE_DEVICES=$GPU_DEVICE python src/train.py \
  --method mle \
  --date $(date +%Y-%m-%d_%H:%M:%S) \
  --project Neurips_aldp \
  --data_dir data/aldp_1000K/md \
  --energy aldp \
  --bwd \
  --mode_bwd mle \
  --epochs 30000 \
  --clipping \
  --hidden_dim 128 \
  --batch_size 16 \
  --seed $SEED \
