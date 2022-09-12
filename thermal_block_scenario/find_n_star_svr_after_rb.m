function [n_star_real, n_star_int] = find_n_star_svr_after_rb(p, const_prev_model, rates)
   
    obj_to_minimize = @(n)optimization_obj_svr_after_rb(n, [const_prev_model.acc, const_prev_model.cost,...
                            rates.acc_params(1), rates.acc_params(2), ...
                            rates.cost_params(1), rates.cost_params(2), p]);
    
    if(exist('optimoptions'))
        options = optimoptions('fmincon','Algorithm','trust-region-reflective', 'GradObj', 'on', ...
                    'StepTolerance', 1e-15, 'OptimalityTolerance', 1e-15, 'Display', 'off');
    else
        options = optimset('Algorithm','trust-region-reflective', 'GradObj', 'on', 'Display', 'off');
    end
   
    n_star_0 = 1;
    
    lb = 2;
    ub = p-1;
                
    [n_star_real, ~, ~, output] = fmincon(obj_to_minimize, n_star_0, [], [], [], [], lb, ub, [], options);
    
    n_star_int = ceil(n_star_real);
    
end

