clc
clear
close all

I=imread('cat.jpg');

I = rgb2gray(I);
% I = imresize(I, [2*r, 2*c]);% original image
[r, c, cs] = size(I);

M = zeros(2*r, 2*c, cs);
M(1:2:end, 1:2:end, 1) = I;

factor=1; % zooming factor
wname='db4'; % wavelet family

[a, h, v, d] = dwt2(I, wname);

temp = I;

h = imresize(h, size(temp));
v = imresize(v, size(temp));
d = imresize(d, size(temp));
M = imresize(M, size(temp));
z=zeros(size(temp));

    for i=1:factor
       temp=idwt2(temp,z,M,z,wname);
    end
O=uint8((2^factor)*temp);

subplot(1,2,1);
imshow(I);
title('OG Image', size(I));

subplot(1,2,2);
imshow(O);
title('Joomed Image');
