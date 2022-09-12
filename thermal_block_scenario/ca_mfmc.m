function [m1, m2, est_amfmc] = ca_mfmc(pde_params, p, acc_params, cost_params)

    %% PDE setup
    b1                   = pde_params(1);
    b2                   = pde_params(2);
    num_intervals_block  = pde_params(3);
    mu_left              = pde_params(4);
    mu_right             = pde_params(5);
    mu_range             = [mu_left; mu_right];

    %% rates constants
    c1          = acc_params(1);
    a           = acc_params(2);
    alpha       = acc_params(3);
    c2          = cost_params(1);
    beta        = cost_params(2);

    %% number of hi fi evals to find the lo fi model
    rates_rb.acc_params    = acc_params;
    rates_rb.cost_params   = cost_params;

    [n_star_real, n_star] = find_n_star_rb(p, rates_rb);
    
    if p - n_star > 1

        %% hi and lo fi models
        hi_fi                   = @(mu)hi_fi_model(b1, b2, num_intervals_block, mu_range, mu);
        [model, reduced_data]   = RB_lo_fi_model_offline(b1, b2, num_intervals_block, mu_range, n_star);
        lo_fi                   = @(mu)RB_lo_fi_model(model, reduced_data, mu);

        %% correlation coeff from A2
        rho_n_2 = 1 - c1*exp(-a*n_star^alpha);

        %% cost from A3
        w_n = c2*n_star^beta;

        %% quantities for standard MFMC
        r       = sqrt(rho_n_2/(w_n*(1 - rho_n_2)));
        m1      = floor((p - n_star)/(1 + w_n*r));
        m2      = floor(r*m1);
        gamma   = sqrt(rho_n_2);

        %% generate samples
        samples_m2 = random('Uniform', mu_left, mu_right, m2, b1*b2);
        samples_m1 = samples_m2(1:m1, :);

        % get the standard MC estimates
        hi_fi_evals     = std_mc_estimator(@(mu)hi_fi(mu), samples_m1);
        lo_fi_evals_m2  = std_mc_estimator(@(mu)lo_fi(mu), samples_m2);
        lo_fi_evals_m1  = lo_fi_evals_m2(1:m1);

        est_m1_hf = mean(hi_fi_evals);
        est_m2_lf = mean(lo_fi_evals_m2);
        est_m1_lf = mean(lo_fi_evals_m1);

        % compute the AMFMC estimator
        est_amfmc = est_m1_hf + gamma*(est_m2_lf - est_m1_lf);
    else
        m1 = 0;
        m2 = 0;
        est_amfmc = -1;
    end
end
