function hi_fi_rt = hi_fi_runtime(b1, b2, num_intervals_block, mu_range, samples)
    
    [no_samples, temp] = size(samples); 
    
    hi_fi = @(mu)hi_fi_model(b1, b2, num_intervals_block, mu_range, mu);
   
    runtime = zeros(no_samples, 1);
    
    for i=1:no_samples
        tic;
        hi_fi_eval  = hi_fi(samples(i, :));
        runtime(i)  = toc; 
    end
        
    hi_fi_rt = mean(runtime);
end
