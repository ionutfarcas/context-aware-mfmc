function lo_fi_rt = SVR_lo_fi_model_runtime(lo_fi_model, samples, w1)
    
    tic;
    lo_fi_approx = SVR_lo_fi_model_eval_multiple(lo_fi_model, samples);
    lo_fi_rt = toc;
    
    no_samples  = size(samples, 1);
    lo_fi_rt    = lo_fi_rt/no_samples;
    lo_fi_rt    = lo_fi_rt/w1;
end
