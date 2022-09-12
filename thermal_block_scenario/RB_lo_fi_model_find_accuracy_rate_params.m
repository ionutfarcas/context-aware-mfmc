function acc_params = RB_lo_fi_model_find_accuracy_rate_params(acc_rate_eval, n_max_range_acc)

     
    %% compute accuracy rates' parameters
    acc_rate    = @(c)exponential_acc_rate(c(1), c(2), c(3), n_max_range_acc) - acc_rate_eval;
    % acc_rate    = @(c, data)exponential_approx_rate(c(1), c(2), c(3), data);
    acc_params0 = [1.0, 1.0, 1.0];
    options     = optimset('MaxIter', 1e6, 'MaxFunEvals', 1e6, 'TolFun', 1e-12);
    acc_params  = lsqnonlin(acc_rate, acc_params0, [], [], options);
%    acc_params  = lsqcurvefit(acc_rate, acc_params0, n_max_range_acc, acc_rate_eval);
end
