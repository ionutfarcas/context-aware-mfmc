clear; close all; clc;

w1          = 0.1150;
budget      = [1e0, 5e0, 1e1, 3e1, 5e1, 8e1, 1e2, 3e2, 5e2];
budget_norm = ceil(budget/w1);
n_max_rb    = [2, 8, 50];

%% rates params
data              = load('RB_lo_fi_model_rate_params/acc_params.mat');
acc_params_rb     = data.acc_params;

data              = load('RB_lo_fi_model_rate_params/cost_params.mat');
cost_params_rb    = data.cost_params;

rates_rb.acc_params    = acc_params_rb;
rates_rb.cost_params   = cost_params_rb;

%% rates
acc_rate_rb    = @(n) exponential_acc_rate(acc_params_rb(1), acc_params_rb(2), acc_params_rb(3), n);
cost_rate_rb   = @(n) algebraic_cost_rate(cost_params_rb(1), cost_params_rb(2), n);

acc_rate_svm    = @(n) acc_params_svm(1).*n.^(-acc_params_svm(2));
cost_rate_svm   = @(n) algebraic_cost_rate(cost_params_svm(1), cost_params_svm(2), n);


%% only RB data
RB_data = load('mfmc_res_RB/RB_MFMC_measurements.mat');

hi_fi_s2    = RB_data.hi_fi_var;
rho_12_mfmc = RB_data.rho;
w2_mfmc     = RB_data.lo_fi_runtime;

mse_std_mc      = @(p, var, w) var * w/p;
mse_mfmc_rb     = @(p, var, w1, w2, rho_12) var/p * ( sqrt(w1*(1 - rho_12^2)) + ...
                                                  sqrt(w2*(rho_12^2)) ).^2;                                              
mse_amfmc_rb                = @(p, n, var, w2, rho_12) var/(p - n) * ( sqrt((1 - rho_12^2)) + ...
                                                  sqrt(w2*(rho_12^2)) ).^2;                  
                                                      
mse_std_mc_hi_fi                    = zeros(length(budget), 1);
mse_mfmc_rb_eval                    = zeros(length(budget), length(n_max_rb));
mse_amfmc_rb_eval                   = zeros(length(budget), 1);

n_star_rb       = zeros(length(budget), 1);
for i=1:length(budget)
    p       = budget(i);
    p_norm  = budget_norm(i);
    
    %% std MC
    mse_std_mc_hi_fi(i) = mse_std_mc(p, hi_fi_s2, w1);
    
    %% AMFMC RB
    [n_star_real, n_star_rb(i)] = find_n_star_rb(p_norm, rates_rb);
    
    rho_12  = sqrt(1 - acc_rate_rb(n_star_rb(i)));
    w2      = cost_rate_rb(n_star_rb(i));
       
    mse_amfmc_rb_eval(i)  = mse_amfmc_rb(p_norm, n_star_rb(i), hi_fi_s2, w2, rho_12); 


    %% MFMC RB
    for n=1:length(n_max_rb)
        w2          = RB_data.lo_fi_runtime(n);
        rho_12      = RB_data.rho(n);
        
        if p - (n_max_rb(n) + 1)*w1 > 0
            q = p - n_max_rb(n)*w1;
            mse_mfmc_rb_eval(i, n) = mse_mfmc_rb(q, hi_fi_s2, w1, w2, rho_12);
        end
    end

end
    
lw = 2;
ms = 4;
fs = 30;

figure();
loglog(budget, mse_std_mc_hi_fi, 'b--o', 'LineWidth', lw, 'MarkerSize', ms); hold on;
for n=1:length(n_max_rb)
    loglog(budget, mse_mfmc_rb_eval(:, n), '--s', 'LineWidth', lw, 'MarkerSize', ms); hold on;
end
loglog(budget, mse_amfmc_rb_eval, 'r--^', 'LineWidth', 1.5*lw , 'MarkerSize', ms + 2); hold on;
hold off;
grid on;


l = legend('std MC',...
             strcat('MFMC RB with N = ', num2str(n_max_rb(1))), ...
             strcat('MFMC RB with N = ', num2str(n_max_rb(2))), ...
             strcat('MFMC RB with N = ', num2str(n_max_rb(3))), ...
             'CA-MFMC RB');

xl = xlabel('budget q(sec)');
yl = ylabel('MSE estimate');

l.FontSize  = fs;
xl.FontSize = fs;
yl.FontSize = fs;

