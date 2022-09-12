function [ yr ] = evalDataModel( dROM, mu )
%EVALDATAMODEL Summary of this function goes here
%   Detailed explanation goes here

% normalize data
for i=1:size(mu, 2)
    mu(:, i) = (mu(:, i) - dROM.mumin(i))./(dROM.mumax(i) - dROM.mumin(i));
end
yr = libsvmpredict(mu(:, 1), mu, dROM.svmmodel, '-q');


end

