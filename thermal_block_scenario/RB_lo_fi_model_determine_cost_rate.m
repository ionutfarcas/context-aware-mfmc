function lo_fi_rt = RB_lo_fi_model_determine_cost_rate(pde_params, n_max_range_cost, samples, w1)

   %% PDE setup
    b1                   = pde_params(1);
    b2                   = pde_params(2);
    num_intervals_block  = pde_params(3);
    mu_left              = pde_params(4);
    mu_right             = pde_params(5);
    mu_range             = [mu_left; mu_right];

    n_max_len_cost  = length(n_max_range_cost);
    no_runs         = 100;
    lo_fi_rt        = zeros(no_runs, n_max_len_cost);   
    
    for i=1:n_max_len_cost
        [reduced_model, reduced_data] = RB_lo_fi_model_offline(b1, b2, ...
                        num_intervals_block, mu_range, n_max_range_cost(i));
        
        for n=1:no_runs
            lo_fi_rt(n, i) = RB_lo_fi_runtime(reduced_model, reduced_data, samples, w1);
        end 
        
    end