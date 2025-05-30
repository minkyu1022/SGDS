python energy_sampling/train_with_RND.py \
  --method AIS+MLE \
  --round 1 \
  --teacher ais \
  --teacher_traj_len 10000 \
  --t_scale 1.0 \
  --energy many_well_128 \
  --pis_architectures \
  --zero_init \
  --clipping \
  --bwd \
  --mode_bwd mle \
  --lr_policy 5e-4 \
  --hidden_dim 256 \
  --s_emb_dim 256 \
  --t_emb_dim 256 \
  --first_epochs 50000 \
  --seed 12345 \