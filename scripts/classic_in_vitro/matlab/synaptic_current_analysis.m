% synaptic_current_analysis.m
% This script performs synaptic current analysis on patch-clamp recordings using MATLAB.

% Add necessary paths for toolboxes
addpath('path/to/your/toolboxes'); % Replace with actual paths if needed

%% 1. Data Loading Module
function [signal, sampling_rate] = load_data(file_path, file_type)
    % Load synaptic current data using appropriate loaders based on the file type.
    % Args:
    % - file_path (str): Path to the data file.
    % - file_type (str): Type of file ('abf' or 'neo').
    % Returns:
    % - signal (vector): Loaded signal data.
    % - sampling_rate (float): Sampling rate of the recording.

    switch file_type
        case 'abf'
            [signal, sampling_rate] = load_abf_data(file_path);
        case 'neo'
            [signal, sampling_rate] = load_neo_data(file_path);
        otherwise
            error('Unsupported file type: %s', file_type);
    end
end

function [signal, sampling_rate] = load_abf_data(file_path)
    % Load synaptic current data from an ABF file using abfload or similar functions.
    % Args:
    % - file_path (str): Path to the ABF file.
    % Returns:
    % - signal (vector): Loaded signal data.
    % - sampling_rate (float): Sampling rate of the recording.

    [data, si] = abfload(file_path);  % Use abfload function to load ABF files
    signal = data(:, 1);  % Assuming single-channel recording
    sampling_rate = 1 / (si * 1e-6);  % Convert sampling interval to Hz
end

function [signal, sampling_rate] = load_neo_data(file_path)
    % Load synaptic current data from a Neo-compatible file using MATLAB.
    % Args:
    % - file_path (str): Path to the Neo file.
    % Returns:
    % - signal (vector): Loaded signal data.
    % - sampling_rate (float): Sampling rate of the recording.

    % Assuming the Neo format is readable via HDF5 or similar in MATLAB
    data = h5read(file_path, '/data');
    sampling_rate = h5readatt(file_path, '/data', 'sampling_rate');  % Adjust the path as needed
    signal = double(data(:));  % Convert to double for processing
end

%% 2. Preprocessing Module
function preprocessed_signal = preprocess_signal(signal, sampling_rate, detrend_signal, freq_min, freq_max, standardize)
    % Preprocess the loaded signal by detrending, bandpass filtering, and standardizing.
    % Args:
    % - signal (vector): Raw signal data.
    % - sampling_rate (float): Sampling rate of the recording.
    % - detrend_signal (bool): Whether to detrend the signal.
    % - freq_min (float): Minimum frequency for bandpass filter.
    % - freq_max (float): Maximum frequency for bandpass filter.
    % - standardize (bool): Whether to standardize the signal.
    % Returns:
    % - preprocessed_signal (vector): Preprocessed signal.

    if detrend_signal
        signal = detrend(signal);  % Remove linear trend from the signal
    end
    [b, a] = butter(4, [freq_min, freq_max] / (sampling_rate / 2), 'bandpass');  % Design Butterworth filter
    preprocessed_signal = filtfilt(b, a, signal);  % Apply zero-phase filtering

    if standardize
        preprocessed_signal = zscore(preprocessed_signal);  % Standardize the signal
    end
end

%% 3. Event Detection Module
function event_times = detect_synaptic_events(signal, sampling_rate, threshold, min_distance)
    % Detect synaptic events (e.g., EPSCs, IPSCs) using a threshold-based method with noise level estimation.
    % Args:
    % - signal (vector): Preprocessed signal data.
    % - sampling_rate (float): Sampling rate of the recording.
    % - threshold (float): Threshold for event detection in terms of standard deviations above mean.
    % - min_distance (float): Minimum distance between events in seconds.
    % Returns:
    % - event_times (vector): Times of detected synaptic events.

    mean_val = mean(signal);
    std_val = std(signal);
    [peaks, locs] = findpeaks(-signal, 'MinPeakHeight', mean_val + threshold * std_val, 'MinPeakDistance', min_distance * sampling_rate);
    event_times = locs / sampling_rate;  % Convert to time in seconds
end

