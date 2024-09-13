# spike_sorting_patch_clamp_analysis.py

# Import necessary libraries
import neo  # For data handling and loading
import pyabf  # For handling ABF (Axon Binary Format) files
import numpy as np  # For numerical operations
import matplotlib.pyplot as plt  # For static visualization
import plotly.express as px  # For interactive visualization
import elephant.spike_train_generation as spkgen  # For spike train generation and analysis
import elephant.statistics as stats  # For statistical measures like firing rates
import scipy.signal as signal  # For filtering and preprocessing
from sklearn.cluster import KMeans  # For clustering spikes
from sklearn.mixture import GaussianMixture  # For Gaussian Mixture Models (GMM)

# 1. Data Loading Module

def load_abf_data(file_path):
    """
    Load patch-clamp data from an ABF file using PyABF.
    
    Args:
    - file_path (str): Path to the ABF file containing raw data.
    
    Returns:
    - signal (np.ndarray): Loaded signal data.
    - sampling_rate (float): Sampling rate of the recording.
    """
    try:
        abf = pyabf.ABF(file_path)
        signal = abf.data[0]  # Assuming single-channel recording
        sampling_rate = abf.dataRate
        return signal, sampling_rate
    except Exception as e:
        raise ValueError(f"Error loading ABF data from {file_path}: {e}")

def load_neo_data(file_path):
    """
    Load patch-clamp data from a Neo-compatible file.
    
    Args:
    - file_path (str): Path to the file containing raw data.
    
    Returns:
    - signal (np.ndarray): Loaded signal data.
    - sampling_rate (float): Sampling rate of the recording.
    """
    try:
        reader = neo.io.NeoHdf5IO(file_path)
        block = reader.read_block()
        segment = block.segments[0]
        signal = np.array(segment.analogsignals[0].magnitude).flatten()
        sampling_rate = segment.analogsignals[0].sampling_rate.magnitude
        return signal, sampling_rate
    except Exception as e:
        raise ValueError(f"Error loading Neo data from {file_path}: {e}")


# 2. Preprocessing Module
def bandpass_filter(signal, sampling_rate, freq_min=300, freq_max=3000):
    """
    Apply a bandpass filter to the signal.
    
    Args:
    - signal (np.ndarray): Raw signal data.
    - sampling_rate (float): Sampling rate of the recording.
    - freq_min (int): Minimum frequency for bandpass filter.
    - freq_max (int): Maximum frequency for bandpass filter.
    
    Returns:
    - filtered_signal (np.ndarray): Filtered signal.
    """
    if not isinstance(signal, np.ndarray):
        raise ValueError("Signal must be a NumPy array.")
    try:
        sos = signal.butter(4, [freq_min, freq_max], btype='bandpass', fs=sampling_rate, output='sos')
        filtered_signal = signal.sosfilt(sos, signal)
        return filtered_signal
    except Exception as e:
        raise RuntimeError(f"Error in signal preprocessing: {e}")


# 3. Spike Detection Module
def detect_spikes_threshold(signal, sampling_rate, threshold=5.0):
    """
    Detect spikes using a simple threshold-based method.
    
    Args:
    - signal (np.ndarray): Preprocessed signal data.
    - sampling_rate (float): Sampling rate of the recording.
    - threshold (float): Threshold for spike detection in terms of standard deviations above mean.
    
    Returns:
    - spike_times (np.ndarray): Times of detected spikes.
    """
    mean_val = np.mean(signal)
    std_val = np.std(signal)
    spikes = np.where(signal > (mean_val + threshold * std_val))[0]
    spike_times = spikes / sampling_rate  # Convert to time in seconds
    return spike_times

def detect_spikes_wavelet(signal, sampling_rate, wavelet='haar', threshold=0.5):
    """
    Detect spikes using wavelet transform for noise reduction and feature extraction.
    
    Args:
    - signal (np.ndarray): Preprocessed signal data.
    - sampling_rate (float): Sampling rate of the recording.
    - wavelet (str): Type of wavelet to use for transformation. Default is 'haar'.
    - threshold (float): Threshold for detecting spikes in wavelet coefficients.
    
    Returns:
    - spike_times (np.ndarray): Times of detected spikes.
    """
    coeffs = pywt.wavedec(signal, wavelet)
    # Thresholding coefficients
    sigma = np.median(np.abs(coeffs[-1])) / 0.6745
    uthresh = sigma * np.sqrt(2 * np.log(len(signal)))
    coeffs[1:] = (pywt.threshold(i, value=uthresh, mode='soft') for i in coeffs[1:])
    # Reconstruct signal and detect spikes
    reconstructed_signal = pywt.waverec(coeffs, wavelet)
    spike_times = detect_spikes_threshold(reconstructed_signal, sampling_rate, threshold=threshold)
    return spike_times

