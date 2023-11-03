%% Code for Flood Frequency Analysis portion of the CEE450 Class Project Fall 2011
%
%%This code takes daily streamflow data and computes 3 flood frequency curves using 3 distributions
%%Using what you have learned in class, choose the one that best fits your particular catchment.
%
%%Modified by Mary Yaeger from code created by Mary Yaeger and Evan Coopersmith for
%%CEE598 Hydrologic Variability, Fall 2010: HW3 and Class Project
%%
clear all
close all

%% INSERT NAME OF YOUR MOPEX DATA FILE, WITHOUT THE FILE EXTENSION
%**Example: for data file KS304s.csv -> FileName = 'KS304';

FileName = 'KS304';

%% LOAD THE MOPEX DATA
%The readme.txt file tells you how the data file is structured
Data = importdata([FileName, '.csv']);

%Parse the time data into columns
Year  = Data(:,1);
Month = Data(:,2);
Day   = Data(:,3);

%Extract the streamflow data
Q = Data(:,6);

%Get the number of calendar years
numYears = length(unique(Year));

%% FIND THE PEAK DAILY FLOW FOR EACH YEAR AND MONTH IN WHICH IT OCCCURED
%Create a vector of all the years in the data file
years = unique(Year);

%Create storage vectors for Qp and QpMonth
Qp = zeros(length(years), 1);
QpMonths = zeros(length(years), 1);

%Loop over the data
for i = 1:length(years)
    singleYearData = Q(Year == years(i));
    singleYearMonths = Month((Year == years(i)));
    [maxDataPoint, maxIndex] = max(singleYearData);
    
    Qp(i) = maxDataPoint;
    QpMonths(i) = singleYearMonths(maxIndex);
end

%% CALCULATE 3 FLOOD FREQUENCY CURVES USING 3 DISTRIBUTIONS
%Sort the Qp data, and associated months
[SortedQp, indices] = sort(Qp, 'descend');
SortQpMonth = QpMonths(indices);

%Declare variables
LogQp = log(SortedQp);
LogMu = mean(LogQp);
LogStDev = std(LogQp);
Mu = mean(SortedQp);
n = length(SortedQp);
m = (1:n); %Rank of flood...
PC1 = 0.25; %Plotting Constants
PC2 = 0.125;
T = (n + PC1)./(m-PC2);
P = 1./T;

%% LOG-NORMAL DISTRIBUTION
w = zeros(n,1);
for i=1:n
    w(i) = (log(1/P(i)^2))^0.5;
end
z = zeros(n,1);
for i=1:n
    z(i) = w(i)-((2.515517+(0.802853*w(i))+(0.010328*w(i)^2))/(1+(1.432788*w(i))+(0.189269*w(i)^2)+(0.001308*w(i)^3)));
end
LogQ = LogMu + (z*LogStDev);
Fitted = exp(LogQ);
LogSeries = Fitted;

%Plot kT on the x-axis, vs. SortedQp on the y-axis
figure(1)
axes('FontSize',14);
semilogy(z,LogSeries, 'k-', 'linewidth', 2)
hold on
semilogy(z,SortedQp, 'ko', 'MarkerFaceColor',[0.8 1 0.3], 'MarkerSize', 6)
xlabel('Standard Normal Variable, K_T', 'fontsize', 16)
ylabel('Maximum Daily Flow Q_p (mm/day)', 'fontsize', 16)

%Plot kT on the x-axis, vs. month of Qp on the y-axis
figure(2)
axes('FontSize',14);
semilogy(z,SortQpMonth, 'ko', 'MarkerFaceColor',[0.8 1 0.3], 'MarkerSize', 6)
xlabel('Standard Normal Variable, K_T', 'fontsize', 16)
ylabel('Month of Q_p', 'fontsize', 16)
xlim = ([1 12]);


%% GUMBEL DISTRIBUTION (EVI)
%%%0.44 is a hard-coded, empirical parameter
C = 0.44;
T_Gringorten = (n + 1 - (2*C))./(m-C);
yT = zeros(n,1);
for i=1:n
    yT(i) = (-1)*log(log(T_Gringorten(i)/(T_Gringorten(i)-1)));
end
GumbSeries = yT;

%Plot yT on the x-axis, vs. SortedQp on the y-axis
figure(3)
axes('FontSize',14);
plot(GumbSeries,SortedQp,'ko', 'MarkerFaceColor',[0.8 0.2 0.3], 'MarkerSize', 6)
ylim([0 1.1*(max(SortedQp))])
xlabel('Reduced Variate, y_T','fontsize', 16)
ylabel('Maximum Daily Flow Q_p (mm/day)', 'fontsize', 16)

%Plot yT on the x-axis, vs. month of Qp on the y-axis
figure(4)
axes('FontSize',14);
plot(GumbSeries,SortQpMonth,'ko', 'MarkerFaceColor',[0.8 0.2 0.3], 'MarkerSize', 6)
ylim([1 12])
xlabel('Reduced Variate, y_T','fontsize', 16)
ylabel('Month of Q_p', 'fontsize', 16)

%% EXPONENTIAL DISTRIBTUTION
Lamda = 1/Mu;
Fitted = -log(P)/Lamda;
ExpSeries = Fitted;

%Plot yT on the x-axis, vs. SortedQp on the y-axis
figure(5)
axes('FontSize',14);
plot(ExpSeries,SortedQp,'ko', 'MarkerFaceColor',[0.35 0.1 0.8], 'MarkerSize', 6)
ylim([0 1.1*(max(SortedQp))])
xlabel('Reduced Variate, y_T','fontsize', 16)
ylabel('Maximum Daily Flow Q_p (mm/day)', 'fontsize', 16)

%Plot yT on the x-axis, vs. month of Qp on the y-axis
figure(6)
axes('FontSize',14);
plot(ExpSeries,SortQpMonth,'ko', 'MarkerFaceColor',[0.35 0.1 0.8], 'MarkerSize', 6)
ylim([1 12])
xlabel('Reduced Variate, y_T','fontsize', 16)
ylabel('Month of Q_p', 'fontsize', 16)

