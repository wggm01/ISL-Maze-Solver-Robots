%Algoritmo para sacar mejor modelo de recta%
clc;
clear all;
close all;
%Importacion de data de prueba de archivo csv
filename='reg0-45.xlsx';
sheet=1;
thetaRange='A1:A41';
rRange='B1:B41';
theta=xlsread(filename,sheet,thetaRange);
rtheta=deg2rad(theta);
r=xlsread(filename,sheet,rRange);

