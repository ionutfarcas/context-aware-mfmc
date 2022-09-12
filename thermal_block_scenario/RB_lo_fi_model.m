function [lo_fi_approx, rb_time] = RB_lo_fi_model(model, reduced_data, mu)

    model = set_mu(model, mu);
    
    rb_sim_data     = rb_simulation(model, reduced_data);
    lo_fi_approx    = rb_sim_data.s; 
    solve_time      = rb_sim_data.solve_time;
    rhs_time        = rb_sim_data.rhs_time;
    rb_time         = solve_time + rhs_time;
    
end
