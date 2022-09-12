function [ dROM ] = train_SVR_lo_fi_model( y, X, params )
%GENDATAMODEL Summary of this function goes here
%   Detailed explanation goes here

addpath(genpath('libsvm-3.20'));
kfold = 5;
cureps = params.eps;

%% normalize data
mumin = params.mumin;
mumax = params.mumax;
for i=1:size(X, 2)
    X(:, i) = (X(:, i) - mumin(i))./(mumax(i) - mumin(i));
end

%% cross validation?
if(isempty(params.cvparam))
    %% cross validation
    gList = logspace(1, -5, 30);
    eList = linspace(1, 5, 10);
    cverr = zeros(length(gList), length(eList));
    for gIter=1:length(gList)
        g = gList(gIter);
        disp([num2str(gIter/length(gList)*100), '%']);
        parfor eIter=1:length(eList)
%        for eIter=1:length(eList)
            e = eList(eIter);
            cverr(gIter, eIter) = 0;
            for curFold=1:kfold
                testIndx = mygetchunk(1:length(y), kfold, curFold);
                trainIndx = 1:length(y);
                trainIndx(testIndx) = [];
                svmmodel = libsvmtrain(y(trainIndx)', X(trainIndx, :), ['-s 3 -t 2 -q -p ', sprintf('%.15f', cureps), ' -g ', sprintf('%.15f', g), ' -c ', sprintf('%.15f', e)]);
                yr = libsvmpredict(y(testIndx)', X(testIndx, :), svmmodel, '-q');
                cverr(gIter, eIter) = norm(yr - y(testIndx)')/norm(y(testIndx)');
            end
            cverr(gIter, eIter) = cverr(gIter, eIter)/kfold;  
            disp(num2str(cverr(gIter, eIter)));
        end
    end
    [~, I] = min(cverr(:));
    g = gList(mod(I, length(gList))+1);
    e = eList(ceil(I/length(gList)));
    params.cvparam(1) = e;
    params.cvparam(2) = g;
end

%% build SVM
e = params.cvparam(1);
g = params.cvparam(2);
svmmodel = libsvmtrain(y', X, ['-s 3 -t 2 -p ', num2str(cureps), ' -g ', num2str(g), ' -c ', num2str(e)]);
dROM.svmmodel = svmmodel;
dROM.e = e;
dROM.g = g;
dROM.eps = cureps;
dROM.mumin = mumin;
dROM.mumax = mumax;
%dROM.F = @(y, curROM)libsvmpredict(zeros(size(y, 1), 1), y, curROM.svmmodel, '-q');

end

