function lo_fi_rt = RB_lo_fi_runtime(reduced_model, reduced_data, samples, w1)

    no_samples  = size(samples, 1);
    lo_fi       = @(mu)RB_lo_fi_model(reduced_model, reduced_data, mu);
 
    runtime = zeros(no_samples, 1);
    
    for i=1:no_samples
        [lo_fi_eval, t] = lo_fi(samples(i, :));
        runtime(i)      = t/w1;
    end
        
    lo_fi_rt = mean(runtime);
end
