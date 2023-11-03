%% Code for Climate Description section of the CEE450 Class Project Fall 2011
%
%%This code takes daily data and computes hydrologic signatures for a catchment.
%
%%Modified by Mary Yaeger from code created by Mary Yaeger and Evan Coopersmith for
%%CEE598 Hydrologic Variability, Fall 2010: HW3 and Class Project
%%
clear all
close all

%% INSERT NAME OF YOUR MOPEX DATA FILE, WITHOUT THE FILE EXTENSION
%**EXAMPLE: for data file KS304s.csv -> FileName = 'KS304';

FileName = '212_30years';

%% Load the MOPEX data
%The readme.txt file tells you how the data file is structured
Data = importdata([FileName, '.csv']);

%Parse the time data into columns
Year  = Data(:,1);
Month = Data(:,2);
Day   = Data(:,3);

%Get the number of calendar years
numYears = length(unique(Year));

%% Annual Total Values
%Create a storage matrix for the output
AnnualTotals = zeros(numYears, 5);

%Loop through the data, where j is the number of data types, in the order
%they appear in the data file (see readme.txt)
for j = 1:5
    X = Data(:, j + 3); %Skip 3 time columns
    
    % Check in case the data does not actually start on 1/1
    if (Month(1) == 1) && (Day(1) == 1)
        yearCount = 0;
    else
        yearCount = 1;
    end
    
    %Loop through the data, where i is the number of days, and change the year any time there is a Jan 1
    for i = 1:length(X)
        %Check for year change first.
        if (Month(i) == 1) && (Day(i) == 1)
            yearCount = yearCount + 1;
        end
        %Now add to total flow for the year
        AnnualTotals(yearCount,j) = AnnualTotals(yearCount,j) + X(i);
    end %end time loop
end %end data loop

%At the annual scale, E = P - Q
AnnualTotalE = AnnualTotals(:,1) - AnnualTotals(:,3);
%Create a vector of data years
Years = unique(Year);
%Calculate probability of exceedance
ProbExceedance = (100 * ((1:length(AnnualTotals))./(length(AnnualTotals) + 1)))';
%Add these 3 new columns to the 5 columns of the AnnualTotals matrix
AnnualTotals = [AnnualTotals, AnnualTotalE, Years, ProbExceedance];

%% Mean Annual Values
%Values display onscreen for use in calculating Aridity Index and
%Evaporative Index (for Budyko curve plotting), as well as Runoff Coefficient and
%Baseflow Index
MeanAnnualP = mean(AnnualTotals(:,1));
disp(['MeanAnnualP = ', num2str(MeanAnnualP)] )

MeanAnnualEp = mean(AnnualTotals(:,2));
disp(['MeanAnnualEp = ', num2str(MeanAnnualEp)] )

MeanAnnualQ = mean(AnnualTotals(:,3));
disp(['MeanAnnualQ = ', num2str(MeanAnnualQ)] )

MeanAnnualQs = mean(AnnualTotals(:,4));
disp(['MeanAnnualQs = ', num2str(MeanAnnualQs)] )

MeanAnnualQu = mean(AnnualTotals(:,5));
disp(['MeanAnnualQu = ', num2str(MeanAnnualQu)] )

MeanAnnualE = mean(AnnualTotals(:,6));
disp(['MeanAnnualE = ', num2str(MeanAnnualE)] )

%% Monthly Regime Curve
%Create storage for the monthly averages
MonthlyAverages =  zeros(12, 5);

%Loop through the data, where j is the number of data types, in the order
%they appear in the data file (see readme.txt)
for j = 1:5
    X = Data(:, j + 3); %Skip 3 time columns
    %Loop through the months and sum monthly data
    for i=1:12
        MonthlyAverages(i, j) = sum(X(Month == i));
    end %time loop    
end

%Calculate monthly averages; ie Sum_May_Q/numYears = Average_May_Q
MonthlyAverages = MonthlyAverages ./ numYears;

