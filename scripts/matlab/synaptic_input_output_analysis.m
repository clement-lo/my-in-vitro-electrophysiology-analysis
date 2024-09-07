% synaptic_analysis.m

% Synaptic Input-Output Analysis in MATLAB

%% Function to Load Data
function data = load_data(file_path)
    % Load synaptic input-output data from a CSV file.
    % Args:
    %     file_path (str): Path to the input data file.
    % Returns:
    %     data (table): Loaded data as a MATLAB table.
    % Raises:
    %     Error if file does not exist or data format is incorrect.
    
    % Check if the file exists
    if ~isfile(file_path)
        error('FileNotFoundError: The file "%s" does not exist.', file_path);
    end
    
    % Try loading the file
    try
        data = readtable(file_path);
        if ~all(ismember({'Input', 'Output'}, data.Properties.VariableNames))
            error('ValueError: The input data must contain "Input" and "Output" columns.');
        end
    catch ME
        rethrow(ME);
    end
end

%% Function to Perform Synaptic Input-Output Analysis
function [fitresult, gof] = analyze_synaptic_io(data, model)
    % Analyze synaptic input-output relationships using curve fitting.
    % Args:
    %     data (table): Synaptic data containing input and output columns.
    %     model (str): Model type for curve fitting ('sigmoid' or 'linear').
    % Returns:
    %     fitresult (cfit): Fitted curve object.
    %     gof (struct): Goodness of fit structure.
    
    % Validate the model parameter
    if ~ismember(model, {'sigmoid', 'linear'})
        error('ValueError: Model must be "sigmoid" or "linear".');
    end
    
    % Extract input and output data
    input_data = data.Input;
    output_data = data.Output;
    
    % Define model functions for curve fitting
    sigmoid = @(a, b, c, x) c ./ (1 + exp(-(x - a) / b));
    linear = @(m, c, x) m * x + c;
    
    % Fit the selected model to the data
    try
        switch model
            case 'sigmoid'
                [fitresult, gof] = fit(input_data, output_data, ...
                    fittype(sigmoid), 'StartPoint', [0, 1, max(output_data)]);
            case 'linear'
                [fitresult, gof] = fit(input_data, output_data, ...
                    fittype(linear), 'StartPoint', [1, 0]);
        end
    catch ME
        error('FitError: An error occurred during curve fitting: %s', ME.message);
    end
end

%% Function to Plot the Results
function plot_results(data, fitresult, model)
    % Plot synaptic input-output data and the fitted curve.
    % Args:
    %     data (table): Synaptic data containing input and output columns.
    %     fitresult (cfit): Fitted curve object.
    %     model (str): Model type used for curve fitting ('sigmoid' or 'linear').
    
    % Plot data points
    figure;
    scatter(data.Input, data.Output, 'filled');
    hold on;
    
    % Plot the fitted curve
    plot(fitresult, 'r-');
    xlabel('Synaptic Input');
    ylabel('Synaptic Output');
    title(sprintf('Synaptic Input-Output Analysis (%s Model)', model));
    legend('Data', 'Fitted Curve');
    hold off;
end

%% Main Script to Run the Analysis
try
    % Set file path and model type
    file_path = '../../data/synaptic_io_data.csv';  % Ensure the data file exists in the 'data/' directory
    model_type = 'sigmoid';  % Change to 'linear' for a different model
    
    % Load data
    data = load_data(file_path);
    
    % Perform analysis
    [fitresult, gof] = analyze_synaptic_io(data, model_type);
    
    % Display goodness of fit
    disp(gof);
    
    % Plot the results
    plot_results(data, fitresult, model_type);

catch ME
    fprintf('An error occurred: %s\n', ME.message);
end
