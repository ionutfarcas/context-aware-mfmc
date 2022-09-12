function hi_fi_evals = hi_fi_model_eval(b1, b2, num_intervals_block, mu_range, mus)
       
    hi_fi_evals = zeros(size(mus, 1), 1);
    
    parfor i=1:size(mus, 1)
        hi_fi_evals(i) = hi_fi_model(b1, b2, num_intervals_block, mu_range, mus(i, :));
    end
    
end