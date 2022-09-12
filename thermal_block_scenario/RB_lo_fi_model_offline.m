function [model, reduced_data] = RB_lo_fi_model_offline(b1, b2, num_intervals_block, mu_range, n)

    params      = []; 
    params.B1   = b1;
    params.B2   = b2;
    
    params.numintervals_per_block = num_intervals_block;
    params.mu_range               = mu_range;
    
    model                         = thermalblock_model_struct(params);  
    model_data                    = gen_model_data(model);
    
    model.RB_train_size         = 1000;
    model.RB_stop_epsilon       = 1e-16;
    model.RB_stop_Nmax          = n;
    
    detailed_data   = gen_detailed_data(model, model_data);
    reduced_data    = gen_reduced_data(model, detailed_data);
end

