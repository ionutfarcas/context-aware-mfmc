clc; clear; close all;

N = maxNumCompThreads(64);

%% PDE setup
b1                   = 3;
b2                   = 3;
num_intervals_block  = 20;
mu_left              = 1.;
mu_right             = 10.;
mu_range             = [mu_left; mu_right];
pde_params           = [b1, b2, num_intervals_block, mu_left, mu_right];

dim     = 9;
eps     = 1e-2;
mumin   = 1.0*ones(dim, 1);
mumax   = 10.0*ones(dim ,1);

%% rates params
data             = load('RB_lo_fi_model_rate_params/acc_params.mat');
acc_params_rb    = data.acc_params;

data             = load('RB_lo_fi_model_rate_params/cost_params.mat');
cost_params_rb   = data.cost_params;

data             = load('SVR_lo_fi_model_rate_params/acc_params.mat');
acc_params_svr   = data.acc_params;

data             = load('SVR_lo_fi_model_rate_params/cost_params.mat');
cost_params_svr  = data.cost_params;


%% CA-MFMC setup
no_runs     = 50;
w1          = 0.1150;
budget      = [1e0, 5e0, 1e1, 3e1, 5e1, 8e1, 1e2, 3e2, 5e2];
p_norm      = floor(budget/w1);

ca_mfmc_est = zeros(no_runs, length(budget));
m1          = zeros(no_runs, length(budget));
m2          = zeros(no_runs, length(budget));
m3          = zeros(no_runs, length(budget));

for i=1:length(budget)
    p = p_norm(i);
    
    for n = 1:no_runs
        [m1(n, i), m2(n, i), m3(n, i), ca_mfmc_est(n, i)] = ...
        ca_mfmc_2D(pde_params, p, acc_params_rb, cost_params_rb, eps, acc_params_svr, cost_params_svr);
    end

    save('ca_mfmc_res_RB_SVR/ca_mfmc_est.mat', 'm1', 'm2', 'm3', 'ca_mfmc_est');
end

save('ca_mfmc_res_RB_SVR/ca_mfmc_est.mat', 'm1', 'm2', 'm3', 'ca_mfmc_est');