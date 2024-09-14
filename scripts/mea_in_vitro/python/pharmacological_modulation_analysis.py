# pharmacological_modulation_analysis.py

import logging
import yaml  # For configuration management
import pyabf  # For handling ABF (Axon Binary Format) files
import neo  # For handling Neo-compatible formats
import spikeinterface as si  # For spike sorting and analysis
import spikeinterface.extractors as se  # For extracting data
import spikeinterface.preprocessing as sp  # For data preprocessing
import spikeinterface.sorters as ss  # For spike sorting algorithms
import spikeinterface.postprocessing as spost  # For postprocessing sorted data
import numpy as np  # For numerical operations
import matplotlib.pyplot as plt  # For static visualization
import plotly.express as px  # For interactive visualization
import quantities as pq  # For unit handling
from scipy.signal import detrend, butter, sosfilt, find_peaks  # For signal preprocessing and peak detection
from scipy.optimize import curve_fit  # For fitting dose-response curves
import networkx as nx  # For graph construction and analysis
from cdlib import algorithms as cd  # For community detection algorithms
from joblib import Parallel, delayed  # For parallel processing
from elephant.spike_train_correlation import corrcoef  # For cross-correlation analysis

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 1. Utility Functions Module
def load_config(config_file):
    """Load configuration settings from a YAML file."""
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        logging.info(f"Configuration loaded from {config_file}.")
        return config
    except Exception as e:
        logging.error(f"Failed to load configuration: {e}")
        raise

def log_exception(exception):
    logging.error(f"An error occurred: {exception}")

# 2. Data Loading and Validation Module
def load_data(file_path, file_type='abf'):
    """Load electrophysiological data using appropriate loaders based on the file type."""
    try:
        if file_type == 'abf':
            abf = pyabf.ABF(file_path)
            signal = abf.data[0]  # Assuming single-channel recording
            sampling_rate = abf.dataRate
            logging.info(f"Loaded ABF data from {file_path} with sampling rate {sampling_rate} Hz.")
        elif file_type == 'neo':
            reader = neo.io.NeoHdf5IO(file_path)
            block = reader.read_block()
            segment = block.segments[0]
            signal = np.array(segment.analogsignals[0].magnitude).flatten()
            sampling_rate = segment.analogsignals[0].sampling_rate.magnitude
            logging.info(f"Loaded Neo data from {file_path} with sampling rate {sampling_rate} Hz.")
        else:
            logging.error(f"Unsupported file type: {file_type}.")
            raise DataLoadingError(f"Unsupported file type: {file_type}. Only 'abf' and 'neo' are supported.")
        validate_data(signal, sampling_rate)
        return signal, sampling_rate
    except Exception as e:
        log_exception(e)
        raise

def validate_data(signal, sampling_rate):
    """Validate the integrity and format of the loaded data."""
    if not isinstance(signal, np.ndarray) or signal.ndim != 1:
        logging.error("Signal data must be a one-dimensional NumPy array.")
        raise ValueError("Signal data must be a one-dimensional NumPy array.")
    if not isinstance(sampling_rate, (int, float)) or sampling_rate <= 0:
        logging.error("Sampling rate must be a positive number.")
        raise ValueError("Sampling rate must be a positive number.")
    logging.info("Data validation passed. Signal and sampling rate are valid.")

# 3. Preprocessing Module
def preprocess_signal(signal, sampling_rate, detrend_signal=True, freq_min=1, freq_max=100):
    """Preprocess the loaded signal by detrending and bandpass filtering."""
    try:
        if detrend_signal:
            signal = detrend(signal)
        sos = butter(4, [freq_min, freq_max], btype='bandpass', fs=sampling_rate, output='sos')
        preprocessed_signal = sosfilt(sos, signal)
        logging.info("Signal preprocessed with bandpass filtering and detrending.")
        return preprocessed_signal
    except Exception as e:
        log_exception(e)
        raise

# 4. Spike Sorting Module
def sort_spikes(recording, sorter_name='kilosort2', gpu_available=False):
    """
    Perform spike sorting on the preprocessed data.
    
    Args:
    - recording (si.BaseRecording): Preprocessed recording data.
    - sorter_name (str): Name of the sorting algorithm to use (e.g., 'kilosort2').
    - gpu_available (bool): If True, use GPU acceleration if available.
    
    Returns:
    - sorting (si.BaseSorting): Sorted spike data.
    """
    try:
        sorter_params = ss.get_default_params(sorter_name)
        if gpu_available:
            sorter_params['gpu'] = True
        sorting = ss.run_sorter(sorter_name, recording, output_folder='sorting_output', **sorter_params)
        logging.info("Spike sorting completed.")
        return sorting
    except Exception as e:
        log_exception(e)
        raise

