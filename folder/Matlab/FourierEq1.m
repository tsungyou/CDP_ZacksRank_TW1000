clc;
close all;
clear all;


d = csvread("UNVR.JK.csv", 1, 1);
dataX = flipdim(d(:, 1:4), 1);
data1 = flipud(dataX);
close_1 = data1(:, 4);
Close = close_1(232:1232, :);
data_model = Close(1:700, :);
t = length(data_model);
time_model = (1:1:t)';
data_test = Close(701:1000, :);
tt = length(data_test);
timetest = [1:1:tt]';
%% cftool on command line 