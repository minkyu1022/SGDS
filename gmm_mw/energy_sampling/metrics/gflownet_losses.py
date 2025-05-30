import torch
from torch.distributions import Normal


def fwd_tb(initial_state, gfn, log_reward_fn, exploration_std=None, return_exp = False):
    states, log_pfs, log_pbs, log_fs = gfn.get_trajectory_fwd(initial_state, exploration_std, log_reward_fn, count=True)
    with torch.no_grad():
        log_r = log_reward_fn(states[:, -1], count=True).detach()

    loss = 0.5 * ((log_pfs.sum(-1) + log_fs[:, 0] - log_pbs.sum(-1) - log_r) ** 2)
    if return_exp:
        return loss.mean(), states, log_pfs, log_pbs, log_r
    else:
        
        return loss.mean()


def bwd_tb(initial_state, initial_reward, gfn, log_reward_fn, exploration_std=None):
    states, log_pfs, log_pbs, log_fs = gfn.get_trajectory_bwd(initial_state, exploration_std, log_reward_fn, count=True)
    # with torch.no_grad():
    #     log_r = log_reward_fn(states[:, -1]).detach()
    
    with torch.no_grad():
        log_r = initial_reward.detach()

    loss = 0.5 * ((log_pfs.sum(-1) + log_fs[:, 0] - log_pbs.sum(-1) - log_r) ** 2)
    return loss.mean()


def fwd_tb_avg(initial_state, gfn, log_reward_fn, exploration_std=None, return_exp = False):
    states, log_pfs, log_pbs, _ = gfn.get_trajectory_fwd(initial_state, exploration_std, log_reward_fn, count=True)
    with torch.no_grad():
        log_r = log_reward_fn(states[:, -1], count=True).detach()

    log_Z = (log_r + log_pbs.sum(-1) - log_pfs.sum(-1)).mean(dim=0, keepdim=True)
    loss = log_Z + (log_pfs.sum(-1) - log_r - log_pbs.sum(-1))
    
    if return_exp:
        return 0.5 * (loss ** 2).mean(), states, log_pfs, log_pbs, log_r
    else:
        
        return 0.5 * (loss ** 2).mean()

def bwd_tb_avg(initial_state, initial_reward, gfn, log_reward_fn, exploration_std=None):
    states, log_pfs, log_pbs, _ = gfn.get_trajectory_bwd(initial_state, exploration_std, log_reward_fn, count=True)
    with torch.no_grad():
        log_r = initial_reward.detach()

    log_Z = (log_r + log_pbs.sum(-1) - log_pfs.sum(-1)).mean(dim=0, keepdim=True)
    loss = log_Z + (log_pfs.sum(-1) - log_r - log_pbs.sum(-1))
    return 0.5 * (loss ** 2).mean()


def db(initial_state, gfn, log_reward_fn, exploration_std=None, return_exp = False):
    states, log_pfs, log_pbs, log_fs = gfn.get_trajectory_fwd(initial_state, exploration_std, log_reward_fn, count=True)
    with torch.no_grad():
        log_fs[:, -1] = log_reward_fn(states[:, -1], count=True).detach()

    loss = 0.5 * ((log_pfs + log_fs[:, :-1] - log_pbs - log_fs[:, 1:]) ** 2).sum(-1)
    if return_exp:
        return loss.mean(), states, log_pfs, log_pbs, log_fs[:, -1]
    else:
        
        return loss.mean()


def subtb(initial_state, gfn, log_reward_fn, coef_matrix, exploration_std=None, return_exp = False):
    states, log_pfs, log_pbs, log_fs = gfn.get_trajectory_fwd(initial_state, exploration_std, log_reward_fn, count=True)
    with torch.no_grad():
        log_fs[:, -1] = log_reward_fn(states[:, -1], count=True).detach()

    diff_logp = log_pfs - log_pbs
    diff_logp_padded = torch.cat(
        (torch.zeros((diff_logp.shape[0], 1)).to(diff_logp),
         diff_logp.cumsum(dim=-1)),
        dim=1)
    A1 = diff_logp_padded.unsqueeze(1) - diff_logp_padded.unsqueeze(2)
    A2 = log_fs[:, :, None] - log_fs[:, None, :] + A1
    A2 = A2 ** 2
    if return_exp:
        return torch.stack([torch.triu(A2[i] * coef_matrix, diagonal=1).sum() for i in range(A2.shape[0])]).sum(), states, log_pfs, log_pbs, log_fs[:, -1]
    else:
        
        return torch.stack([torch.triu(A2[i] * coef_matrix, diagonal=1).sum() for i in range(A2.shape[0])]).sum()



def bwd_mle(samples, initial_reward, gfn, log_reward_fn, exploration_std=None):
    states, log_pfs, log_pbs, log_fs = gfn.get_trajectory_bwd(samples, exploration_std, log_reward_fn, count=True)
    loss = -log_pfs.sum(-1)
    return loss.mean()


def pis(initial_state, gfn, log_reward_fn, exploration_std=None, return_exp = False):
    states, log_pfs, log_pbs, log_fs = gfn.get_trajectory_fwd(initial_state, exploration_std, log_reward_fn, count=True, pis=True)
    with torch.enable_grad():
        log_r = log_reward_fn(states[:, -1], count=True)

    normalization_constant = float(1 / initial_state.shape[-1])
    loss = normalization_constant * (log_pfs.sum(-1) - log_pbs.sum(-1) - log_r)
    
    if return_exp:
        return loss.mean(), states, log_pfs, log_pbs, log_r
    else:
        return loss.mean()
    


def fwd_gafn(initial_state, rnd, gfn, log_reward_fn, exploration_std=None, return_exp = False):
    states, log_pfs, log_pbs, log_fs = gfn.get_trajectory_fwd(initial_state, exploration_std, log_reward_fn, count=True)
    with torch.no_grad():
        log_r = log_reward_fn(states[:, -1], count=True).detach()

    intrinsic_reward_sum = rnd_rewards(rnd, states)
    augmented_rewards = torch.logaddexp(log_r, intrinsic_reward_sum.log())
    
    loss = 0.5 * ((log_pfs.sum(-1) + log_fs[:, 0] - augmented_rewards - log_pbs.sum(-1)) ** 2)
    if return_exp:
        return loss.mean(), states, log_pfs, log_pbs, log_r
    else:
        
        return loss.mean()
    
def rnd_rewards(rnd_model, trajectory):
    # 기존: states, log_pfs, log_pbs, R(x)
    intrinsic_rewards = []
    for t in range(trajectory.shape[1] - 1):
        r_t = rnd_model.forward(trajectory[:,t])
        intrinsic_rewards.append(r_t)  # shape (B,)
    intrinsic_rewards = torch.stack(intrinsic_rewards, dim=1)  # (B, n)
    
    return intrinsic_rewards.sum(-1)