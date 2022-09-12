clc; clear; close all;

N = maxNumCompThreads(1);

w1 = 0.1150;

%% PDE setup
b1                   = 3;
b2                   = 3;
num_intervals_block  = 20;
mu_left              = 1.;
mu_right             = 10.;
mu_range             = [mu_left; mu_right];
pde_params           = [b1, b2, num_intervals_block, mu_left, mu_right];

eps = 1e-2;

%% setup
no_samples_lo_fi    = [100, 500, 1000, 2000, 3000, 5000, 6000, 7000, 8000, 10000, 12000, 15000, 18000, 20000];

no_samples_for_acc_rate  = 1e2;
no_samples_for_cost_rate = 1e3;

runs_already_done = 1;

cost_rate_samples = random('Uniform', mu_left, mu_right, no_samples_for_cost_rate, b1*b2);

%% perform simulations to use for estimating the rates
if runs_already_done == 1
 
    data             = load('SVR_lo_fi_model_rate_measurement_params/acc_rate_measurements.mat');
    acc_rate_eval    = data.acc_rate_eval;
    
    data       = load('SVR_lo_fi_model_rate_measurement_params/lo_fi_runtime_measurements.mat');
    lo_fi_rt   = data.lo_fi_rt;
    
else
    rng(266789);
    
    acc_rate_hi_fi_samples = random('Uniform', mu_left, mu_right, no_samples_for_acc_rate, b1*b2);
    save('SVR_lo_fi_model_rate_measurement_params/acc_rate_hi_fi_samples.mat', 'acc_rate_hi_fi_samples');

    acc_rate_hi_fi_evals = hi_fi_model_eval(b1, b2, num_intervals_block, mu_range, acc_rate_hi_fi_samples);
    save('SVR_lo_fi_model_rate_measurement_params/acc_rate_hi_fi_evals.mat', 'acc_rate_hi_fi_evals');
    
    acc_rate_eval = SVR_lo_fi_model_determine_accuracy_rate(pde_params, eps, no_samples_lo_fi, acc_rate_hi_fi_samples, acc_rate_hi_fi_evals);
    save('SVR_lo_fi_model_rate_measurement_params/acc_rate_measurements_new.mat', 'acc_rate_eval');
    
    lo_fi_rt = SVR_lo_fi_model_determine_cost_rate(pde_params, eps, no_samples_lo_fi, cost_rate_samples, w1);
    save('SVR_lo_fi_model_rate_measurement_params/lo_fi_runtime_measurements.mat', 'lo_fi_rt');
    
end


%% call high level functions to determine accuracy and cost rates
acc_params  = SVR_lo_fi_model_find_accuracy_rate_params(acc_rate_eval, no_samples_lo_fi);
cost_params = SVR_lo_fi_model_find_cost_rate_params(lo_fi_rt, no_samples_lo_fi);

save('SVR_lo_fi_model_rate_params/acc_params_new.mat', 'acc_params');
save('SVR_lo_fi_model_rate_params/cost_params.mat', 'cost_params');