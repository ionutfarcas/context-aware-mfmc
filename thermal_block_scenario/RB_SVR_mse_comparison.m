clear; clc; close all

%% setup
w1          = 0.1150;
no_runs     = 50;
budget      = [1e0, 5e0, 1e1, 3e1, 5e1, 8e1, 1e2, 3e2, 5e2];
no_samples  = floor(budget/w1);
n_max       = [2, 8, 50];

%% ref results
data        = load('ref_res/ca_mfmc_ref_res.mat');
ref_means   = data.ca_mfmc_est;
ref_mean    = mean(ref_means);


%% standard MC 
data            = load('std_mc_res/std_mc_est.mat');
std_mc_mean     = data.std_mc_est;
mse_std_mc_calc      = zeros(length(no_samples), 1);

temp = zeros(no_runs, length(no_samples));
for s=1:length(no_samples)
    
    for n=1:no_runs
        temp(n, :) = (std_mc_mean(n, 1:length(no_samples)) - ref_mean).^2;
    end
    
    mse_std_mc_calc(s) = mean(temp(:, s));
end

%% MFMC
std_mfmc_mean       = zeros(no_runs, length(no_samples));
mse_mfmc_rb_calc    = zeros(length(no_samples), length(n_max));

data        = load('mfmc_res_RB/mfmc_est.mat');
mfmc_est    = data.mfmc_est;

for n=1:length(n_max)
    
    for s=1:length(no_samples)
        if budget(s) - w1*(n_max(n) + 1) > 0
            mse_mfmc_rb_calc(s, n) = mean((mfmc_est(:, n, s) - ref_mean).^2);
        end
    end
end

%% CA-MFMC RB
ca_rb_mfmc_mean         = zeros(no_runs, length(no_samples));
mse_ca_mfmc_rb_calc     = zeros(length(no_samples), 1);

data            = load('ca_mfmc_res_RB/ca_mfmc_est.mat');
ca_rb_mfmc_est  = data.ca_mfmc_est;

for s=1:length(no_samples)
    mse_ca_mfmc_rb_calc(s) = mean((ca_rb_mfmc_est(:, s) - ref_mean).^2);
end

%% CA-MFMC RB + SVR
ca_rb_svr_mfmc_mean         = zeros(no_runs, length(no_samples));
mse_ca_mfmc_rb_svr_calc     = zeros(length(no_samples), 1);

data                = load('ca_mfmc_res_RB_SVR/ca_mfmc_est.mat');
ca_rb_svr_mfmc_est  = data.ca_mfmc_est;

for s=2:length(no_samples)
    mse_ca_mfmc_rb_svr_calc(s) = mean((ca_rb_svr_mfmc_est(:, s) - ref_mean).^2);
end


save('/home/ionut/work/postdoc/code/context_aware_MFMC/plots_for_paper/thermal_block/results/MSE_TB_RB_computed.mat', ...
    'mse_std_mc_calc', 'mse_mfmc_rb_calc', 'mse_ca_mfmc_rb_calc', 'mse_ca_mfmc_rb_svr_calc')

%% plot part
lw1 = 2;
lw2 = 1.5;
ms1 = 5;
ms2 = 5;
fs  = 30;

fig1 = figure();

loglog(budget, mse_std_mc_calc, 'b-*', 'LineWidth', lw1, 'MarkerSize', ms2);
hold on;
loglog(budget, mse_mfmc_rb_calc(:, 1), 'g-o', 'LineWidth', lw1, 'MarkerSize', ms2);
hold on;
loglog(budget, mse_mfmc_rb_calc(:, 2), 'k-o', 'LineWidth', lw1, 'MarkerSize', ms2);
hold on;
loglog(budget, mse_mfmc_rb_calc(:, 3), 'm-o', 'LineWidth', lw1, 'MarkerSize', ms2);
hold on;
loglog(budget, mse_ca_mfmc_rb_calc, 'r-s', 'LineWidth', lw1, 'MarkerSize', ms2);
hold on;
loglog(budget, mse_ca_mfmc_rb_svr_calc, 'c-o', 'LineWidth', lw1, 'MarkerSize', ms2);

xl = xlabel('budget p (runtime [sec])');
yl = ylabel('estimated MSE');
xl.FontSize = fs; yl.FontSize = fs;
l1 = legend('standard MC ', ...
            strcat('MFMC RB with N= ', num2str(2)), ...
             strcat('MFMC RB with N= ', num2str(8)), ...
             strcat('MFMC RB with N= ', num2str(50)), ...
             'CA-MFMC RB', 'CA-MFMC RB + SVR');
set(l1, 'interpreter', 'latex')
t.FontSize = fs;
l1.FontSize = fs;
l1.Location='northeast';
grid on;
set(gca,'FontSize', 20);