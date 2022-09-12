function [m1, m2, est_mfmc] = mfmc(pde_params, n_max, p, rho, w, lo_fi_var, hi_fi_var)

    %% PDE setup
    b1                   = pde_params(1);
    b2                   = pde_params(2);
    num_intervals_block  = pde_params(3);
    mu_left              = pde_params(4);
    mu_right             = pde_params(5);
    mu_range             = [mu_left; mu_right];
    
    %% quantities for standard MFMC
    w1      = w(1);
    wn      = w(2);
    rho_n_2 = rho^2;
    
    r1      = 1.0;
    r2      = sqrt((w1*rho_n_2)/(wn*(1 - rho_n_2)));
    temp    = (p - n_max*w1)/(w1*r1 + wn*r2);
    m1      = floor(temp);
    if temp < 1
        m1 = ceil(temp);
    end
    m2      = floor(r2*temp);
    gamma   = sqrt(rho_n_2*hi_fi_var/lo_fi_var);
    
    
    
    
    if m1 >= 1
        
        % hi and lo fi models
        hi_fi                   = @(mu)hi_fi_model(b1, b2, num_intervals_block, mu_range, mu);
        [model, reduced_data]   = RB_lo_fi_model_offline(b1, b2, num_intervals_block, mu_range, n_max);
        lo_fi                   = @(mu)RB_lo_fi_model(model, reduced_data, mu);

        % get samples
        samples_m2 = random('Uniform', mu_left, mu_right, m2, b1*b2);
        samples_m1 = samples_m2(1:m1, :);

        % get the standard MC estimates
        evals_m1_hf = std_mc_estimator(@(mu)hi_fi(mu), samples_m1);
        est_m1_hf   = mean(evals_m1_hf);
        
        evals_m2_lf = std_mc_estimator(@(mu)lo_fi(mu), samples_m2);
        evals_m1_lf = evals_m2_lf(1:m1);
        
        est_m2_lf = mean(evals_m2_lf);
        est_m1_lf = mean(evals_m1_lf);

        % compute the MFMC estimator
        est_mfmc = est_m1_hf + gamma*(est_m2_lf - est_m1_lf);
    else
        m1 = 0;
        m2 = 0;
       
        est_mfmc = -1;
    end
end
