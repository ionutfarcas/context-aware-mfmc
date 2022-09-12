function acc_rate_eval = SVR_lo_fi_model_determine_accuracy_rate(pde_params, eps, no_samples_lo_fi, hi_fi_samples, hi_fi_evals)
    
    b1                   = pde_params(1);
    b2                   = pde_params(2);
    num_intervals_block  = pde_params(3);
    mu_left              = pde_params(4);
    mu_right             = pde_params(5);
    mu_range             = [mu_left; mu_right];


    dim      = b1 * b2;
    mu_min   = mu_left*ones(dim, 1);
    mu_max   = mu_right*ones(dim ,1);
    
    acc_rate_eval   = zeros(length(no_samples_lo_fi), 1);

    for i=1:length(no_samples_lo_fi)
        n = no_samples_lo_fi(i);

        x = random('Uniform', mu_left, mu_right, n, dim);
        y = hi_fi_model_eval(b1, b2, num_intervals_block, mu_range, x)';

        lo_fi_model = SVR_lo_fi_model_offline(eps, mu_min, mu_max, x, y);
        lo_fi_evals = SVR_lo_fi_model_eval_multiple(lo_fi_model, hi_fi_samples);

        no_samples_hi_fi = length(hi_fi_samples);

        [hi_fi_var, lo_fi_var, rho] = corr_coeff(no_samples_hi_fi, lo_fi_evals, hi_fi_evals);
        acc_rate_eval(i)            = 1 - rho^2;
    end
end