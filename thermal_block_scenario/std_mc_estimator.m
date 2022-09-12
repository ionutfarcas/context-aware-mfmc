function func_evals = std_mc_estimator(func, samples)

    N           = size(samples, 1);
    func_evals  = zeros(N, 1);

    parfor n=1:N
        func_evals(n) = func(samples(n, :));
    end
end

