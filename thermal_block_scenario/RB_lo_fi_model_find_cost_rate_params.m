function cost_params = RB_lo_fi_model_find_cost_rate_params(lo_fi_rt, n_max_range_cost)

    lo_fi_rt = mean(lo_fi_rt);
  
    %% compute cost rates' parameters 
    y = log(lo_fi_rt)';
    A = zeros(length(lo_fi_rt), 2);

    A(:, 1) = 1;
    A(:, 2) = log(n_max_range_cost);

    cost_rate_params    = A\y;
    cost_params         = [exp(cost_rate_params(1)), cost_rate_params(2)];
    
end
