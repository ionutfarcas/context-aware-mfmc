function [f, grad] = optimization_obj_rb(n, data)
c1      = data(1);
a       = data(2);
alpha   = data(3);
c2      = data(4);
beta    = data(5);
p       = data(6);

f       = ( c1*exp(-a*n^alpha) + c2*n^beta ) / (p - n);
grad    = ( -c1*a*alpha*n^(alpha)/n*exp(-a*n^alpha) + c2*n^beta*beta/n ) / (p-n) + ...
                        ( c1*exp(-a*n^alpha) + c2*n^beta ) / (p-n)^2; 

f       = f*p*100;
grad    = grad*p*100;

if(imag(f) > 0)
    f       = NaN;
    grad    = NaN;
end

end