# action_potential_analysis.py

# Import necessary libraries
import pyabf  # For handling ABF (Axon Binary Format) files
import neo  # For handling Neo-compatible formats
import numpy as np  # For numerical operations
import matplotlib.pyplot as plt  # For static visualization
import plotly.express as px  # For interactive visualization
from scipy.signal import detrend, butter, sosfilt, find_peaks  # For signal preprocessing and spike detection
from elephant.statistics import isi  # For interspike interval analysis
import quantities as pq  # For handling physical quantities

# 1. Data Loading Module
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
    """
    Load action potential data from an ABF file using PyABF.
    
    Args:
    - file_path (str): Path to the ABF file.
    
    Returns:
    - signal (np.ndarray): Loaded signal data.
    - sampling_rate (float): Sampling rate of the recording.
    """
    abf = pyabf.ABF(file_path)
    signal = abf.data[0]  # Assuming single-channel recording
    sampling_rate = abf.dataRate
    return signal, sampling_rate

def load_neo_data(file_path):
    """
    Load action potential data from a Neo-compatible file.
    
    Args:
    - file_path (str): Path to the Neo file.
    
    Returns:
    - signal (np.ndarray): Loaded signal data.
    - sampling_rate (float): Sampling rate of the recording.
    """
    reader = neo.io.NeoHdf5IO(file_path)
    block = reader.read_block()
    segment = block.segments[0]
    signal = np.array(segment.analogsignals[0].magnitude).flatten()
    sampling_rate = segment.analogsignals[0].sampling_rate.magnitude
    return signal, sampling_rate

# 2. Preprocessing Module
def preprocess_signal(signal, sampling_rate, detrend_signal=True, freq_min=1, freq_max=100):
    """
    Preprocess the loaded signal by detrending and bandpass filtering.
    
    Args:
    - signal (np.ndarray): Raw signal data.
    - sampling_rate (float): Sampling rate of the recording.
    - detrend_signal (bool): Whether to detrend the signal.
    - freq_min (float): Minimum frequency for bandpass filter.
    - freq_max (float): Maximum frequency for bandpass filter.
    
    Returns:
    - preprocessed_signal (np.ndarray): Preprocessed signal.
    """
    if detrend_signal:
        signal = detrend(signal)
    preprocessed_signal = bandpass_filter(signal, sampling_rate, freq_min, freq_max)
    return preprocessed_signal

def bandpass_filter(signal, sampling_rate, freq_min, freq_max):
    """
    Apply a bandpass filter to the signal.
    
    Args:
    - signal (np.ndarray): Signal data.
    - sampling_rate (float): Sampling rate of the recording.
    - freq_min (float): Minimum frequency for bandpass filter.
    - freq_max (float): Maximum frequency for bandpass filter.
    
    Returns:
    - filtered_signal (np.ndarray): Filtered signal.
    """
    sos = butter(4, [freq_min, freq_max], btype='bandpass', fs=sampling_rate, output='sos')
    filtered_signal = sosfilt(sos, signal)
    return filtered_signal

# 3. Spike Detection Module
def detect_action_potentials(signal, sampling_rate, threshold=-30.0):
    """
    Detect action potentials using a voltage threshold-based method.
    
    Args:
    - signal (np.ndarray): Preprocessed signal data.
    - sampling_rate (float): Sampling rate of the recording.
    - threshold (float): Voltage threshold for spike detection in mV.
    
    Returns:
    - spike_times (np.ndarray): Times of detected spikes.
    """
    spike_indices = find_peaks(-signal, height=abs(threshold))[0]  # Detect threshold crossings using scipy
    spike_times = spike_indices / sampling_rate  # Convert to time in seconds
    return spike_times

# 4. Interspike Interval (ISI) Analysis Module
def compute_isi(spike_times):
    """
    Compute Interspike Intervals (ISI) from detected spikes.
    
    Args:
    - spike_times (np.ndarray): Times of detected spikes.
    
    Returns:
    - isi_values (np.ndarray): Interspike intervals.
    """
    isi_values = isi(spike_times * pq.s).rescale('ms')  # Compute ISI using Elephant
    return isi_values

def plot_isi_histogram(isi_values, bins=30):
    """
    Plot histogram of Interspike Intervals (ISI).
    
    Args:
    - isi_values (np.ndarray): Interspike intervals.
    - bins (int): Number of bins for histogram. Default is 30.
    """
    plt.figure(figsize=(8, 4))
    plt.hist(isi_values, bins=bins, color='skyblue', edgecolor='black')
    plt.xlabel('Interspike Interval (ms)')
    plt.ylabel('Frequency')
    plt.title('ISI Histogram')
    plt.show()

# 5. Visualization Module
def plot_action_potentials(signal, spike_times, sampling_rate, interactive=False):
    """
    Plot the action potential traces and detected spikes.
    
    Args:
    - signal (np.ndarray): Signal data (raw or preprocessed).
    - spike_times (np.ndarray): Times of detected spikes.
    - sampling_rate (float): Sampling rate of the recording.
    - interactive (bool): Whether to use interactive plotting.
    """
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

# Main function
def main(file_path, file_type='abf'):
    """
    Main function to perform action potential analysis.
    
    Args:
    - file_path (str): Path to the data file.
    - file_type (str): Type of file ('abf' or 'neo'). Default is 'abf'.
    """
    # Step 1: Load Data
    signal, sampling_rate = load_data(file_path, file_type)
    
    # Step 2: Preprocess Data
    preprocessed_signal = preprocess_signal(signal, sampling_rate)
    
    # Step 3: Detect Action Potentials
    spike_times = detect_action_potentials(preprocessed_signal, sampling_rate)
    print("Detected Spike Times:", spike_times)
    
    # Step 4: Compute ISI
    isi_values = compute_isi(spike_times)
    print("Computed ISI Values (ms):", isi_values)
    
    # Step 5: Visualize Results
    plot_action_potentials(preprocessed_signal, spike_times, sampling_rate, interactive=False)
    plot_isi_histogram(isi_values)

if __name__ == "__main__":
    # Example file path for demonstration purposes
    example_file_path = 'data/example_data.abf'  # Adjust the path for your dataset
    main(example_file_path)