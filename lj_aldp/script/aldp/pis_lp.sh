#!/bin/bash

GPU_DEVICE=$1  
SEED=$2        

if [ -z "$GPU_DEVICE" ] || [ -z "$SEED" ]; then
  echo "Usage: $0 <GPU_DEVICE> <SEED>"
  exit 1
fi

CUDA_VISIBLE_DEVICES=$GPU_DEVICE python src/train.py \
  --method pis_lp \
  --date $(date +%Y-%m-%d_%H:%M:%S) \
  --project Neurips_aldp \
  --energy aldp \
  --mode_fwd pis \
  --langevin \
  --clipping \
  --hidden_dim 128 \
  --batch_size 8 \
  --epochs 5000 \
  --seed $SEED \