function [ chunk ] = mygetchunk( indx, numberOfChunks, chunkIndx )
%MYGETCHUNK Splits 'indx' into 'numberOfChunks' chunks and returns 'chunkIndx'
% In
%   indx            ...     index array that is split
%   numberOfChunks  ...     number of chunks
%   chunkIndx       ...     index of chunk that is return
% Out
%   chunk           ...     indices of chunk

N = length(indx);
assert(chunkIndx <= numberOfChunks);
chunkLength = ceil(N/numberOfChunks);
startA = (chunkIndx - 1)*chunkLength + 1;
endA = min(chunkIndx*chunkLength, N);

chunk = indx(startA:endA);


end

