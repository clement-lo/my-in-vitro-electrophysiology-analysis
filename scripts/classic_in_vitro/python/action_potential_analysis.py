# action_potential_analysis.py

# Import necessary libraries
import logging
import yaml  # For handling configuration files
import pyabf  # For handling ABF (Axon Binary Format) files
import neo  # For handling Neo-compatible formats
import numpy as np  # For numerical operations
import matplotlib.pyplot as plt  # For static visualization
import plotly.express as px  # For interactive visualization
from scipy.signal import detrend, butter, sosfilt, find_peaks  # For signal preprocessing and spike detection
from elephant.statistics import isi  # For interspike interval analysis
import quantities as pq  # For handling physical quantities
from joblib import Parallel, delayed  # For parallel processing of large datasets
import numpy as np
import pywt  # For wavelet transform
from scipy.signal import correlate
from sklearn.ensemble import RandomForestClassifier  # Example for ML-based spike detection
import quantities as pq
from elephant.statistics import isi, cv2



# Configure logging for detailed output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration Management Module
def load_config(config_file):
    """Load configuration settings from a YAML file and validate."""
    default_config = {
        'data': {'file_path': 'data/example_data.abf', 'file_type': 'abf'},
        'preprocessing': {'detrend_signal': True, 'freq_min': 1, 'freq_max': 100},
        'spike_detection': {'method': 'threshold', 'threshold': -30.0},
        'analysis': {'advanced_isi': True}
    }
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        # Merge with defaults
        config = {**default_config, **config}
        logging.info(f"Configuration loaded and validated from {config_file}.")
        return config
    except Exception as e:
        logging.error(f"Failed to load configuration: {e}")
        return default_config  # Fallback to default configuration

