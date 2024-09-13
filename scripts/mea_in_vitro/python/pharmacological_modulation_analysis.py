# pharmacological_modulation_analysis.py

# Import necessary libraries
import logging
import pyabf  # For handling ABF (Axon Binary Format) files
import neo  # For handling Neo-compatible formats
import numpy as np  # For numerical operations
import matplotlib.pyplot as plt  # For static visualization
import plotly.express as px  # For interactive visualization
from scipy.signal import detrend, butter, sosfilt, find_peaks  # For signal preprocessing and peak detection
from scipy.optimize import curve_fit  # For fitting dose-response curves

# Configure logging for detailed output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Custom exceptions for specific errors
class DataLoadingError(Exception):
    """Custom exception for errors in loading data."""
    pass

class AnalysisError(Exception):
    """Custom exception for errors during data analysis."""
    pass

# 1. Data Loading Module
def load_data(file_path, file_type='abf'):
    """
    Load electrophysiological data using appropriate loaders based on the file type.
    
    Args:
    - file_path (str): Path to the data file (e.g., 'data/example_data.abf').
    - file_type (str): Type of file ('abf' or 'neo'). Supports ABF (Axon Binary Format) and Neo formats.
    
    Returns:
    - signal (np.ndarray): Loaded signal data as a NumPy array.
    - sampling_rate (float): Sampling rate of the recording in Hz.
    
    Raises:
    - DataLoadingError: If loading fails or the file type is unsupported.
    """
    if file_type == 'abf':
        try:
            abf = pyabf.ABF(file_path)
            signal = abf.data[0]  # Assuming single-channel recording
            sampling_rate = abf.dataRate
            logging.info(f"Loaded ABF data from {file_path} with sampling rate {sampling_rate} Hz.")
        except Exception as e:
            logging.error(f"Failed to load ABF file: {e}")
            raise DataLoadingError(f"Could not load ABF data from {file_path}.") from e
    elif file_type == 'neo':
        try:
            reader = neo.io.NeoHdf5IO(file_path)
            block = reader.read_block()
            segment = block.segments[0]
            signal = np.array(segment.analogsignals[0].magnitude).flatten()
            sampling_rate = segment.analogsignals[0].sampling_rate.magnitude
            logging.info(f"Loaded Neo data from {file_path} with sampling rate {sampling_rate} Hz.")
        except Exception as e:
            logging.error(f"Failed to load Neo file: {e}")
            raise DataLoadingError(f"Could not load Neo data from {file_path}.") from e
    else:
        logging.error(f"Unsupported file type: {file_type}.")
        raise DataLoadingError(f"Unsupported file type: {file_type}. Only 'abf' and 'neo' are supported.")
    
    validate_data(signal, sampling_rate)
    return signal, sampling_rate

def validate_data(signal, sampling_rate):
    """
    Validate the integrity and format of the loaded data.
    
    Args:
    - signal (np.ndarray): Loaded signal data.
    - sampling_rate (float): Sampling rate of the recording.
    
    Raises:
    - ValueError: If the data is not in the expected format or contains invalid values.
    """
    if not isinstance(signal, np.ndarray) or signal.ndim != 1:
        logging.error("Signal data must be a one-dimensional NumPy array.")
        raise ValueError("Signal data must be a one-dimensional NumPy array.")
    
    if not isinstance(sampling_rate, (int, float)) or sampling_rate <= 0:
        logging.error("Sampling rate must be a positive number.")
        raise ValueError("Sampling rate must be a positive number.")
    
    logging.info("Data validation passed. Signal and sampling rate are valid.")

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
    sos = butter(4, [freq_min, freq_max], btype='bandpass', fs=sampling_rate, output='sos')
    preprocessed_signal = sosfilt(sos, signal)
    logging.info("Signal preprocessed with bandpass filtering and detrending.")
    return preprocessed_signal

