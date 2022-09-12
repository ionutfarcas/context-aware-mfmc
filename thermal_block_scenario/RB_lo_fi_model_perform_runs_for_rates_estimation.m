clc; clear; close all;

% N = maxNumCompThreads(1);


%% PDE setup
b1                   = 3;
b2                   = 3;
num_intervals_block  = 20;
mu_left              = 1.;
mu_right             = 10.;
mu_range             = [mu_left; mu_right];
pde_params           = [b1, b2, num_intervals_block, mu_left, mu_right];

%% RB setup
n_max_range_acc     = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 22, 25]';
n_max_range_cost    = linspace(15, 35, 21)';

%% MC setup
no_samples  = 1e5;
p           = 1e4;

w1 = 0.1150;

rng(266789)
acc_rate_hi_fi_samples = random('Uniform', mu_left, mu_right, no_samples, b1*b2);
save('RB_lo_fi_model_rate_measurement_params/acc_rate_hi_fi_samples.mat', 'acc_rate_hi_fi_samples');

acc_rate_hi_fi_evals = hi_fi_model_eval(b1, b2, num_intervals_block, mu_range, acc_rate_hi_fi_samples);
save('RB_lo_fi_model_rate_measurement_params/acc_rate_hi_fi_evals.mat', 'acc_rate_hi_fi_evals');

