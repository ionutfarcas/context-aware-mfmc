clc; clear; close all;

N = maxNumCompThreads(1);

%% PDE setup
b1                   = 3;
b2                   = 3;
num_intervals_block  = 20;
mu_left              = 1;
mu_right             = 10.;
mu_range             = [mu_left; mu_right];
pde_params           = [b1, b2, num_intervals_block, mu_left];

%% MC setup
no_runs     = 30;
no_samples  = 1e3;

 %% hi fi model evaluations
hi_fi_rt = zeros(no_runs, 1);

for n=1:no_runs
    samples = random('Uniform', mu_left, mu_right, no_samples, b1*b2);
    
    hi_fi_rt(n) = hi_fi_runtime(b1, b2, num_intervals_block, mu_range, samples);
end

save('hi_fi_model_measurements/hi_fi_runtime.mat', 'hi_fi_rt');
