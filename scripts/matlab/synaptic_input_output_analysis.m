% synaptic_input_output_analysis.m

% Synaptic Input-Output Analysis in MATLAB

% Function to load data
function data = load_data(file_path)
    % Load synaptic input-output data from a CSV file.
    % Args:
    %     file_path (str): Path to the input data file.
    % Returns:
    %     data (table): Loaded data as a MATLAB table.
    
    data = readtable(file_path);
end

% Function to perform synaptic input-output analysis
function [fitresult, gof] = analyze_synaptic_io(data)
    % Analyze synaptic input-output relationships using curve fitting.
    % Args:
    %     data (table): Synaptic data containing input and output columns.
    % Returns:
    %     fitresult (cfit): Fitted curve.
    %     gof (struct): Goodness of fit structure.

    % Extract input and output data
    input_data = data.Input;
    output_data = data.Output;

    % Define the sigmoid function for curve fitting
    sigmoid = @(a, b, c, x) c ./ (1 + exp(-(x - a) / b));

    % Fit the sigmoid curve to the data
    [fitresult, gof] = fit(input_data, output_data, sigmoid, ...
        'StartPoint', [0, 1, max(output_data)]);
end

% Function to plot the results
function plot_results(data, fitresult)
    % Plot synaptic input-output data and the fitted curve.
    % Args:
    %     data (table): Synaptic data containing input and output columns.
    %     fitresult (cfit): Fitted curve object.

    % Plot data points
    figure;
    scatter(data.Input, data.Output, 'filled');
    hold on;

    % Plot the fitted curve
    plot(fitresult, 'r-');
    xlabel('Synaptic Input');
    ylabel('Synaptic Output');
    title('Synaptic Input-Output Analysis');
    legend('Data', 'Fitted Curve');
    hold off;
end

% Main script to run the analysis
file_path = '../../data/synaptic_io_data.csv'; % Ensure the data file exists in the 'data/' directory
data = load_data(file_path); % Load data

% Perform the analysis
[fitresult, gof] = analyze_synaptic_io(data);

% Plot the results
plot_results(data, fitresult);
