clear; close all; clc;

w1          = 0.1150;
budget      = [1e0, 5e0, 1e1, 3e1, 5e1, 8e1, 1e2, 3e2, 5e2, 8e2, 1e3];
budget_norm = ceil(budget/w1);

%% only RB data
RB_data = load('mfmc_res_RB/RB_MFMC_measurements.mat');

hi_fi_s2    = RB_data.hi_fi_var;

mse_std_mc          = @(p, var, w) var * w/p;                                                      
mse_std_mc_hi_fi    = zeros(length(budget), 1);

for i=1:length(budget)
    p       = budget(i);
    
    %% std MC
    mse_std_mc_hi_fi(i) = mse_std_mc(p, hi_fi_s2, w1);
    
end

data = load('numerically_estimated_mse/std_mc_mse.mat');
mse_std_mc_num = data.std_mc_mse;
    
lw = 2;
ms = 4;
fs = 30;

figure();
loglog(budget, mse_std_mc_hi_fi, 'b--o', 'LineWidth', lw, 'MarkerSize', ms); hold on;
loglog(budget, mse_std_mc_num, 'r--o', 'LineWidth', lw, 'MarkerSize', ms); hold on;
hold off;
grid on;


l = legend('std MC', 'std MC num');

xl = xlabel('budget q(sec)');
yl = ylabel('MSE estimate');

l.FontSize  = fs;
xl.FontSize = fs;
yl.FontSize = fs;