# Data Loading Module
def load_data(file_path, file_type='abf'):
    """
    Load intracellular action potential data using appropriate loaders based on the file type.
    
    Args:
    - file_path (str): Path to the data file.
    - file_type (str): Type of file ('abf' or 'neo').
    
    Returns:
    - signal (np.ndarray): Loaded signal data.
    - sampling_rate (float): Sampling rate of the recording.
    """
    loaders = {
        'abf': load_abf_data,
        'neo': load_neo_data
    }
    if file_type in loaders:
        return loaders[file_type](file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

def load_abf_data(file_path):
    """Load action potential data from an ABF file using PyABF."""
    abf = pyabf.ABF(file_path)
    signal = abf.data[0]  # Assuming single-channel recording
    sampling_rate = abf.dataRate
    return signal, sampling_rate

def load_neo_data(file_path):
    """Load action potential data from a Neo-compatible file."""
    reader = neo.io.NeoHdf5IO(file_path)
    block = reader.read_block()
    segment = block.segments[0]
    signal = np.array(segment.analogsignals[0].magnitude).flatten()
    sampling_rate = segment.analogsignals[0].sampling_rate.magnitude
    return signal, sampling_rate

# Preprocessing Module
def preprocess_signal(signal, sampling_rate, detrend_signal=True, freq_min=1, freq_max=100):
    """Preprocess the loaded signal by detrending and bandpass filtering."""
    if detrend_signal:
        signal = detrend(signal)
    preprocessed_signal = bandpass_filter(signal, sampling_rate, freq_min, freq_max)
    logging.info("Signal preprocessed with bandpass filtering and detrending.")
    return preprocessed_signal

def bandpass_filter(signal, sampling_rate, freq_min, freq_max):
    """Apply a bandpass filter to the signal."""
    sos = butter(4, [freq_min, freq_max], btype='bandpass', fs=sampling_rate, output='sos')
    filtered_signal = sosfilt(sos, signal)
    return filtered_signal

# Spike Detection Module
def detect_action_potentials(signal, sampling_rate, method='threshold', **kwargs):
    """Detect action potentials using a specified detection method."""
    if method == 'threshold':
        threshold = kwargs.get('threshold', -30.0)
        return threshold_spike_detection(signal, sampling_rate, threshold)
    elif method == 'template_matching':
        template = kwargs.get('template')
        return template_matching_spike_detection(signal, template)
    elif method == 'wavelet':
        wavelet = kwargs.get('wavelet', 'db4')
        return wavelet_transform_spike_detection(signal, wavelet)
    elif method == 'machine_learning':
        model = kwargs.get('model')
        return ml_based_spike_detection(signal, model)
    else:
        raise NotImplementedError(f"Spike detection method '{method}' is not implemented.")

def threshold_spike_detection(signal, sampling_rate, threshold):
    """Spike detection using a threshold-based method."""
    spike_indices = find_peaks(-signal, height=abs(threshold))[0]
    spike_times = spike_indices / sampling_rate
    return spike_times

def template_matching_spike_detection(signal, template, sampling_rate, threshold=0.8):
    """
    Spike detection using template matching.
    
    Args:
    - signal (np.ndarray): Preprocessed signal data.
    - template (np.ndarray): Template waveform for matching.
    - sampling_rate (float): Sampling rate of the recording.
    - threshold (float): Cross-correlation threshold for spike detection.
    
    Returns:
    - spike_times (np.ndarray): Times of detected spikes.
    """
    # Normalize template and signal
    template = (template - np.mean(template)) / np.std(template)
    signal = (signal - np.mean(signal)) / np.std(signal)
    
    # Perform cross-correlation
    correlation = correlate(signal, template, mode='same')
    
    # Detect spikes where correlation exceeds the threshold
    spike_indices = np.where(correlation > threshold)[0]
    spike_times = np.unique(spike_indices) / sampling_rate
    
    return spike_times

def wavelet_transform_spike_detection(signal, sampling_rate, wavelet='db4', threshold=0.5):
    """
    Spike detection using wavelet transforms.
    
    Args:
    - signal (np.ndarray): Preprocessed signal data.
    - sampling_rate (float): Sampling rate of the recording.
    - wavelet (str): Type of wavelet to use ('db4' is common for spike detection).
    - threshold (float): Threshold for wavelet coefficients.
    
    Returns:
    - spike_times (np.ndarray): Times of detected spikes.
    """
    # Perform continuous wavelet transform
    coeffs, freqs = pywt.cwt(signal, scales=np.arange(1, 128), wavelet=wavelet)
    
    # Use absolute value of coefficients for spike detection
    power = np.abs(coeffs)
    
    # Identify peaks in wavelet power coefficients that exceed threshold
    spike_indices = np.where(power.max(axis=0) > threshold)[0]
    spike_times = spike_indices / sampling_rate
    
    return spike_times

def ml_based_spike_detection(signal, model, sampling_rate):
    """
    Spike detection using a pre-trained machine learning model.
    
    Args:
    - signal (np.ndarray): Preprocessed signal data.
    - model (sklearn model): Pre-trained machine learning model.
    - sampling_rate (float): Sampling rate of the recording.
    
    Returns:
    - spike_times (np.ndarray): Times of detected spikes.
    """
    # Feature extraction example (could be more sophisticated)
    window_size = int(0.01 * sampling_rate)  # 10 ms window
    features = [signal[i:i+window_size] for i in range(0, len(signal) - window_size, window_size)]
    
    # Predict spikes using the model
    predictions = model.predict(features)
    
    # Find spike times based on model predictions
    spike_indices = np.where(predictions == 1)[0] * window_size
    spike_times = spike_indices / sampling_rate
    
    return spike_times

# Advanced ISI Analysis Module: Expanded Implementations

def detect_bursts(spike_times, burst_isi_threshold=100):
    """
    Detect bursts in spike times using an interspike interval threshold.
    
    Args:
    - spike_times (np.ndarray): Times of detected spikes.
    - burst_isi_threshold (float): Maximum ISI in ms to be considered part of a burst.
    
    Returns:
    - burst_stats (dict): Dictionary containing burst statistics.
    """
    # Convert spike times to ISI
    isi_values = np.diff(spike_times) * 1000  # Convert to ms
    
    # Identify bursts based on ISI threshold
    burst_indices = np.where(isi_values <= burst_isi_threshold)[0]
    burst_start_times = spike_times[burst_indices]
    burst_durations = np.diff(burst_start_times)
    
    burst_count = len(burst_start_times)
    mean_burst_duration = np.mean(burst_durations) if burst_count > 0 else 0
    
    burst_stats = {'burst_count': burst_count, 'mean_burst_duration': mean_burst_duration}
    
    return burst_stats

def compute_refractory_period(spike_times):
    """
    Compute refractory period statistics from spike times.
    
    Args:
    - spike_times (np.ndarray): Times of detected spikes.
    
    Returns:
    - refractory_period_stats (dict): Dictionary containing refractory period statistics.
    """
    # Compute ISI and find the minimum ISI as refractory period estimate
    isi_values = np.diff(spike_times) * 1000  # Convert to ms
    min_refractory_period = np.min(isi_values) if len(isi_values) > 0 else 0
    std_dev_refractory_period = np.std(isi_values)
    
    refractory_period_stats = {
        'mean_refractory_period': min_refractory_period,
        'std_dev_refractory_period': std_dev_refractory_period
    }
    
    return refractory_period_stats

def compute_variability_metrics(spike_times):
    """
    Compute variability metrics such as CV2 and local variations.
    
    Args:
    - spike_times (np.ndarray): Times of detected spikes.
    
    Returns:
    - variability_metrics (dict): Dictionary containing variability metrics.
    """
    isi_values = isi(spike_times * pq.s).rescale('ms').magnitude  # Convert ISI to milliseconds
    cv2_value = np.mean(cv2(spike_times * pq.s))  # Coefficient of variation 2
    
    # Calculate local variation (Placeholder; can use more sophisticated methods)
    local_variation = np.std(np.diff(isi_values) / (isi_values[:-1] + isi_values[1:]))
    
    variability_metrics = {'CV2': cv2_value, 'local_variation': local_variation}
    
    return variability_metrics

# Visualization Module
def plot_action_potentials(signal, spike_times, sampling_rate, interactive=False):
    """Plot the action potential traces and detected spikes."""
    time_vector = np.arange(len(signal)) / sampling_rate
    spike_indices = (spike_times * sampling_rate).astype(int)

    if interactive:
        fig = px.line(x=time_vector, y=signal, labels={'x': 'Time (s)', 'y': 'Voltage (mV)'}, title='Action Potential Trace')
        fig.add_scatter(x=spike_times, y=signal[spike_indices], mode='markers', name='Detected Spikes')
        fig.show()
    else:
        plt.figure(figsize=(10, 4))
        plt.plot(time_vector, signal, color='b', label='Action Potential Trace')
        plt.scatter(spike_times, signal[spike_indices], color='r', label='Detected Spikes')
        plt.xlabel('Time (s)')
        plt.ylabel('Voltage (mV)')
        plt.title('Action Potential Trace with Detected Spikes')
        plt.legend()
        plt.show()

def plot_isi_histogram(isi_values, bins=30):
    """Plot histogram of Interspike Intervals (ISI)."""
    plt.figure(figsize=(8, 4))
    plt.hist(isi_values, bins=bins, color='skyblue', edgecolor='black')
    plt.xlabel('Interspike Interval (ms)')
    plt.ylabel('Frequency')
    plt.title('ISI Histogram')
    plt.show()

# Main function
def main(config_file):
    """Main function to perform action potential analysis."""
    # Load configuration
    config = load_config(config_file)
    
    # Step 1: Load Data
    data_config = config['data']
    signal, sampling_rate = load_data(data_config['file_path'], data_config['file_type'])
    
    # Step 2: Preprocess Data
    preproc_config = config['preprocessing']
    preprocessed_signal = preprocess_signal(signal, sampling_rate, detrend_signal=preproc_config['detrend_signal'],
                                            freq_min=preproc_config['freq_min'], freq_max=preproc_config['freq_max'])
    
    # Step 3: Detect Action Potentials
    detect_config = config['spike_detection']
    spike_times = detect_action_potentials(preprocessed_signal, sampling_rate, method=detect_config['method'],
                                           threshold=detect_config.get('threshold', -30.0))
    print("Detected Spike Times:", spike_times)
    
    # Step 4: Advanced ISI Analysis
    if config['analysis'].get('advanced_isi', False):
        isi_values = isi(spike_times * pq.s).rescale('ms')
        burst_stats, refractory_period_stats, variability_metrics = advanced_isi_analysis(spike_times)
        print("Computed ISI Values (ms):", isi_values)
        print("Burst Stats:", burst_stats)
        print("Refractory Period Stats:", refractory_period_stats)
        print("Variability Metrics:", variability_metrics)
    
    # Step 5: Visualize Results
    plot_action_potentials(preprocessed_signal, spike_times, sampling_rate, interactive=False)
    if config['analysis'].get('advanced_isi', False):
        plot_isi_histogram(isi_values)

if __name__ == "__main__":
    # Specify the configuration file path
    config_file = 'config_action_potential.yaml'  # Adjust path to your configuration file
    main(config_file)