%% 4. Kinetic Analysis Module
function y = exponential_decay(t, A, tau, C)
    % Exponential decay function for fitting synaptic event kinetics.
    % Args:
    % - t (vector): Time vector.
    % - A (float): Amplitude of the decay.
    % - tau (float): Time constant of the decay.
    % - C (float): Offset.
    % Returns:
    % - y (vector): Exponential decay values.

    y = A * exp(-t / tau) + C;
end

function fitted_params = fit_event_kinetics(event_times, signal, sampling_rate, window)
    % Fit decay kinetics of detected synaptic events using an exponential model.
    % Args:
    % - event_times (vector): Times of detected synaptic events.
    % - signal (vector): Preprocessed signal data.
    % - sampling_rate (float): Sampling rate of the recording.
    % - window (float): Time window (in seconds) around each event to fit kinetics.
    % Returns:
    % - fitted_params (cell array): List of fitted parameters for each event.

    fitted_params = {};
    for i = 1:length(event_times)
        start = round((event_times(i) - window / 2) * sampling_rate);
        end_idx = round((event_times(i) + window / 2) * sampling_rate);
        if start < 1 || end_idx > length(signal)
            continue;
        end
        time_vector = (0:(end_idx - start)) / sampling_rate;
        event_signal = signal(start:end_idx) - min(signal(start:end_idx));  % Normalize event signal
        
        % Fit exponential decay model to the event signal
        try
            fit_func = @(p, t) exponential_decay(t, p(1), p(2), p(3));
            params = nlinfit(time_vector, event_signal, fit_func, [1, 0.01, 0]);  % Initial guess for parameters
            fitted_params{end + 1} = params;
        catch
            % Skip if the fitting fails
            continue;
        end
    end
end

%% 5. Visualization Module
function plot_synaptic_traces(signal, sampling_rate)
    % Plot the raw or preprocessed synaptic current traces.
    % Args:
    % - signal (vector): Signal data (raw or preprocessed).
    % - sampling_rate (float): Sampling rate of the recording.

    time_vector = (0:length(signal) - 1) / sampling_rate;
    figure;
    plot(time_vector, signal, 'b');
    xlabel('Time (s)');
    ylabel('Amplitude (pA)');
    title('Synaptic Current Trace');
    grid on;
end

function plot_event_detection(signal, event_times, sampling_rate)
    % Plot detected synaptic events on the synaptic current traces.
    % Args:
    % - signal (vector): Preprocessed signal data.
    % - event_times (vector): Times of detected synaptic events.
    % - sampling_rate (float): Sampling rate of the recording.

    time_vector = (0:length(signal) - 1) / sampling_rate;
    event_indices = round(event_times * sampling_rate);
    
    figure;
    plot(time_vector, signal, 'b', 'DisplayName', 'Synaptic Current');
    hold on;
    plot(event_times, signal(event_indices), 'ro', 'DisplayName', 'Detected Events');
    xlabel('Time (s)');
    ylabel('Amplitude (pA)');
    title('Synaptic Event Detection');
    legend show;
    grid on;
end

%% Main function
function main(file_path, file_type)
    % Main function to perform synaptic current analysis.
    % Args:
    % - file_path (str): Path to the data file.
    % - file_type (str): Type of file ('abf' or 'neo').

    % Step 1: Load Data
    [signal, sampling_rate] = load_data(file_path, file_type);
    
    % Step 2: Preprocess Data
    preprocessed_signal = preprocess_signal(signal, sampling_rate, true, 1, 100, true);
    
    % Step 3: Detect Synaptic Events
    event_times = detect_synaptic_events(preprocessed_signal, sampling_rate, 5.0, 0.005);
    disp('Detected Synaptic Event Times:');
    disp(event_times);
    
    % Step 4: Fit Kinetic Parameters
    fitted_params = fit_event_kinetics(event_times, preprocessed_signal, sampling_rate, 0.05);
    disp('Fitted Kinetic Parameters for Events:');
    disp(fitted_params);
    
    % Step 5: Visualize Results
    plot_synaptic_traces(preprocessed_signal, sampling_rate);
    plot_event_detection(preprocessed_signal, event_times, sampling_rate);
end

% Run the main function with an example file path
main('data/example_data.abf', 'abf');  % Adjust the path for your dataset