# 3. Response Analysis Module
def detect_firing_rate_change(signal, sampling_rate, baseline_period=(0, 10), drug_period=(10, 20)):
    """
    Detect changes in firing rates before and after drug application.
    
    Args:
    - signal (np.ndarray): Preprocessed signal data.
    - sampling_rate (float): Sampling rate of the recording.
    - baseline_period (tuple): Time window (start, end) in seconds for baseline period. Default is (0, 10).
    - drug_period (tuple): Time window (start, end) in seconds for drug application period. Default is (10, 20).
    
    Returns:
    - baseline_rate (float): Firing rate during baseline period.
    - drug_rate (float): Firing rate during drug period.
    """
    baseline_start, baseline_end = int(baseline_period[0] * sampling_rate), int(baseline_period[1] * sampling_rate)
    drug_start, drug_end = int(drug_period[0] * sampling_rate), int(drug_period[1] * sampling_rate)
    
    baseline_signal = signal[baseline_start:baseline_end]
    drug_signal = signal[drug_start:drug_end]
    
    # Calculate firing rates
    baseline_rate = len(find_peaks(baseline_signal)[0]) / (baseline_end - baseline_start) * sampling_rate
    drug_rate = len(find_peaks(drug_signal)[0]) / (drug_end - drug_start) * sampling_rate
    
    logging.info(f"Baseline firing rate: {baseline_rate:.2f} Hz, Drug period firing rate: {drug_rate:.2f} Hz.")
    
    return baseline_rate, drug_rate

# 4. Dose-Response Curve Fitting Module
def fit_dose_response(doses, responses):
    """
    Fit a dose-response curve using a sigmoidal function.
    
    Args:
    - doses (np.ndarray): Concentrations of the pharmacological agent.
    - responses (np.ndarray): Observed responses (e.g., firing rates).
    
    Returns:
    - popt (np.ndarray): Optimized parameters for the sigmoidal curve.
    - pcov (np.ndarray): Covariance matrix of the parameters.
    """
    def sigmoid(x, EC50, hill_slope, max_response):
        return max_response / (1 + (EC50 / x) ** hill_slope)

    try:
        popt, pcov = curve_fit(sigmoid, doses, responses, bounds=(0, [1000., 10., 100.]))
        logging.info("Successfully fitted dose-response curve.")
    except RuntimeError as e:
        logging.error(f"Failed to fit dose-response curve: {e}")
        raise AnalysisError("Curve fitting failed. Check your dose-response data.") from e
    
    return popt, pcov

# 5. Visualization Module
def plot_results(signal, sampling_rate, event_times=None, doses=None, responses=None, popt=None):
    """
    Visualize the pharmacological modulation analysis results.
    
    Args:
    - signal (np.ndarray): Preprocessed signal data.
    - sampling_rate (float): Sampling rate of the recording.
    - event_times (np.ndarray): Times of detected synaptic events. Default is None.
    - doses (np.ndarray): Drug concentrations. Default is None.
    - responses (np.ndarray): Observed responses. Default is None.
    - popt (np.ndarray): Parameters for the dose-response curve. Default is None.
    """
    # Plot raw signal with detected events
    time_vector = np.arange(len(signal)) / sampling_rate
    plt.figure(figsize=(10, 4))
    plt.plot(time_vector, signal, label='Preprocessed Signal')
    if event_times is not None:
        plt.scatter(event_times, signal[(event_times * sampling_rate).astype(int)], color='r', label='Detected Events')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Pharmacological Modulation Analysis')
    plt.legend()
    plt.show()

    # Plot dose-response curve
    if doses is not None and responses is not None and popt is not None:
        fig = px.scatter(x=doses, y=responses, labels={'x': 'Dose', 'y': 'Response'}, title='Dose-Response Curve')
        dose_range = np.linspace(min(doses), max(doses), 100)
        fig.add_trace(px.line(x=dose_range, y=sigmoid(dose_range, *popt), name='Fitted Curve').data[0])
        fig.show()

# Main function
def main(file_path, file_type='abf', doses=None, responses=None):
    """
    Main function to perform pharmacological modulation analysis.
    
    Args:
    - file_path (str): Path to the data file.
    - file_type (str): Type of file ('abf' or 'neo'). Default is 'abf'.
    - doses (np.ndarray): Concentrations of pharmacological agents. Default is None.
    - responses (np.ndarray): Observed responses. Default is None.
    """
    # Step 1: Load Data
    signal, sampling_rate = load_data(file_path, file_type)
    
    # Step 2: Preprocess Data
    preprocessed_signal = preprocess_signal(signal, sampling_rate)
    
    # Step 3: Detect Changes in Firing Rate
    baseline_rate, drug_rate = detect_firing_rate_change(preprocessed_signal, sampling_rate)
    
    # Step 4: Fit Dose-Response Curve (if doses and responses are provided)
    if doses is not None and responses is not None:
        popt, pcov = fit_dose_response(doses, responses)
        plot_results(preprocessed_signal, sampling_rate, doses=doses, responses=responses, popt=popt)
    else:
        plot_results(preprocessed_signal, sampling_rate)

if __name__ == "__main__":
    example_file_path = 'data/example_data.abf'  # Adjust the path for your dataset
    main(example_file_path)