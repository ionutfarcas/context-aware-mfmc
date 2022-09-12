clc; clear; close all;

N = maxNumCompThreads(1);

%% PDE setup
b1                   = 3;
b2                   = 3;
num_intervals_block  = 20;
mu_left              = 1.;
mu_right             = 10.;
mu_range             = [mu_left; mu_right];
pde_params           = [b1, b2, num_intervals_block, mu_left, mu_right];

%% RB setup
n_max_range = [2, 8, 50];
no_runs     = 50;

rng(266789)
cost_rate_hi_fi_samples = random('Uniform', mu_left, mu_right, 1e3, b1*b2);

data                    = load('RB_lo_fi_model_rate_measurement_params/acc_rate_hi_fi_samples_new.mat');
acc_rate_hi_fi_samples  = data.acc_rate_hi_fi_samples;
data                    = load('RB_lo_fi_model_rate_measurement_params/acc_rate_hi_fi_evals_new.mat');
acc_rate_hi_fi_evals    = data.acc_rate_hi_fi_evals;

lo_fi_var       = zeros(length(n_max_range), 1);
rho             = zeros(length(n_max_range), 1);
lo_fi_runtime   = zeros(no_runs, length(n_max_range));
lo_fi_setup_rt  = zeros(length(n_max_range), 1);

for i=1:length(n_max_range)
    [hi_fi_var, lo_fi_var(i), rho(i)] = RB_corr_coeff(b1, b2, num_intervals_block, ...
                                   mu_range, n_max_range(i), acc_rate_hi_fi_samples, acc_rate_hi_fi_evals);
    
    tic;                          
    [reduced_model, reduced_data] = RB_lo_fi_model_offline(b1, b2, ...
                        num_intervals_block, mu_range, n_max_range(i));
    lo_fi_setup_rt(i) = toc;
    
    lo_fi = @(mu)RB_lo_fi_model(reduced_model, reduced_data, mu);
                    
    for n=1:no_runs
        no_samples  = size(cost_rate_hi_fi_samples, 1);
        
        local_runtime = zeros(no_samples, 1);
        for s=1:no_samples
            [lo_fi_eval, t]  = lo_fi(cost_rate_hi_fi_samples(s, :));
            local_runtime(s) = t;
        end
        
        lo_fi_runtime(n, i) = mean(local_runtime); 
    end
end

lo_fi_runtime = mean(lo_fi_runtime);

save('mfmc_res_RB/RB_MFMC_measurements_new.mat', 'hi_fi_var', 'lo_fi_var', 'rho', 'lo_fi_runtime', 'lo_fi_setup_rt');