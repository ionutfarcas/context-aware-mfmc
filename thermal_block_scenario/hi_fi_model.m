function hi_fi_approx = hi_fi_model(b1, b2, num_intervals_block, mu_range, mu)

    params      = []; 
    params.B1   = b1;
    params.B2   = b2;
    
    params.numintervals_per_block = num_intervals_block;
    params.mu_range               = mu_range;
    
    model        = thermalblock_model_struct(params);  
    model_data   = gen_model_data(model);
    
    model     = set_mu(model, mu);
    sim_data  = detailed_simulation(model, model_data);
    
    hi_fi_approx = sim_data.s;
end

