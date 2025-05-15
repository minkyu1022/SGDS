#!/bin/bash

GPU_DEVICE=$1  
SEED=$2        

if [ -z "$GPU_DEVICE" ] || [ -z "$SEED" ]; then
  echo "Usage: $0 <GPU_DEVICE> <SEED>"
  exit 1
fi

CUDA_VISIBLE_DEVICES=$GPU_DEVICE python src/train.py \
  --method subtb_lp \
  --date $(date +%Y-%m-%d_%H:%M:%S) \
  --project Neurips_aldp \
  --energy aldp \
  --mode_fwd subtb \
  --lr_flow 0.0005 \
  --langevin \
  --partial_energy \
  --conditional_flow_model \
  --clipping \
  --epochs 5000 \
  --hidden_dim 128 \
  --batch_size 16 \
  --seed $SEED \
