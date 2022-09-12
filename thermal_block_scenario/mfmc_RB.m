clc; clear; close all;

%% PDE setup
b1                   = 3;
b2                   = 3;
num_intervals_block  = 20;
mu_left              = 1.;
mu_right             = 10.;
mu_range             = [mu_left; mu_right];
pde_params           = [b1, b2, num_intervals_block, mu_left, mu_right];
n_max                = [2, 8, 50];

%% MC setup
no_runs     = 50;
w1          = 0.1150;
budget      = [1e0, 5e0, 1e1, 3e1, 5e1, 8e1, 1e2, 3e2, 5e2];

mfmc_est    = zeros(no_runs, length(n_max), length(budget));
m1          = zeros(no_runs, length(n_max), length(budget));
m2          = zeros(no_runs, length(n_max), length(budget));

MFMC_data = load('mfmc_res_RB/RB_MFMC_measurements.mat');


rho_rb         = MFMC_data.rho;
w2_rb          = MFMC_data.lo_fi_runtime;
lo_fi_var_rb   = MFMC_data.lo_fi_var;
hi_fi_var      = MFMC_data.hi_fi_var; 

rng(872178)
for r = 1:length(n_max)
    n_m         = n_max(r);
    w2          = w2_rb(r);
    rho         = rho_rb(r);
    lo_fi_var   = lo_fi_var_rb(r);
    
    w = [w1, w2];
    
    for i=1:length(budget)
        p = budget(i);
        
        for n = 1:no_runs
            [m1(n, r, i), m2(n, r, i), mfmc_est(n, r, i)]   = mfmc(pde_params, n_m, p, rho, w,...
                                                                       lo_fi_var, hi_fi_var);
        end
        
        save('mfmc_res_RB/mfmc_est.mat', 'm1', 'm2', 'mfmc_est');
    end
end

save('mfmc_res_RB/mfmc_est.mat', 'm1', 'm2', 'mfmc_est');