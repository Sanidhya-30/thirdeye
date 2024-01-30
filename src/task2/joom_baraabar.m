% Read the image
OGIm = imread('cat_lowres.jpg'); 
[r, c, cs] = size(OGIm);
ModIm = zeros(2 * r- 1, 2 * c- 1, cs);
ModIm(1:2:end, 1:2:end, :) = OGIm;

% Define wavelet and level
wavelet = 'db1';            % Daubechies wavelet 
level = 1; 

% Perform DWT
% [C, S] = wavedec2(OGIm, level, wavelet);
[a, h, v, d] = dwt2(OGIm,wavelet);

[rows, cols, channels] = size(a);

ca = zeros(2 * rows - 1, 2 * cols - 1, channels);
% ca(1:2:end, 1:2:end, :) = a;

ch = zeros(2 * rows - 1, 2 * cols - 1, channels);
% ch(1:2:end, 1:2:end, :) = h;

cv = zeros(2 * rows - 1, 2 * cols - 1, channels);
% cv(1:2:end, 1:2:end, :) = v;

cd = zeros(2 * rows - 1, 2 * cols - 1, channels);
% cd(1:2:end, 1:2:end, :) = d;

% Extract detail coefficients for level 1
% detCoeff = detcoef2(C, S, 1);

% [H1,V1,D1] = detcoef2('all',C,S,1);
% A1 = appcoef2(C,S,'haar',1);
% V1img = wcodemat(V1,255,'mat',1);
% H1img = wcodemat(H1,255,'mat',1);
% D1img = wcodemat(D1,255,'mat',1);
% A1img = wcodemat(A1,255,'mat',1);


% Perform IDWT
% reconstructedImage = waverec2(C, S, wavelet);
reconstructedImage = idwt2(ca, ch, cv, cd, wavelet);

% Display images
figure;
subplot(1,3,1);
imshow(OGIm);
title('Original Image');

% subplot(2,3,2);
% imshow(V1img);
% title('Vertical deets');
% 
% subplot(2,3,4);
% imshow(H1img);
% title('Horizontal deets');
% 
% subplot(2,3,5);
% imshow(D1img);
% title('Diagonal deets');

subplot(1,3,2);
imshow(uint8(ModIm));
title('Upscaled Image');

subplot(1,3,3);
imshow(uint8(reconstructedImage));
title('Reconstructed Image');