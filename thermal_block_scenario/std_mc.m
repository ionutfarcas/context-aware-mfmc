clc; clear; close all;

%% PDE setup
b1                   = 3;
b2                   = 3;
num_intervals_block  = 20;
mu_left              = 1;
mu_right             = 10.;
mu_range             = [mu_left; mu_right];
pde_params           = [b1, b2, num_intervals_block, mu_left];

%% MC setup
w1          = 0.1150; 
no_runs     = 50;
budget      = [1e0, 5e0, 1e1, 3e1, 5e1, 8e1, 1e2, 3e2, 5e2];
no_samples  = floor(budget/w1);

%% hi fi model evaluations
hi_fi = @(mu)hi_fi_model(b1, b2, num_intervals_block, mu_range, mu);

std_mc_est    = zeros(no_runs, length(budget));

rng(1821898);
for s=1:length(no_samples)
    
    for n=1:no_runs
        samples             = random('Uniform', mu_left, mu_right, no_samples(s), b1*b2);
        std_mc_est(n, s)    = mean(std_mc_estimator(@(mu)hi_fi(mu), samples));
    end
    
    save('std_mc_res/std_mc_est.mat', 'std_mc_est');
end

save('std_mc_res/std_mc_est.mat', 'std_mc_est');