%% Flow Duration Curve.
%Create storage for the FDC
Sorted =  zeros(length(Data), 5);

%Loop through the data, where j is the number of data types, in the order
%they appear in the data file (see readme.txt)
for j = 1:5
    X = Data(:, j + 3); %Skip 3 time columns
    Sorted(:, j) = sort(X, 'descend');    
end

%Calculate exceedance probability (in %)
Probability = (100 * ((1:length(Data))./(length(Data) + 1)))';
FDC = [Sorted, Probability];

%% Plot Signatures

Months = [1,2,3,4,5,6,7,8,9,10,11,12]';

%Plot climate seasonality
figure(1)
axes('FontSize',14);
plot(Months,MonthlyAverages(:,1), 'b-', 'linewidth', 3)
hold on
plot(Months,MonthlyAverages(:,2), 'r-o', 'linewidth', 3)
xlim([1 12])
ylim([0 1.1*max(max(MonthlyAverages))])
xlabel('Month','fontsize', 14)
ylabel('mm/mo', 'fontsize', 14)
legend('Ave monthly P','Ave monthly Ep') 

%Plot annual totals as a function of exceedance probability
figure(2)
axes('FontSize',14);
semilogy(AnnualTotals(:,8),(sort(AnnualTotals(:,1), 'descend')), 'bo') %, 'linewidth',3)
% semilogy(AnnualTotals(:,8),(sort(AnnualTotals(:,1), 'descend')), 'b-', 'linewidth',3)
hold on
semilogy(AnnualTotals(:,8),(sort(AnnualTotals(:,3), 'descend')), 'co') %, 'linewidth', 3)
% semilogy(AnnualTotals(:,8),(sort(AnnualTotals(:,3), 'descend')), 'c--', 'linewidth', 3)
semilogy(AnnualTotals(:,8),(sort(AnnualTotals(:,4), 'descend')), 'g-.', 'linewidth', 3)
semilogy(AnnualTotals(:,8),(sort(AnnualTotals(:,5), 'descend')), 'm:', 'linewidth', 4)
legend('Annual P', 'Annual Q', 'Annual Q_s', 'Annual Q_u')
xlabel('Exceedance Probability', 'fontsize', 16);
ylabel('Annual Totals', 'fontsize', 16);
ylim([10^1 1.2*max(AnnualTotals(:,1))])
xlim([0 100])

%Plot monthly regime curves
figure(3)
axes('FontSize',14);
bar(Months,MonthlyAverages(:,1)) 
hold on
plot(Months,MonthlyAverages(:,2), 'y-o', 'linewidth', 3)
plot(Months,MonthlyAverages(:,3), 'c--', 'linewidth', 3)
plot(Months,MonthlyAverages(:,4), 'g-.', 'linewidth', 3)
plot(Months,MonthlyAverages(:,5), 'm:', 'linewidth', 4)
xlim([1 12])
% ylim([0 1.1*max(max(MonthlyAverages))])
ylim([0 1.1*max(max(MonthlyAverages))])
xlabel('Month','fontsize', 14)
ylabel('mm/mo', 'fontsize', 14)
legend('Ave monthly P','Ave monthly Ep','Ave monthly Q', 'Ave monthly Q_s', 'Ave monthly Q_u') 

%Plot the flow duration curves 
figure(4)
axes('FontSize',14);
semilogy(FDC(:,6),FDC(:,1), 'b-', 'linewidth', 3)
hold on
semilogy(FDC(:,6),FDC(:,3), 'c--', 'linewidth', 3)
semilogy(FDC(:,6),FDC(:,4), 'g-.', 'linewidth', 3)
semilogy(FDC(:,6),FDC(:,5), 'm:', 'linewidth', 4)
legend('P', 'Q', 'Q_s', 'Q_u')
xlabel('Exceedance Probability', 'fontsize', 16);
ylabel('Daily Flow (mm/day)', 'fontsize', 16);
ylim([10^-4 1.2*max(FDC(:,1))])
xlim([0 100])
