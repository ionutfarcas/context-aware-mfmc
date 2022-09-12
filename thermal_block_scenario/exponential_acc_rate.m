function approx_rate = exponential_acc_rate(c, a, alpha, n)

    approx_rate = c.*exp(-a.*n.^alpha); 
end

