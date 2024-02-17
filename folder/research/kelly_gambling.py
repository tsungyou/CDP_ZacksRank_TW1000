import cvxpy as cv
import numpy as np

n = 20
k = 100

# makes np.random.rand(N) predictable
np.random.seed(0)

# monte carlo simulation
pi = np.random.uniform(size=k)
# normalization
pi /= np.sum(pi)

min_return = .7
max_return = 1.3

# matrix with shape (20, 100), which is the random generated return we'll use
# r[0] refers to return matrix for t=1, there's 20 objective and total t=100
r = np.random.uniform(low=min_return, high=max_return, size=(n,k))
for i in range(30):
  r[np.random.choice(range(n)), np.random.choice(range(k))] = 0.1
  r[np.random.choice(range(n)), np.random.choice(range(k))] = 2.5

# while based on assumption of kelly gambling,
# the last objective should be riskfree object(cash, with 0 return)
r[-1,:] = 1.0

# monte carlo sample
samples = 10000
t = 100

# again
np.random.seed(0)

mc_sample = r[:, np.random.choice(r.shape[1], size=samples*t, p=pi)]

# risk constraints
alpha = 0.7
beta = 0.1

def simulate_trajectories(sampled_returns, b):
  # log tracjectory
  # print(sampled_returns.shape, b.shape)
  N_SAMPLES, T, n = sampled_returns.shape
  # return np.hstack([np.zeros((N_SAMPLES, 1)), np.cumsum(np.log(np.dot(sampled_returns, b)), axis=1)])
  return np.cumsum(np.log(np.dot(sampled_returns, b)), axis=1)

def growth_rate_Wmins(logw_samples):
  # expected log return and minW
  T = logw_samples.shape[1] - 1
  print(np.min(logw_samples, axis=1))
  return np.mean(logw_samples[:,-1])/T, np.exp(np.min(logw_samples, axis=1))

def drawdown_prob(W_mins, alpha):
  return np.sum(W_mins < alpha)/float(len(W_mins)) 

b_RCKellyGambling = cv.Variable(n)
lambda_rck = cv.Parameter(pos=True)
growth_rate = pi.T*cv.log(r.T*b_RCKellyGambling)
risk_constraint = cv.log_sum_exp(np.log(pi) - lambda_rck*cv.log(r.T*b_RCKellyGambling)) <= 0
constraints = [cv.sum(b_RCKellyGambling) == 1, b_RCKellyGambling >= 0, risk_constraint]
probl_rck = cv.Problem(cv.Maximize(growth_rate), constraints)

print("========================================")
print("lambda | gr_MC | prob_th | prob_MC")

# 5.5: the lambda that leads to P aroubd alpha(.1)
# 0 : lambda = 0 => e^0 = 1 = beta => 不對portfolio低於0.7的機率設限
for lambda_rck.value in [0, np.log(beta)/np.log(alpha), 5.5]:
    print()
    probl_rck.solve()
    exp_growth_rate, W_mins = growth_rate_Wmins(simulate_trajectories(np.reshape(mc_sample.T, (samples, t, n)), np.asarray(b_RCKellyGambling.value)))
    print(f"{lambda_rck.value:.3f} | {exp_growth_rate:.3f} | {np.exp(lambda_rck.value * np.log(alpha)):.3f} | {drawdown_prob(W_mins, alpha):.3f} \\\\")
print("========================================")

print("lambda: selected lambda for RCK bet.")
print('gr_MC: growth based on monte carlo simulation.')
print("prob_th: drawdown probability according to lambda, the RCK bet with.")
print("prob_MC: probability that the loss of the portfolio at any moment exceeds predermined risk constraint(drawown).")
print(b_RCKellyGambling.value)

import matplotlib.pyplot as plt
N_TRAJ = 10
OFFSET = 2
lambda_star = 5.5

f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
ax1.semilogy(np.arange(t), [alpha]*t, 'r--', label = 'alpha')
ax2.semilogy(np.arange(t), [alpha]*t, 'r--', label = 'alpha')
ax1.set_xlabel("Kelly trajectories")
ax2.set_xlabel("RCK trajectories")
ax1.set_ylabel("wealth")
ax1.legend(loc='upper left')

for ax, lambda_rck.value in zip([ax1, ax2], [0., lambda_star]):
  probl_rck.solve()
  logw_samples = simulate_trajectories(np.reshape(mc_sample[:, OFFSET:OFFSET+N_TRAJ*t].T,
                                                  (N_TRAJ, t, n)),
                                        np.asarray(b_RCKellyGambling.value).ravel())
  print(f"trajectories with W_min < alpha: {sum(np.exp(np.min(logw_samples, axis=1)) < alpha)} of {N_TRAJ}")

  for i in range(N_TRAJ):
      wealth = np.exp(logw_samples[i,:])
      ax.semilogy(wealth, 'b')

OFFSET = 2
lambda_star = 5.5

f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
ax1.semilogy(np.arange(t), [alpha]*t, 'r--', label = 'alpha')
ax2.semilogy(np.arange(t), [alpha]*t, 'r--', label = 'alpha')
ax1.set_xlabel("Kelly trajectories")
ax2.set_xlabel("RCK trajectories")
ax1.set_ylabel("wealth")
ax1.legend(loc='upper left')

for ax, lambda_rck.value in zip([ax1, ax2], [0., lambda_star]):
  probl_rck.solve()
  logw_samples = simulate_trajectories(np.reshape(mc_sample[:, OFFSET:OFFSET+N_TRAJ*t].T, (N_TRAJ, t, n)), np.asarray(b_RCKellyGambling.value).ravel())
  print(f"trajectories with W_min < alpha: {sum(np.exp(np.min(logw_samples, axis=1)) < alpha)} of {N_TRAJ}")

for i in range(N_TRAJ):
  wealth = np.exp(logw_samples[i,:])
  ax.semilogy(wealth, 'b')