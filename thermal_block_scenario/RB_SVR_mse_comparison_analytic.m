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

data              = load('SVR_lo_fi_model_rate_params/acc_params.mat');
acc_params_svr     = data.acc_params;

data              = load('SVR_lo_fi_model_rate_params/cost_params.mat');
cost_params_svr    = data.cost_params;

rates_rb.acc_params    = acc_params_rb;
rates_rb.cost_params   = cost_params_rb;

rates_svr.acc_params    = acc_params_svr;
rates_svr.cost_params   = cost_params_svr;

%% rates
acc_rate_rb    = @(n) exponential_acc_rate(acc_params_rb(1), acc_params_rb(2), acc_params_rb(3), n);
cost_rate_rb   = @(n) algebraic_cost_rate(cost_params_rb(1), cost_params_rb(2), n);

acc_rate_svr    = @(n) algebraic_acc_rate(acc_params_svr(1), acc_params_svr(2), n);
cost_rate_svr   = @(n) algebraic_cost_rate(cost_params_svr(1), cost_params_svr(2), n);


%% only RB data
RB_data = load('mfmc_res_RB/RB_MFMC_measurements.mat');

hi_fi_s2    = RB_data.hi_fi_var;
rho_12_mfmc = RB_data.rho;
w2_mfmc     = RB_data.lo_fi_runtime;

mse_std_mc      = @(p, var, w) var * w/p;
mse_mfmc_rb     = @(p, var, w1, w2, rho_12) var/p * ( sqrt(w1*(1 - rho_12^2)) + ...
                                                  sqrt(w2*(rho_12^2)) ).^2;                                              
mse_ca_mfmc_rb                = @(p, n, var, w2, rho_12) var/(p - n) * ( sqrt((1 - rho_12^2)) + ...
                                                  sqrt(w2*(rho_12^2)) ).^2; 
                                              
mse_ca_mfmc_rb_svr            = @(p, n1, n2, var, w2, w3, rho_12, rho_13) var/(p - n1 - n2) * ( sqrt((1 - rho_12^2)) + ...
                                                  sqrt(w2*(rho_12^2 - rho_13^2)) + sqrt(w3*(rho_13^2)) ).^2;    
                                                      
mse_std_mc_eval                       = zeros(length(budget), 1);
mse_mfmc_rb_eval                      = zeros(length(budget), length(n_max_rb));
mse_ca_mfmc_rb_eval                   = zeros(length(budget), 1);
mse_ca_mfmc_rb_svr_eval               = zeros(length(budget), 1);

n_star_rb       = zeros(length(budget), 1);
n_star_svr      = zeros(length(budget), 1);
for i=1:length(budget)
    p       = budget(i);
    p_norm  = budget_norm(i);
    
    %% std MC
    mse_std_mc_eval(i) = mse_std_mc(p, hi_fi_s2, w1);
    
  
    %% MFMC RB
    for n=1:3
        w2          = RB_data.lo_fi_runtime(n);
        rho_12      = RB_data.rho(n);

%         w2      = cost_rate_rb(n_max_rb(n))*w1;
%         rho_12  = sqrt(1 - acc_rate_rb(n_max_rb(n)));
        
        if p - (n_max_rb(n) + 1)*w1 > 0
            q = p - n_max_rb(n)*w1;
            mse_mfmc_rb_eval(i, n) = mse_mfmc_rb(q, hi_fi_s2, w1, w2, rho_12);
        end
    end
    
     %% CA-MFMC RB
    [n_star_real, n_star_rb(i)] = find_n_star_rb(p_norm, rates_rb);
    
    if p_norm - n_star_rb(i) > 1
    
        rho_12  = sqrt(1 - acc_rate_rb(n_star_rb(i)));
        w2      = cost_rate_rb(n_star_rb(i));

        mse_ca_mfmc_rb_eval(i)  = mse_ca_mfmc_rb(p_norm, n_star_rb(i), hi_fi_s2, w2, rho_12); 
    
    %% %% CA-MFMC RB + SVR
        acc_rb_model  = acc_rate_rb(n_star_rb(i));
        cost_rb_model = cost_rate_rb(n_star_rb(i));

        const_prev_model.acc    = acc_rb_model;
        const_prev_model.cost   = cost_rb_model;

        new_p = p_norm - n_star_rb(i);

        [n_star_real, n_star_svr(i)] = find_n_star_svr_after_rb(new_p, const_prev_model, rates_svr);
        
        if new_p - n_star_svr(i) > 1

            rho_13  = sqrt(1 - acc_rate_svr(n_star_svr(i)));
            w3      = cost_rate_svr(n_star_svr(i));

            mse_ca_mfmc_rb_svr_eval(i)  = mse_ca_mfmc_rb_svr(p_norm, n_star_rb(i), n_star_svr(i), ...
                hi_fi_s2, w2, w3, rho_12, rho_13); 
        end
    end

end

save('/home/ionut/work/postdoc/code/context_aware_MFMC/plots_for_paper/thermal_block/results/MSE_TB_RB_analytic.mat', ...
    'mse_std_mc_eval', 'mse_mfmc_rb_eval', 'mse_ca_mfmc_rb_eval', 'mse_ca_mfmc_rb_svr_eval') 
    
lw = 2;
ms = 4;
fs = 30;

figure();
loglog(budget, mse_std_mc_eval, 'b--o', 'LineWidth', lw, 'MarkerSize', ms); hold on;
for n=1:length(n_max_rb)
    loglog(budget, mse_mfmc_rb_eval(:, n), '--s', 'LineWidth', lw, 'MarkerSize', ms); hold on;
end
loglog(budget, mse_ca_mfmc_rb_eval, 'r--^', 'LineWidth', 1.5*lw , 'MarkerSize', ms + 2); hold on;
loglog(budget, mse_ca_mfmc_rb_svr_eval, 'm--o', 'LineWidth', 1.5*lw , 'MarkerSize', ms + 2); hold on;
hold off;
grid on;


l = legend('std MC',...
             strcat('MFMC RB with N = ', num2str(n_max_rb(1))), ...
             strcat('MFMC RB with N = ', num2str(n_max_rb(2))), ...
             strcat('MFMC RB with N = ', num2str(n_max_rb(3))), ...
             'CA-MFMC RB', ...
             'CA-MFMC RB + SVR');

xl = xlabel('budget q(sec)');
yl = ylabel('MSE estimate');

l.FontSize  = fs;
xl.FontSize = fs;
yl.FontSize = fs;

