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
std_mc_mse      = zeros(length(no_samples), 1);

temp = zeros(no_runs, length(no_samples));
for s=1:length(no_samples)
    
    for n=1:no_runs
        temp(n, :) = (std_mc_mean(n, 1:9) - ref_mean).^2;
    end
    
    std_mc_mse(s) = mean(temp(:, s));
end

%% MFMC
std_mfmc_mean  = zeros(no_runs, length(no_samples));
std_mfmc_mse   = zeros(3, length(no_samples));

data        = load('mfmc_res_RB/mfmc_est.mat');
mfmc_est    = data.mfmc_est;

for n=1:3
    
    for s=1:length(no_samples)
        if budget(s) - w1*(n_max(n) + 1) > 0
            std_mfmc_mse(n, s) = mean((mfmc_est(:, n, s) - ref_mean).^2);
        end
    end
end

%% AMFMC
ca_mfmc_mean  = zeros(no_runs, length(no_samples));
ca_mfmc_mse   = zeros(length(no_samples), 1);

data        = load('ca_mfmc_res_RB/ca_mfmc_est.mat');
ca_mfmc_est = data.ca_mfmc_est;

for s=1:length(no_samples)
    ca_mfmc_mse(s) = mean((ca_mfmc_est(:, s) - ref_mean).^2);
end

%% plot part
lw1 = 2;
lw2 = 1.5;
ms1 = 5;
ms2 = 5;
fs  = 30;

fig1 = figure();

loglog(budget, std_mc_mse, 'b-*', 'LineWidth', lw1, 'MarkerSize', ms2);
hold on;
loglog(budget, std_mfmc_mse(1, :), 'g-o', 'LineWidth', lw1, 'MarkerSize', ms2);
hold on;
loglog(budget, std_mfmc_mse(2, :), 'k-o', 'LineWidth', lw1, 'MarkerSize', ms2);
hold on;
loglog(budget, std_mfmc_mse(3, :), 'm-o', 'LineWidth', lw1, 'MarkerSize', ms2);
hold on;
loglog(budget, ca_mfmc_mse, 'r-s', 'LineWidth', lw1, 'MarkerSize', ms2);

xl = xlabel('budget p (runtime [sec])');
yl = ylabel('estimated MSE');
xl.FontSize = fs; yl.FontSize = fs;
l1 = legend('standard MC ', ...
            strcat('MFMC RB with N= ', num2str(2)), ...
             strcat('MFMC RB with N= ', num2str(8)), ...
             strcat('MFMC RB with N= ', num2str(50)), ...
             'AMFMC RB');
set(l1, 'interpreter', 'latex')
t.FontSize = fs;
l1.FontSize = fs;
l1.Location='northeast';
grid on;
set(gca,'FontSize', 20);