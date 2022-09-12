function acc_rate_eval = RB_lo_fi_model_determine_accuracy_rate(pde_params, n_max_range_acc, samples, hi_fi_evals)

    %% PDE setup
    b1                   = pde_params(1);
    b2                   = pde_params(2);
    num_intervals_block  = pde_params(3);
    mu_left              = pde_params(4);
    mu_right             = pde_params(5);
    mu_range             = [mu_left; mu_right];

    %% RB setup
    n_max_len_acc   = length(n_max_range_acc);
    acc_rate_eval   = zeros(n_max_len_acc, 1);
    
    for i=1:n_max_len_acc
        [hi_fi_var, lo_fi_var, rho]    = RB_corr_coeff(b1, b2, num_intervals_block, ...
                                                                mu_range, n_max_range_acc(i), samples, hi_fi_evals);
                                                            
        acc_rate_eval(i)            = 1 - rho^2;
    end 
end
