function activate_rbmatlab(system)
    wd = pwd;

    if strcmp(system, 'earhart')
        setenv('RBMATLABHOME','/oden/ionut/tools/rbmatlab_release_1_16_09');
        setenv('RBMATLABTEMP','/oden/ionut/tmp/matlab');
        addpath(getenv('RBMATLABHOME'));
        startup_rbmatlab
        
        cd(wd);
    elseif strcmp(system, 'laptop')
        setenv('RBMATLABHOME','/home/ionut/tools/rbmatlab_release_1_16_09');
        setenv('RBMATLABTEMP','/tmp/matlab');
        addpath(getenv('RBMATLABHOME'));
        startup_rbmatlab
        
        cd(wd);
    else
        disp('Wrong system!')
    end
end
