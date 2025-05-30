import os
import wandb
import argparse

from utils import *
from teachers import *
from energies import *
from plot_utils import *
from metrics.evaluations import *
from metrics.gflownet_losses import *

parser = argparse.ArgumentParser()

# System config
parser.add_argument('--seed', type=int, default=0)
parser.add_argument('--save_dir', type=str, default='')
parser.add_argument('--date', type=str, default='test')
parser.add_argument('--device', type=str, default='cuda')
parser.add_argument('--method', type=str, default='ours')
parser.add_argument('--project', type=str, default='aldp')

# Dataset config
parser.add_argument('--data_dir', type=str, default='')
parser.add_argument('--teacher', type=str, default='md', choices=('md', 'mala'))
parser.add_argument('--energy', type=str, default='aldp', choices=('aldp', 'pypv', 'lj13', 'lj55'))

## MD config
parser.add_argument("--gamma", default=1.0, type=float)
parser.add_argument('--n_steps', type=int, default=200000)
parser.add_argument('--eval_size', type=int, default=10000)
parser.add_argument("--timestep", default=5e-4, type=float)
parser.add_argument("--temperature", default=600, type=float)
parser.add_argument('--teacher_batch_size', type=int, default=1000)

# MALA config
parser.add_argument('--burn_in', type=int, default=15000)
parser.add_argument('--rnd_weight', type=float, default=0)
parser.add_argument('--prior_std', type=float, default=1.75)
parser.add_argument('--ld_step', type=float, default=0.00001)
parser.add_argument('--max_iter_ls', type=int, default=20000)
parser.add_argument('--ld_schedule', action='store_true', default=False)
parser.add_argument('--target_acceptance_rate', type=float, default=0.574)

args = parser.parse_args()

set_seed(args.seed)

def get_energy():
    if args.energy == 'aldp':
        energy = ALDP(args)
    elif args.energy == 'pypv':
        energy = PYPV(args)
    elif args.energy == 'lj13':
        energy = LJ13(args)
    elif args.energy == 'lj55':
        energy = LJ55(args)
    return energy

def get_teacher():
    if args.teacher == 'md':
        teacher = MD(args, energy)
    elif args.teacher == 'mala':
        teacher = MALA(args, energy)
    return teacher

def eval(energy, samples):
    samples = samples[:args.eval_size].to(args.device)
    gt_samples = energy.sample(args.eval_size).to(args.device)
    energies = energy.energy(samples).detach().cpu().numpy()
    gt_energies = energy.energy(gt_samples).detach().cpu().numpy()
    interatomic_distances = energy.interatomic_distance(samples).reshape(-1).detach().cpu().numpy()
    gt_interatomic_distances = energy.interatomic_distance(gt_samples).reshape(-1).detach().cpu().numpy()

    energy_dict = {
        'Student': energies,
        'GT': gt_energies,
    }
    dist_dict = {
        'Student': interatomic_distances,
        'GT': gt_interatomic_distances
    }
    if args.energy in ['aldp', 'pypv']:        
        gt_phi_psi_fig = plot_phi_psi(gt_samples.reshape(gt_samples.shape[0], -1, 3))
        phi_psi_fig = plot_phi_psi(samples.reshape(samples.shape[0], -1, 3))
        wandb.log({"GT Phi Psi": wandb.Image(gt_phi_psi_fig)})
        wandb.log({"Teacher Phi Psi": wandb.Image(phi_psi_fig)})

    energy_hist_fig = plot_energy_hist(energy_dict)
    dist_fig = make_interatomic_dist_fig(dist_dict)
    wandb.log({"Energy Hist": wandb.Image(energy_hist_fig)})
    wandb.log({"Interatomic Distances": wandb.Image(dist_fig)})

if __name__ == '__main__':    
    name = f'data/{args.save_dir}/{args.teacher}'
    os.makedirs(name, exist_ok=True)

    wandb.init(project=args.project, config=vars(args))
    wandb.run.log_code(".")

    energy = get_energy()
    teacher = get_teacher()
    
    global_epochs = 0

    if args.teacher=='mala':
        prior = Gaussian(args.device, energy.data_ndim, std=args.prior_std)
        initial_positions = prior.sample(args.teacher_batch_size).to(args.device)
    elif args.teacher=='md':
        initial_positions = energy.initial_position
        initial_positions = initial_positions.repeat(args.teacher_batch_size, 1).to(args.device)
    samples, rewards = teacher.sample(initial_positions)

    np.save(f'{name}/positions.npy', samples.detach().cpu().numpy())
    np.save(f'{name}/rewards.npy', rewards.detach().cpu().numpy())
    
    eval(energy, samples)