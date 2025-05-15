#!/bin/bash

GPU_DEVICE=$1  
MAX_ITER_LS=$2 
BURN_IN=$3
BATCH_SIZE=$4 
SAVE_DIR=$5

CUDA_VISIBLE_DEVICES=$GPU_DEVICE python src/collect.py \
  --project aldp_md \
  --energy aldp \
  --teacher md \
  --ld_step 5e-4 \
  --burn_in $BURN_IN \
  --max_iter_ls $MAX_ITER_LS \
  --teacher_batch_size $BATCH_SIZE \
  --save_dir $SAVE_DIR \