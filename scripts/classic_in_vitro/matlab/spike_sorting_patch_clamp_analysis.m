% spike_sorting_patch_clamp_analysis.m
% This script performs spike sorting and patch-clamp analysis on intracellular recordings using MATLAB.

% Add necessary paths for toolboxes
addpath('path/to/your/toolboxes'); % Replace with actual paths if needed

%% 1. Data Loading Module
function [signal, sampling_rate] = load_data(file_path, file_type)
    % Load patch-clamp data using appropriate loaders based on the file type.
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
    % Load patch-clamp data from an ABF file using abfload or similar functions.
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
    % Load patch-clamp data from a Neo-compatible file using MATLAB.
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
function filtered_signal = preprocess_signal(signal, sampling_rate, freq_min, freq_max)
    % Apply a bandpass filter to the signal.
    % Args:
    % - signal (vector): Raw signal data.
    % - sampling_rate (float): Sampling rate of the recording.
    % - freq_min (int): Minimum frequency for bandpass filter.
    % - freq_max (int): Maximum frequency for bandpass filter.
    % Returns:
    % - filtered_signal (vector): Filtered signal.

    if ~isvector(signal)
        error('Signal must be a vector.');
    end
    [b, a] = butter(4, [freq_min, freq_max] / (sampling_rate / 2), 'bandpass');  % Design Butterworth filter
    filtered_signal = filtfilt(b, a, signal);  % Apply zero-phase filtering
end

%% 3. Spike Detection Module
function spike_times = detect_spikes_threshold(signal, sampling_rate, threshold)
    % Detect spikes using a simple threshold-based method.
    % Args:
    % - signal (vector): Preprocessed signal data.
    % - sampling_rate (float): Sampling rate of the recording.
    % - threshold (float): Threshold for spike detection in terms of standard deviations above mean.
    % Returns:
    % - spike_times (vector): Times of detected spikes.

    mean_val = mean(signal);
    std_val = std(signal);
    spike_indices = find(signal > (mean_val + threshold * std_val));  % Detect threshold crossings
    spike_times = spike_indices / sampling_rate;  % Convert to time in seconds
end

function spike_times = detect_spikes_wavelet(signal, sampling_rate, wavelet, threshold)
    % Detect spikes using wavelet transform for noise reduction and feature extraction.
    % Args:
    % - signal (vector): Preprocessed signal data.
    % - sampling_rate (float): Sampling rate of the recording.
    % - wavelet (str): Type of wavelet to use for transformation. Default is 'haar'.
    % - threshold (float): Threshold for detecting spikes in wavelet coefficients.
    % Returns:
    % - spike_times (vector): Times of detected spikes.

    [c, l] = wavedec(signal, 4, wavelet);  % Wavelet decomposition
    sigma = median(abs(c)) / 0.6745;  % Estimate noise level
    uthresh = sigma * sqrt(2 * log(length(signal)));
    c = wthresh(c, 's', uthresh);  % Soft thresholding
    reconstructed_signal = waverec(c, l, wavelet);  % Reconstruct signal
    spike_times = detect_spikes_threshold(reconstructed_signal, sampling_rate, threshold);  % Detect spikes
end

function spike_times = detect_spikes_template_matching(signal, template, sampling_rate, threshold)
    % Detect spikes using template matching.
    % Args:
    % - signal (vector): Preprocessed signal data.
    % - template (vector): Template of the spike waveform to match against.
    % - sampling_rate (float): Sampling rate of the recording.
    % - threshold (float): Correlation threshold to detect spikes.
    % Returns:
    % - spike_times (vector): Times of detected spikes.

    correlation = xcorr(signal, template, 'coeff');  % Cross-correlation
    spike_indices = find(correlation > threshold * max(correlation));  % Find indices above threshold
    spike_times = spike_indices / sampling_rate;  % Convert to time in seconds
end

