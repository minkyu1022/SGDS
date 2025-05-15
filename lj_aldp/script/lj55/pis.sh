#!/bin/bash

GPU_DEVICE=$1  
SEED=$2        

if [ -z "$GPU_DEVICE" ] || [ -z "$SEED" ]; then
  echo "Usage: $0 <GPU_DEVICE> <SEED>"
  exit 1
fi

CUDA_VISIBLE_DEVICES=$GPU_DEVICE python src/train.py \
  --method pis \
  --date $(date +%Y-%m-%d_%H:%M:%S) \
  --project Neurips_lj55 \
  --energy lj55 \
  --mode_fwd pis \
  --lr_policy 0.0001 \
  --max_grad_norm 1.0 \
  --batch_size 2 \
  --clipping \
  --epochs 50000 \
  --seed $SEED \