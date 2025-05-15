#!/bin/bash

GPU_DEVICE=$1  
MAX_ITER_LS=$2 
BURN_IN=$3 
BATCH_SIZE=$4 
SAVE_DIR=$5

CUDA_VISIBLE_DEVICES=$GPU_DEVICE python src/collect.py \
  --project lj55_mala \
  --energy lj55 \
  --teacher mala \
  --max_iter_ls $MAX_ITER_LS \
  --burn_in $BURN_IN \
  --teacher_batch_size $BATCH_SIZE \
  --save_dir $SAVE_DIR \
  --ld_schedule \