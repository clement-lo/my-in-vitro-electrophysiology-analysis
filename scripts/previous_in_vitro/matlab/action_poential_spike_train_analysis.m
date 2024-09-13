% action_potential_spike_train_analysis.m

% MATLAB Script for Analyzing Action Potential Properties and Spike Train Dynamics

%% Function to Load Electrophysiology Data
function data = load_data(file_path)
    % Load electrophysiology data from a CSV file.
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
        if ~all(ismember({'Time', 'Voltage'}, data.Properties.VariableNames))
            error('ValueError: The input data must contain "Time" and "Voltage" columns.');
        end
    catch ME
        rethrow(ME);
    end
end

%% Function to Detect Action Potentials and Analyze Properties
function ap_properties = analyze_action_potentials(data, threshold)
    % Analyze action potential properties in electrophysiology data.
    % Args:
    %     data (table): Electrophysiology data containing time and voltage columns.
    %     threshold (double): Voltage threshold for peak detection.
    % Returns:
    %     ap_properties (table): Table containing detected AP properties (e.g., amplitude, half-width).
    
    time = data.Time;
    voltage = data.Voltage;
    
    % Detect action potentials (APs) using peak detection
    [pks, locs] = findpeaks(voltage, 'MinPeakHeight', threshold);
    
    % Calculate action potential properties
    amplitudes = pks;
    half_widths = diff(locs) * mean(diff(time));  % Rough estimate of half-width using sample rate
    
    ap_properties = table(locs, amplitudes, half_widths, ...
        'VariableNames', {'AP_Index', 'Amplitude', 'Half_Width'});
end

%% Function to Analyze Spike Train Dynamics
function [firing_rate_hist, isi_distribution] = analyze_spike_train(ap_properties, bin_size)
    % Analyze spike train dynamics such as firing rate and interspike interval (ISI) distribution.
    % Args:
    %     ap_properties (table): Table containing detected action potentials.
    %     bin_size (double): Bin size for calculating firing rate histogram (in seconds).
    % Returns:
    %     firing_rate_hist (array): Firing rate histogram.
    %     isi_distribution (array): Interspike interval distribution.
    
    spike_times = ap_properties.AP_Index;  % Spike times based on indices
    
    % Calculate ISI (Interspike Interval)
    isi = diff(spike_times);  % Interspike intervals
    
    % Calculate Firing Rate Histogram
    firing_rate_hist = histcounts(spike_times, 'BinWidth', bin_size);
    
    isi_distribution = isi;
end

%% Function to Plot Results
function plot_results(data, ap_properties, firing_rate_hist, isi_distribution)
    % Plot action potential properties, firing rate histogram, and ISI distribution.
    % Args:
    %     data (table): Electrophysiology data.
    %     ap_properties (table): Table containing detected action potential properties.
    %     firing_rate_hist (array): Firing rate histogram.
    %     isi_distribution (array): Interspike interval distribution.

    % Plot raw data with detected APs
    figure;
    plot(data.Time, data.Voltage, 'b-');
    hold on;
    scatter(data.Time(ap_properties.AP_Index), ap_properties.Amplitude, 'ro');
    xlabel('Time (s)');
    ylabel('Voltage (mV)');
    title('Action Potential Detection');
    legend('Voltage Trace', 'Detected APs');
    hold off;
    
    % Plot firing rate histogram
    figure;
    histogram(firing_rate_hist, 'BinWidth', 0.01, 'FaceColor', 'blue', 'EdgeColor', 'black');
    xlabel('Firing Rate (Hz)');
    ylabel('Count');
    title('Firing Rate Histogram');
    
    % Plot ISI distribution
    figure;
    histogram(isi_distribution, 'BinWidth', 0.01, 'FaceColor', 'green', 'EdgeColor', 'black');
    xlabel('Interspike Interval (s)');
    ylabel('Count');
    title('Interspike Interval (ISI) Distribution');
end

%% Main Script to Run the Analysis
try
    % Set file path and parameters
    file_path = '../../data/action_potential_data.csv';  % Ensure the data file exists in the 'data/' directory
    threshold = 0;  % Set the voltage threshold for peak detection
    bin_size = 0.01;  % Bin size for firing rate histogram
    
    % Load data
    data = load_data(file_path);
    
    % Perform AP analysis
    ap_properties = analyze_action_potentials(data, threshold);
    
    % Analyze spike train dynamics
    [firing_rate_hist, isi_distribution] = analyze_spike_train(ap_properties, bin_size);
    
    % Plot the results
    plot_results(data, ap_properties, firing_rate_hist, isi_distribution);

catch ME
    fprintf('An error occurred: %s\n', ME.message);
end