function cost_rate_eval = SVR_lo_fi_model_determine_cost_rate(pde_params, eps, no_samples_lo_fi, cost_samples, w1)
    
    b1                   = pde_params(1);
    b2                   = pde_params(2);
    num_intervals_block  = pde_params(3);
    mu_left              = pde_params(4);
    mu_right             = pde_params(5);
    mu_range             = [mu_left; mu_right];


    dim      = b1 * b2;
    mu_min   = mu_left*ones(dim, 1);
    mu_max   = mu_right*ones(dim ,1);
    
    no_runs = 50;
    
    cost_rate_eval   = zeros(no_runs, length(no_samples_lo_fi));

    for i=1:length(no_samples_lo_fi)
        n = no_samples_lo_fi(i);

        x = random('Uniform', mu_left, mu_right, n, dim);
        y = hi_fi_model_eval(b1, b2, num_intervals_block, mu_range, x)';

        lo_fi_model = SVR_lo_fi_model_offline(eps, mu_min, mu_max, x, y);
        
        for n=1:no_runs 
            cost_rate_eval(n, i) = SVR_lo_fi_model_runtime(lo_fi_model, cost_samples, w1);
        end
    end
end