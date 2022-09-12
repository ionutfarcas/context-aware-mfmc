function acc_params = SVR_lo_fi_model_find_accuracy_rate_params(acc_rate_eval, no_samples_lo_fi)

    y_acc = log(acc_rate_eval);
    A_acc = zeros(length(acc_rate_eval), 2);

    A_acc(:, 1) = 1;
    A_acc(:, 2) = -log(no_samples_lo_fi);

    acc_rate_params = A_acc\y_acc;
    acc_params      = [exp(acc_rate_params(1)), acc_rate_params(2)];  
   
end