# 5. Spike Feature Extraction and Dimensionality Reduction Module
def extract_and_reduce_features(recording_preprocessed, sorting, method='pca', n_components=2):
    """
    Extract spike features and perform dimensionality reduction.
    
    Args:
    - recording_preprocessed (si.BaseRecording): Preprocessed recording data.
    - sorting (si.BaseSorting): Sorted spike data.
    - method (str): Dimensionality reduction method ('pca', 'tsne', 'umap').
    - n_components (int): Number of dimensions to reduce to.
    
    Returns:
    - reduced_features (np.ndarray): Dimensionality-reduced spike features.
    """
    try:
        # Extract waveforms
        waveform_extractor = spost.WaveformExtractor.create(recording_preprocessed, sorting, folder='waveforms', remove_existing_folder=True)
        waveform_extractor.set_params(ms_before=1.5, ms_after=2.5)
        waveform_extractor.run()
        features = waveform_extractor.get_all_features()
        
        # Dimensionality reduction
        if method == 'pca':
            reducer = skd.PCA(n_components=n_components)
        elif method == 'tsne':
            reducer = skm.TSNE(n_components=n_components)
        elif method == 'umap':
            reducer = umap.UMAP(n_components=n_components)
        else:
            raise ValueError("Invalid dimensionality reduction method.")
        reduced_features = reducer.fit_transform(features)
        logging.info(f"Dimensionality reduction using {method} completed.")
        return reduced_features
    except Exception as e:
        log_exception(e)
        raise

# 6. Clustering and Network Dynamics Module
def cluster_spikes(reduced_features, method='hdbscan'):
    """
    Cluster spikes using advanced clustering algorithms like HDBSCAN.
    
    Args:
    - reduced_features (np.ndarray): Dimensionality-reduced spike features.
    - method (str): Clustering method ('hdbscan').
    
    Returns:
    - labels (np.ndarray): Cluster labels for each spike.
    """
    try:
        clusterer = hdbscan.HDBSCAN(min_cluster_size=10)
        labels = clusterer.fit_predict(reduced_features)
        logging.info(f"Spike clustering using {method} completed.")
        return labels
    except Exception as e:
        log_exception(e)
        raise

def compute_graph_metrics(G):
    """
    Compute basic graph metrics like degree, betweenness, closeness centrality.
    
    Args:
    - G (networkx.Graph): Network graph.
    
    Returns:
    - metrics (dict): Computed graph metrics.
    """
    metrics = {
        'degree': dict(nx.degree(G)),
        'betweenness': nx.betweenness_centrality(G),
        'closeness': nx.closeness_centrality(G)
    }
    return metrics

# 7. Visualization Module
def plot_clusters(reduced_features, labels):
    """
    Plot clusters of spikes in 2D or 3D space.
    
    Args:
    - reduced_features (np.ndarray): Dimensionality-reduced spike features.
    - labels (np.ndarray): Cluster labels for each spike.
    """
    fig = px.scatter(x=reduced_features[:, 0], y=reduced_features[:, 1], color=labels.astype(str))
    fig.update_layout(title="Spike Clustering", xaxis_title="Component 1", yaxis_title="Component 2")
    fig.show()

# Main function to orchestrate the full analysis workflow
def main(config):
    """Main function to perform integrated analysis using configuration parameters."""
    try:
        # Load configuration parameters
        file_path = config['data']['file_path']
        file_type = config['data']['file_type']
        gpu_available = config['spike_sorting']['gpu_available']
        freq_min = config['preprocessing']['freq_min']
        freq_max = config['preprocessing']['freq_max']
        sorter_name = config['spike_sorting']['sorter_name']
        
        # Load and preprocess data
        signal, sampling_rate = load_data(file_path, file_type)
        preprocessed_signal = preprocess_signal(signal, sampling_rate, freq_min=freq_min, freq_max=freq_max)
        
        # Spike Sorting
        recording = si.BaseRecording(signal, sampling_rate)
        recording_preprocessed = preprocess_data(recording, freq_min, freq_max)
        sorting = sort_spikes(recording_preprocessed, sorter_name, gpu_available)
        
        # Spike Feature Extraction and Reduction
        reduced_features = extract_and_reduce_features(recording_preprocessed, sorting)
        
        # Clustering and Network Dynamics
        labels = cluster_spikes(reduced_features)
        G = create_network(connectivity_matrix)
        plot_clusters(reduced_features, labels)

        # Visualization and Result Presentation
        plot_network(G, communities)
        
    except Exception as e:
        log_exception(e)
        raise

if __name__ == "__main__":
    config = load_config('config_analysis.yaml')
    main(config)