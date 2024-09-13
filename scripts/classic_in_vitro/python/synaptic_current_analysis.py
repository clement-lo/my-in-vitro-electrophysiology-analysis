# synaptic_current_analysis.py

# Import necessary libraries
import pyabf  # For handling ABF (Axon Binary Format) files
import neo  # For handling Neo-compatible formats
import numpy as np  # For numerical operations
import matplotlib.pyplot as plt  # For static visualization
import plotly.express as px  # For interactive visualization
from scipy.signal import detrend, butter, sosfilt, find_peaks  # For signal preprocessing and peak detection
from scipy.optimize import curve_fit  # For fitting functions to synaptic event kinetics
from scipy.stats import zscore  # For standardizing data
from elephant import signal_processing as sp  # For advanced signal processing

# 1. Data Loading Module
def load_data(file_path, file_type='abf'):
    """
    Load synaptic current data using appropriate loaders based on the file type.
    
    Args:
    - file_path (str): Path to the data file.
    - file_type (str): Type of file ('abf' or 'neo').
    
    Returns:
    - signal (np.ndarray): Loaded signal data.
    - sampling_rate (float): Sampling rate of the recording.
    """
    if file_type == 'abf':
        return load_abf_data(file_path)
    elif file_type == 'neo':
        return load_neo_data(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

def load_abf_data(file_path):
    """
    Load synaptic current data from an ABF file using PyABF.
    
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
    Load synaptic current data from a Neo-compatible file.
    
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
def preprocess_signal(signal, sampling_rate, detrend_signal=True, freq_min=1, freq_max=100, standardize=True):
    """
    Preprocess the loaded signal by detrending, bandpass filtering, and standardizing.
    
    Args:
    - signal (np.ndarray): Raw signal data.
    - sampling_rate (float): Sampling rate of the recording.
    - detrend_signal (bool): Whether to detrend the signal.
    - freq_min (float): Minimum frequency for bandpass filter.
    - freq_max (float): Maximum frequency for bandpass filter.
    - standardize (bool): Whether to standardize the signal.
    
    Returns:
    - preprocessed_signal (np.ndarray): Preprocessed signal.
    """
    if detrend_signal:
        signal = detrend(signal)
    sos = butter(4, [freq_min, freq_max], btype='bandpass', fs=sampling_rate, output='sos')
    preprocessed_signal = sosfilt(sos, signal)
    if standardize:
        preprocessed_signal = zscore(preprocessed_signal)
    return preprocessed_signal

# 3. Event Detection Module
def detect_synaptic_events(signal, sampling_rate, threshold=5.0, min_distance=0.005):
    """
    Detect synaptic events (e.g., EPSCs, IPSCs) using a threshold-based method with noise level estimation.
    
    Args:
    - signal (np.ndarray): Preprocessed signal data.
    - sampling_rate (float): Sampling rate of the recording.
    - threshold (float): Threshold for event detection in terms of standard deviations above mean.
    - min_distance (float): Minimum distance between events in seconds.
    
    Returns:
    - event_times (np.ndarray): Times of detected synaptic events.
    """
    mean_val = np.mean(signal)
    std_val = np.std(signal)
    peaks, _ = find_peaks(-signal, height=(mean_val + threshold * std_val), distance=int(min_distance * sampling_rate))
    event_times = peaks / sampling_rate  # Convert to time in seconds
    return event_times

# 4. Kinetic Analysis Module
def exponential_decay(t, A, tau, C):
    """
    Exponential decay function for fitting synaptic event kinetics.
    
    Args:
    - t (np.ndarray): Time vector.
    - A (float): Amplitude of the decay.
    - tau (float): Time constant of the decay.
    - C (float): Offset.
    
    Returns:
    - (np.ndarray): Exponential decay values.
    """
    return A * np.exp(-t / tau) + C

def fit_event_kinetics(event_times, signal, sampling_rate, window=0.05):
    """
    Fit decay kinetics of detected synaptic events using an exponential model.
    
    Args:
    - event_times (np.ndarray): Times of detected synaptic events.
    - signal (np.ndarray): Preprocessed signal data.
    - sampling_rate (float): Sampling rate of the recording.
    - window (float): Time window (in seconds) around each event to fit kinetics.
    
    Returns:
    - fitted_params (list): List of fitted parameters for each event.
    """
    fitted_params = []
    for event in event_times:
        start = int((event - window / 2) * sampling_rate)
        end = int((event + window / 2) * sampling_rate)
        if start < 0 or end >= len(signal):
            continue
        time_vector = np.arange(0, end - start) / sampling_rate
        event_signal = signal[start:end] - np.min(signal[start:end])
        try:
            params, _ = curve_fit(exponential_decay, time_vector, event_signal, p0=[1, 0.01, 0])
            fitted_params.append(params)
        except RuntimeError:
            continue
    return fitted_params

# 5. Visualization Module
def plot_synaptic_traces(signal, sampling_rate, interactive=False):
    """
    Plot the raw or preprocessed synaptic current traces.
    
    Args:
    - signal (np.ndarray): Signal data (raw or preprocessed).
    - sampling_rate (float): Sampling rate of the recording.
    - interactive (bool): Whether to use interactive plotting.
    """
    time_vector = np.arange(len(signal)) / sampling_rate
    if interactive:
        fig = px.line(x=time_vector, y=signal, labels={'x': 'Time (s)', 'y': 'Amplitude (pA)'}, title='Synaptic Current Trace')
        fig.show()
    else:
        plt.figure(figsize=(10, 4))
        plt.plot(time_vector, signal, color='b')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude (pA)')
        plt.title('Synaptic Current Trace')
        plt.show()

def plot_event_detection(signal, event_times, sampling_rate):
    """
    Plot detected synaptic events on the synaptic current traces.
    
    Args:
    - signal (np.ndarray): Preprocessed signal data.
    - event_times (np.ndarray): Times of detected synaptic events.
    - sampling_rate (float): Sampling rate of the recording.
    """
    time_vector = np.arange(len(signal)) / sampling_rate
    plt.figure(figsize=(10, 4))
    plt.plot(time_vector, signal, color='b', label='Synaptic Current')
    plt.scatter(event_times, signal[(event_times * sampling_rate).astype(int)], color='r', label='Detected Events')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude (pA)')
    plt.title('Synaptic Event Detection')
    plt.legend()
    plt.show()

# Main function
def main(file_path, file_type='abf'):
    """
    Main function to perform synaptic current analysis.
    
    Args:
    - file_path (str): Path to the data file.
    - file_type (str): Type of file ('abf' or 'neo'). Default is 'abf'.
    """
    # Step 1: Load Data
    signal, sampling_rate = load_data(file_path, file_type)
    
    # Step 2: Preprocess Data
    preprocessed_signal = preprocess_signal(signal, sampling_rate)
    
    # Step 3: Detect Synaptic Events
    event_times = detect_synaptic_events(preprocessed_signal, sampling_rate)
    print("Detected Synaptic Event Times:", event_times)
    
    # Step 4: Fit Kinetic Parameters
    fitted_params = fit_event_kinetics(event_times, preprocessed_signal, sampling_rate)
    print("Fitted Kinetic Parameters for Events:", fitted_params)
    
    # Step 5: Visualize Results
    plot_synaptic_traces(preprocessed_signal, sampling_rate, interactive=True)
    plot_event_detection(preprocessed_signal, event_times, sampling_rate)

if __name__ == "__main__":
    # Example file path for demonstration purposes
    example_file_path = 'data/example_data.abf'  # Adjust the path for your dataset
    main(example_file_path)