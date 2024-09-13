% action_potential_analysis.m
% This script performs action potential analysis on intracellular recordings using MATLAB.

% Add necessary paths for toolboxes
addpath('path/to/your/toolboxes'); % Replace with actual paths if needed

%% 1. Data Loading Module
function [signal, sampling_rate] = load_data(file_path, file_type)
    % Load intracellular action potential data using appropriate loaders based on the file type.
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
    % Load action potential data from an ABF file using abfload or similar functions.
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
    % Load action potential data from a Neo-compatible file using MATLAB.
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
function preprocessed_signal = preprocess_signal(signal, sampling_rate, detrend_signal, freq_min, freq_max)
    % Preprocess the loaded signal by detrending and bandpass filtering.
    % Args:
    % - signal (vector): Raw signal data.
    % - sampling_rate (float): Sampling rate of the recording.
    % - detrend_signal (bool): Whether to detrend the signal.
    % - freq_min (float): Minimum frequency for bandpass filter.
    % - freq_max (float): Maximum frequency for bandpass filter.
    % Returns:
    % - preprocessed_signal (vector): Preprocessed signal.

    if detrend_signal
        signal = detrend(signal);  % Remove linear trend from the signal
    end
    preprocessed_signal = bandpass_filter(signal, sampling_rate, freq_min, freq_max);
end

function filtered_signal = bandpass_filter(signal, sampling_rate, freq_min, freq_max)
    % Apply a bandpass filter to the signal.
    % Args:
    % - signal (vector): Signal data.
    % - sampling_rate (float): Sampling rate of the recording.
    % - freq_min (float): Minimum frequency for bandpass filter.
    % - freq_max (float): Maximum frequency for bandpass filter.
    % Returns:
    % - filtered_signal (vector): Filtered signal.

    [b, a] = butter(4, [freq_min, freq_max] / (sampling_rate / 2), 'bandpass');  % Design Butterworth filter
    filtered_signal = filtfilt(b, a, signal);  % Apply zero-phase filtering
end

%% 3. Spike Detection Module
function spike_times = detect_action_potentials(signal, sampling_rate, threshold)
    % Detect action potentials using a voltage threshold-based method.
    % Args:
    % - signal (vector): Preprocessed signal data.
    % - sampling_rate (float): Sampling rate of the recording.
    % - threshold (float): Voltage threshold for spike detection in mV.
    % Returns:
    % - spike_times (vector): Times of detected spikes.

    [pks, spike_indices] = findpeaks(-signal, 'MinPeakHeight', abs(threshold));  % Detect negative peaks
    spike_times = spike_indices / sampling_rate;  % Convert to time in seconds
end

%% 4. Interspike Interval (ISI) Analysis Module
function isi_values = compute_isi(spike_times)
    % Compute Interspike Intervals (ISI) from detected spikes.
    % Args:
    % - spike_times (vector): Times of detected spikes.
    % Returns:
    % - isi_values (vector): Interspike intervals in milliseconds.

    isi_values = diff(spike_times) * 1000;  % Convert ISI to milliseconds
end

function plot_isi_histogram(isi_values, bins)
    % Plot histogram of Interspike Intervals (ISI).
    % Args:
    % - isi_values (vector): Interspike intervals.
    % - bins (int): Number of bins for histogram. Default is 30.

    figure;
    histogram(isi_values, bins, 'FaceColor', 'skyblue', 'EdgeColor', 'black');
    xlabel('Interspike Interval (ms)');
    ylabel('Frequency');
    title('ISI Histogram');
    grid on;
end

%% 5. Visualization Module
function plot_action_potentials(signal, spike_times, sampling_rate, interactive)
    % Plot the action potential traces and detected spikes.
    % Args:
    % - signal (vector): Signal data (raw or preprocessed).
    % - spike_times (vector): Times of detected spikes.
    % - sampling_rate (float): Sampling rate of the recording.
    % - interactive (bool): Whether to use interactive plotting (ignored in MATLAB).

    time_vector = (0:length(signal) - 1) / sampling_rate;  % Time vector for plotting
    spike_indices = round(spike_times * sampling_rate);  % Convert spike times to indices

    figure;
    plot(time_vector, signal, 'b', 'DisplayName', 'Action Potential Trace');
    hold on;
    plot(spike_times, signal(spike_indices), 'ro', 'DisplayName', 'Detected Spikes');
    xlabel('Time (s)');
    ylabel('Voltage (mV)');
    title('Action Potential Trace with Detected Spikes');
    legend show;
    grid on;
end

%% Main function
function main(file_path, file_type)
    % Main function to perform action potential analysis.
    % Args:
    % - file_path (str): Path to the data file.
    % - file_type (str): Type of file ('abf' or 'neo'). Default is 'abf'.

    % Step 1: Load Data
    [signal, sampling_rate] = load_data(file_path, file_type);
    
    % Step 2: Preprocess Data
    detrend_signal = true;
    freq_min = 1;  % Hz
    freq_max = 100;  % Hz
    preprocessed_signal = preprocess_signal(signal, sampling_rate, detrend_signal, freq_min, freq_max);
    
    % Step 3: Detect Action Potentials
    threshold = -30.0;  % mV
    spike_times = detect_action_potentials(preprocessed_signal, sampling_rate, threshold);
    disp('Detected Spike Times:');
    disp(spike_times);
    
    % Step 4: Compute ISI
    isi_values = compute_isi(spike_times);
    disp('Computed ISI Values (ms):');
    disp(isi_values);
    
    % Step 5: Visualize Results
    plot_action_potentials(preprocessed_signal, spike_times, sampling_rate, false);
    plot_isi_histogram(isi_values, 30);
end

% Run the main function with an example file path
main('data/example_data.abf', 'abf');  % Adjust the path for your dataset