def detect_spikes_template_matching(signal, template, threshold=0.8):
    """
    Detect spikes using template matching.
    
    Args:
    - signal (np.ndarray): Preprocessed signal data.
    - template (np.ndarray): Template of the spike waveform to match against.
    - threshold (float): Correlation threshold to detect spikes.
    
    Returns:
    - spike_times (np.ndarray): Times of detected spikes.
    """
    correlation = signal.correlate(signal, template, mode='same')
    spike_indices = np.where(correlation > threshold * np.max(correlation))[0]
    spike_times = spike_indices / sampling_rate  # Convert to time in seconds
    return spike_times

# 4. Feature Extraction Module
def extract_spike_features(signal, spike_times, sampling_rate, window=30):
    """
    Extract features like spike width, amplitude, and waveform shape for clustering.
    
    Args:
    - signal (np.ndarray): Preprocessed signal data.
    - spike_times (np.ndarray): Times of detected spikes.
    - sampling_rate (float): Sampling rate of the recording.
    - window (int): Number of samples to extract around each spike for feature calculation.
    
    Returns:
    - features (np.ndarray): Extracted features.
    """
    if window <= 0:
        raise ValueError("Window size must be positive.")
    features = []
    for spike in spike_times:
        start = int(spike * sampling_rate) - window
        end = int(spike * sampling_rate) + window
        if start < 0 or end >= len(signal):
            continue
        waveform = signal[start:end]
        amplitude = np.max(waveform) - np.min(waveform)
        width = np.argmax(waveform) - np.argmin(waveform)
        features.append([amplitude, width])
    return np.array(features)

# 5. Spike Sorting and Clustering Module
def sort_spikes(features, method='kmeans', n_clusters=2):
    """
    Perform spike sorting using clustering algorithms like K-means or GMM.
    
    Args:
    - features (np.ndarray): Extracted spike features.
    - method (str): Clustering method ('kmeans' or 'gmm'). Default is 'kmeans'.
    - n_clusters (int): Number of clusters for sorting. Default is 2.
    
    Returns:
    - labels (np.ndarray): Cluster labels for each spike.
    """
    if method not in ['kmeans', 'gmm']:
        raise ValueError("Invalid method. Use 'kmeans' or 'gmm'.")
    if n_clusters <= 0:
        raise ValueError("Number of clusters must be positive.")
    if method == 'kmeans':
        model = KMeans(n_clusters=n_clusters)
    else:
        model = GaussianMixture(n_components=n_clusters)
    labels = model.fit_predict(features)
    return labels

# 6. Visualization Module
def plot_raster(spike_times):
    """
    Plot raster plot of the spike sorting results.
    
    Args:
    - spike_times (np.ndarray): Times of detected spikes.
    """
    plt.eventplot(spike_times, linelengths=0.8)
    plt.xlabel('Time (s)')
    plt.ylabel('Spike Events')
    plt.title('Raster Plot')
    plt.show()

def plot_firing_rate_histogram(spike_times, bin_size=0.1):
    """
    Plot histogram of firing rates using Matplotlib for visualization.
    
    Args:
    - spike_times (np.ndarray): Times of detected spikes.
    - bin_size (float): Bin size in seconds for histogram. Default is 0.1s.
    """
    bins = np.arange(0, max(spike_times), bin_size)
    hist, _ = np.histogram(spike_times, bins=bins)
    firing_rates = hist / bin_size
    plt.bar(bins[:-1], firing_rates, width=bin_size)
    plt.xlabel('Time (s)')
    plt.ylabel('Firing Rate (Hz)')
    plt.title('Firing Rate Histogram')
    plt.show()

# Main function
def main(file_path, file_type='abf'):
    """
    Main function to perform spike sorting and patch-clamp analysis.
    
    Args:
    - file_path (str): Path to the data file.
    - file_type (str): Type of file ('abf' or 'neo').
    """
    # Step 1: Load Data
    if file_type == 'abf':
        signal, sampling_rate = load_abf_data(file_path)
    elif file_type == 'neo':
        signal, sampling_rate = load_neo_data(file_path)
    else:
        raise ValueError("Invalid file type. Use 'abf' or 'neo'.")

    # Step 2: Preprocess Data
    filtered_signal = preprocess_signal(signal, sampling_rate)

    # Step 3: Detect Spikes
    spike_times = detect_spikes(filtered_signal, sampling_rate)
    print("Detected Spike Times:", spike_times)

    # Step 4: Extract Spike Features
    features = extract_spike_features(filtered_signal, spike_times, sampling_rate)
    print("Extracted Spike Features:", features)

    # Step 5: Sort Spikes
    labels = sort_spikes(features)
    print("Spike Sorting Labels:", labels)

    # Step 6: Visualize Results
    plot_raster(spike_times)
    plot_firing_rate_histogram(spike_times)

if __name__ == "__main__":
    # Example file path for demonstration purposes
    example_file_path = 'data/example_data.abf'  # Adjust the path for your dataset
    main(example_file_path, file_type='abf')
