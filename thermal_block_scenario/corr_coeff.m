function [hi_fi_var, lo_fi_var, rho] = corr_coeff(no_samples, lo_fi_evals, hi_fi_evals)
    
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