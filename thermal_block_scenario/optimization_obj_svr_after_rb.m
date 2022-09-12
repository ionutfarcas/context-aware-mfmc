function [f, grad] = optimization_obj_svr_after_rb(n, data)
    c_a_1   = data(1);
    c_c_1   = data(2);
    c1      = data(3);
    alpha   = data(4);
    c2      = data(5);
    beta    = data(6);
    p       = data(7);

    f       = ( c_a_1 + c_c_1*c1*n.^(-alpha) + c2*n.^(beta) )./ (p - n);
    grad    = ( -c_c_1*c1*n^(-alpha)*alpha/n+c2*n^beta*beta/n ) / (p-n) + ...
                        ( c_a_1 + c_c_1*c1*n.^(-alpha) + c2*n.^(beta) ) / (p-n)^2; 

    f       = f*p*500;
    grad    = grad*p*500;

    if(imag(f) > 0)
        f       = NaN;
        grad    = NaN;
    end
end