%% 4. Feature Extraction Module
function features = extract_spike_features(signal, spike_times, sampling_rate, window)
    % Extract features like spike width, amplitude, and waveform shape for clustering.
    % Args:
    % - signal (vector): Preprocessed signal data.
    % - spike_times (vector): Times of detected spikes.
    % - sampling_rate (float): Sampling rate of the recording.
    % - window (int): Number of samples to extract around each spike for feature calculation.
    % Returns:
    % - features (matrix): Extracted features.

    if window <= 0
        error('Window size must be positive.');
    end
    features = [];
    for i = 1:length(spike_times)
        start_idx = round(spike_times(i) * sampling_rate) - window;
        end_idx = round(spike_times(i) * sampling_rate) + window;
        if start_idx < 1 || end_idx > length(signal)
            continue;
        end
        waveform = signal(start_idx:end_idx);
        amplitude = max(waveform) - min(waveform);
        width = find(waveform == max(waveform)) - find(waveform == min(waveform));
        features = [features; amplitude, width];  % Append features
    end
end

%% 5. Spike Sorting and Clustering Module
function labels = sort_spikes(features, method, n_clusters)
    % Perform spike sorting using clustering algorithms like K-means or GMM.
    % Args:
    % - features (matrix): Extracted spike features.
    % - method (str): Clustering method ('kmeans' or 'gmm').
    % - n_clusters (int): Number of clusters for sorting.
    % Returns:
    % - labels (vector): Cluster labels for each spike.

    if n_clusters <= 0
        error('Number of clusters must be positive.');
    end
    if strcmp(method, 'kmeans')
        labels = kmeans(features, n_clusters);
    elseif strcmp(method, 'gmm')
        gm = fitgmdist(features, n_clusters);
        labels = cluster(gm, features);
    else
        error('Invalid method. Use "kmeans" or "gmm".');
    end
end

%% 6. Visualization Module
function plot_raster(spike_times)
    % Plot raster plot of the spike sorting results.
    % Args:
    % - spike_times (vector): Times of detected spikes.

    figure;
    for i = 1:length(spike_times)
        line([spike_times(i), spike_times(i)], [0, 1], 'Color', 'k', 'LineWidth', 1);
        hold on;
    end
    xlabel('Time (s)');
    ylabel('Spike Events');
    title('Raster Plot');
    hold off;
end

function plot_firing_rate_histogram(spike_times, bin_size)
    % Plot histogram of firing rates using Matplotlib for visualization.
    % Args:
    % - spike_times (vector): Times of detected spikes.
    % - bin_size (float): Bin size in seconds for histogram.

    bins = 0:bin_size:max(spike_times);
    hist_values = histcounts(spike_times, bins);
    firing_rates = hist_values / bin_size;
    figure;
    bar(bins(1:end-1), firing_rates, 'histc');
    xlabel('Time (s)');
    ylabel('Firing Rate (Hz)');
    title('Firing Rate Histogram');
end

%% Main function
function main(file_path, file_type)
    % Main function to perform spike sorting and patch-clamp analysis.
    % Args:
    % - file_path (str): Path to the data file.
    % - file_type (str): Type of file ('abf' or 'neo').

    % Step 1: Load Data
    [signal, sampling_rate] = load_data(file_path, file_type);
    
    % Step 2: Preprocess Data
    filtered_signal = preprocess_signal(signal, sampling_rate, 300, 3000);
    
    % Step 3: Detect Spikes
    spike_times = detect_spikes_threshold(filtered_signal, sampling_rate, 5.0);
    disp('Detected Spike Times:');
    disp(spike_times);
    
    % Step 4: Extract Spike Features
    features = extract_spike_features(filtered_signal, spike_times, sampling_rate, 30);
    disp('Extracted Spike Features:');
    disp(features);
    
    % Step 5: Sort Spikes
    labels = sort_spikes(features, 'kmeans', 2);
    disp('Spike Sorting Labels:');
    disp(labels);
    
    % Step 6: Visualize Results
    plot_raster(spike_times);
    plot_firing_rate_histogram(spike_times, 0.1);
end

% Run the main function with an example file path
main('data/example_data.abf', 'abf');  % Adjust the path for your dataset