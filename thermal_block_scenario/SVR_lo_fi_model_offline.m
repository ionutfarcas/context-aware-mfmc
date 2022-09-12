function rom_svm = SVR_lo_fi_model_offline(eps, mumin, mumax, x, y)
   
    params.eps      = eps;
    params.mumin    = mumin;
    params.mumax    = mumax;
    params.cvparam  = []; 
    
    rom_svm = train_SVR_lo_fi_model(y, x, params);
end

