function [m1, m2, m3, est_ca_mfmc] = ca_mfmc_2D(pde_params, p, acc_params_rb, cost_params_rb, ...
                                                eps, acc_params_svr, cost_params_svr)

    %% PDE setup
    b1                   = pde_params(1);
    b2                   = pde_params(2);
    num_intervals_block  = pde_params(3);
    mu_left              = pde_params(4);
    mu_right             = pde_params(5);
    mu_range             = [mu_left; mu_right];

    dim     = b1*b2;
    mumin   = mu_left*ones(dim, 1);
    mumax   = mu_right*ones(dim ,1);

    %% rates constants
    c1_rb          = acc_params_rb(1);
    a_rb           = acc_params_rb(2);
    alpha_rb       = acc_params_rb(3);
    c2_rb          = cost_params_rb(1);
    beta_rb        = cost_params_rb(2);
    
    c1_svr         = acc_params_svr(1);
    alpha_svr      = acc_params_svr(2);
    c2_svr         = cost_params_svr(1);
    beta_svr       = cost_params_svr(2);

    rates_rb.acc_params    = acc_params_rb;
    rates_rb.cost_params   = cost_params_rb;

    [n_star_real_rb, n_star_rb] = find_n_star_rb(p, rates_rb);
    
     %% correlation coeff RB
    rho_1_2 = 1 - c1_rb*exp(-a_rb*n_star_rb^alpha_rb);

    %% cost RB
    w_1 = c2_rb*n_star_rb^beta_rb;

    const_prev_model.acc    = c1_rb*exp(-a_rb*n_star_rb^alpha_rb);
    const_prev_model.cost   = w_1;

    new_p = p - n_star_rb;

    rates_svr.acc_params    = acc_params_svr;
    rates_svr.cost_params   = cost_params_svr;

    [n_star_real_svr, n_star_svr] = find_n_star_svr_after_rb(new_p, const_prev_model, rates_svr);

    %% correlation coeff SVR
    rho_2_2 = 1 - c1_svr*n_star_svr^(-alpha_svr);

    %% cost SVR
    w_2 = c2_svr*n_star_svr^beta_svr;
    
    if p - n_star_rb -n_star_svr > 1

        % hi and lo fi models
        hi_fi                   = @(mu)hi_fi_model(b1, b2, num_intervals_block, mu_range, mu);
        
        [model, reduced_data]   = RB_lo_fi_model_offline(b1, b2, num_intervals_block, mu_range, n_star_rb);
        lo_fi_RB                = @(mu)RB_lo_fi_model(model, reduced_data, mu);

        x_train_SVR = random('Uniform', mu_left, mu_right, n_star_svr, b1*b2);
        y_train_SVR = zeros(1, n_star_svr);
        for i = 1:n_star_svr
            y_train_SVR(i) = hi_fi(x_train_SVR(i, :));
        end
        
        SVR_lo_fi_model = SVR_lo_fi_model_offline(eps, mumin, mumax, x_train_SVR, y_train_SVR);


        % quantities for standard MFMC
        r1      = sqrt((rho_1_2 - rho_2_2)/(w_1*(1 - rho_1_2)));
        r2      = sqrt(rho_2_2/(w_2*(1 - rho_1_2)));

        m1      = floor((p - n_star_rb - n_star_svr)/(1 + w_1*r1 + w_2*r2));
        m2      = floor(r1*m1);
        m3      = floor(r2*m1);
        
        gamma_1 = sqrt(rho_1_2);
        gamma_2 = sqrt(rho_2_2);


        % generate samples
        samples_m3 = random('Uniform', mu_left, mu_right, m3, b1*b2);
        samples_m2 = samples_m3(1:m2, :);
        samples_m1 = samples_m3(1:m1, :);

        % get the standard MC estimates
        hi_fi_evals     = std_mc_estimator(@(mu)hi_fi(mu), samples_m1);
        
        RB_lo_fi_evals_m2  = std_mc_estimator(@(mu)lo_fi_RB(mu), samples_m2);
        RB_lo_fi_evals_m1  = RB_lo_fi_evals_m2(1:m1);

        SVR_lo_fi_evals_m3 = SVR_lo_fi_model_eval_multiple(SVR_lo_fi_model, samples_m3);
        SVR_lo_fi_evals_m2 = SVR_lo_fi_evals_m3(1:m2);

        
        est_m1_hf = mean(hi_fi_evals);

        RB_est_m2_lf = mean(RB_lo_fi_evals_m2);
        RB_est_m1_lf = mean(RB_lo_fi_evals_m1);

        SVR_est_m3_lf = mean(SVR_lo_fi_evals_m3);
        SVR_est_m2_lf = mean(SVR_lo_fi_evals_m2);

        % compute the AMFMC estimator
        est_ca_mfmc = est_m1_hf + ...
                            gamma_1*(RB_est_m2_lf - RB_est_m1_lf) + ...
                            gamma_2*(SVR_est_m3_lf - SVR_est_m2_lf);
        
    else
        m1 = 0;
        m2 = 0;
        m3 = 0;
        est_ca_mfmc = -1;
    end
end
