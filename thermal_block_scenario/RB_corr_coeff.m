function [hi_fi_var, lo_fi_var, rho] = RB_corr_coeff(b1, b2, num_intervals_block, ...
                                                    mu_range, n_max, samples, hi_fi_evals)
    
    [no_samples, temp]      = size(samples);
    [model, reduced_data]   = RB_lo_fi_model_offline(b1, b2, num_intervals_block, mu_range, n_max);
        
    lo_fi       = @(mu)RB_lo_fi_model(model, reduced_data, mu);
    lo_fi_evals = zeros(no_samples, 1);
    
    for i=1:no_samples
        [lo_fi_evals(i), t] = lo_fi(samples(i, :));
    end
    
    hi_fi_mean = mean(hi_fi_evals);
    lo_fi_mean = mean(lo_fi_evals);
    
    hi_fi_std = std(hi_fi_evals);
    lo_fi_std = std(lo_fi_evals);
    
    rho = 0;
    for i=1:no_samples
        rho = rho + (hi_fi_evals(i) - hi_fi_mean)*(lo_fi_evals(i) - lo_fi_mean); 
    end
    
    hi_fi_var   = hi_fi_std^2;
    lo_fi_var   = lo_fi_std^2;
    rho         = rho/((no_samples - 1)*hi_fi_std*lo_fi_std);
end