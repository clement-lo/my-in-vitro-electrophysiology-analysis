% time_frequency_analysis.m

% MATLAB Script for Time-Frequency Analysis of Intrinsic Oscillations

%% Function to Load Electrophysiological Data
function [time, voltage] = load_data(file_path)
    % Load electrophysiological data from a CSV file.
    % Args:
    %     file_path (char): Path to the input data file.
    % Returns:
    %     time (array): Array of time points.
    %     voltage (array): Array of voltage values corresponding to time points.
    
    % Read the CSV file
    data = readmatrix(file_path);
    
    % Check if the data has at least two columns
    if size(data, 2) < 2
        error('The input data must contain at least two columns: Time and Voltage.');
    end
    
    time = data(:, 1);  % First column is Time
    voltage = data(:, 2);  % Second column is Voltage
end

%% Function to Compute and Plot the Power Spectral Density (PSD)
function plot_psd(time, voltage, fs)
    % Compute and plot the power spectral density (PSD) of the electrophysiological signal.
    % Args:
    %     time (array): Array of time points.
    %     voltage (array): Array of voltage values corresponding to time points.
    %     fs (double): Sampling frequency of the data (in Hz).

    [Pxx, f] = pwelch(voltage, [], [], [], fs);
    figure;
    plot(f, 10 * log10(Pxx));
    xlabel('Frequency (Hz)');
    ylabel('Power/Frequency (dB/Hz)');
    title('Power Spectral Density (PSD)');
    grid on;
end

%% Function to Compute and Plot the Spectrogram
function plot_spectrogram(time, voltage, fs)
    % Compute and plot the spectrogram of the electrophysiological signal.
    % Args:
    %     time (array): Array of time points.
    %     voltage (array): Array of voltage values corresponding to time points.
    %     fs (double): Sampling frequency of the data (in Hz).

    window = 256;  % Window length for the spectrogram
    noverlap = 128;  % Number of overlapping samples
    nfft = 512;  % Number of FFT points
    [s, f, t] = spectrogram(voltage, window, noverlap, nfft, fs);
    figure;
    imagesc(t, f, 10 * log10(abs(s)));
    axis xy;
    xlabel('Time (s)');
    ylabel('Frequency (Hz)');
    title('Spectrogram');
    colorbar;
end

%% Function to Compute and Plot Coherence Between Two Signals
function plot_coherence(time, voltage1, voltage2, fs)
    % Compute and plot the coherence between two electrophysiological signals.
    % Args:
    %     time (array): Array of time points.
    %     voltage1 (array): Array of voltage values for the first signal.
    %     voltage2 (array): Array of voltage values for the second signal.
    %     fs (double): Sampling frequency of the data (in Hz).

    [Cxy, f] = mscohere(voltage1, voltage2, [], [], [], fs);
    figure;
    plot(f, Cxy);
    xlabel('Frequency (Hz)');
    ylabel('Coherence');
    title('Coherence between Two Signals');
    grid on;
end

%% Main Script to Run the Time-Frequency Analysis
try
    % Define file path and sampling frequency
    file_path = '../data/intrinsic_oscillations_data.csv';  % Update this path as needed
    fs = 1000;  % Sampling frequency in Hz

    % Load the data
    [time, voltage] = load_data(file_path);
    disp('Data loaded successfully.');

    % Plot Power Spectral Density (PSD)
    plot_psd(time, voltage, fs);

    % Plot Spectrogram
    plot_spectrogram(time, voltage, fs);

    % Simulate another signal for coherence analysis (using filtered noise)
    [b, a] = butter(4, [0.1 0.4], 'bandpass');  % Band-pass filter
    voltage2 = filtfilt(b, a, randn(size(voltage)));

    % Plot Coherence between the original and simulated signals
    plot_coherence(time, voltage, voltage2, fs);

catch ME
    fprintf('An error occurred during analysis: %s\n', ME.message);
end