# advanced_spike_sorting_clustering.py

# Import necessary libraries
import logging  # For logging
import yaml  # For loading YAML configuration files
import neo  # For data handling and loading
import spikeinterface as si  # Core module for SpikeInterface
import spikeinterface.extractors as se  # For extracting data
import spikeinterface.preprocessing as sp  # For data preprocessing
import spikeinterface.sorters as ss  # For spike sorting algorithms
import spikeinterface.postprocessing as spost  # For postprocessing sorted data
import spikeinterface.qualitymetrics as sq  # For quality control metrics
import sklearn.decomposition as skd  # For PCA
import sklearn.manifold as skm  # For t-SNE
import umap  # For UMAP dimensionality reduction
import hdbscan  # For HDBSCAN clustering
import matplotlib.pyplot as plt  # For static visualization
import plotly.express as px  # For interactive visualization
import elephant.spike_train_correlation as escorr  # For cross-correlograms
import quantities as pq  # For unit handling
import numpy as np  # For numerical operations
from scipy.optimize import minimize  # For parameter optimization
from joblib import Parallel, delayed  # For parallel processing
import datashader as ds  # For handling large-scale data visualizations
from datashader import transfer_functions as tf

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration from YAML file
with open('config_advanced_spike_sorting_clustering.yaml', 'r') as file:
    config = yaml.safe_load(file)

# 1. Utility Functions
def validate_data(data):
    if not isinstance(data, (np.ndarray, se.BaseRecording)):
        raise ValueError("Data must be a NumPy array or SpikeInterface BaseRecording.")
    return True

def log_exception(exception):
    logging.error(f"An error occurred: {exception}")

# 2. Data Loading and Validation Module
def load_mea_data(file_path):
    """
    Load MEA data using Neo and convert to SpikeInterface format.
    
    Args:
    - file_path (str): Path to the file containing raw data.
    
    Returns:
    - recording (si.BaseRecording): Loaded data in SpikeInterface's RecordingExtractor format.
    """
    try:
        reader = neo.io.Spike2IO(filename=file_path)
        block = reader.read_block()
        segment = block.segments[0]
        analog_signal = segment.analogsignals[0]
        recording = se.NeoRecordingExtractor(analog_signal)
        validate_data(recording)
        logging.info(f"Successfully loaded data from {file_path}")
        return recording
    except Exception as e:
        log_exception(e)
        raise

# 3. Preprocessing Module
def preprocess_data(recording, freq_min, freq_max, common_ref_type):
    """
    Preprocess the loaded data by applying bandpass filtering and common reference.
    
    Args:
    - recording (si.BaseRecording): Loaded data in SpikeInterface's RecordingExtractor format.
    - freq_min (int): Minimum frequency for bandpass filter.
    - freq_max (int): Maximum frequency for bandpass filter.
    - common_ref_type (str): Type of common reference ('median', 'average', etc.).
    
    Returns:
    - recording_preprocessed (si.BaseRecording): Preprocessed data.
    """
    try:
        recording_bp = sp.bandpass_filter(recording, freq_min=freq_min, freq_max=freq_max)
        recording_cmr = sp.common_reference(recording_bp, reference=common_ref_type)
        logging.info("Data preprocessing completed.")
        return recording_cmr
    except Exception as e:
        log_exception(e)
        raise

# 4. Spike Sorting Module with GPU Support and Optimization
def sort_spikes(recording, sorter_name, gpu_available):
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

# 5. Dimensionality Reduction Module
def reduce_dimensions(features, method='pca', n_components=2):
    """
    Perform dimensionality reduction on spike features.
    
    Args:
    - features (np.ndarray): High-dimensional spike features.
    - method (str): Reduction method ('pca', 'tsne', 'umap').
    - n_components (int): Number of dimensions to reduce to.
    
    Returns:
    - reduced_features (np.ndarray): Dimensionality-reduced features.
    """
    try:
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

# 6. Clustering Module
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

def plot_large_scale_visualization(reduced_features, labels):
    """
    Plot large-scale clusters using Datashader.
    """
    df = pd.DataFrame({
        'x': reduced_features[:, 0],
        'y': reduced_features[:, 1],
        'label': labels
    })
    cvs = ds.Canvas(plot_width=400, plot_height=400)
    agg = cvs.points(df, 'x', 'y', ds.count_cat('label'))
    img = tf.shade(agg, how='eq_hist')
    tf.set_background(img, 'black').to_pil().show()

# 8. Cross-Correlogram and Network Analysis Module
def compute_and_plot_correlograms(sorting):
    """
    Compute and plot cross-correlograms for sorted spike trains.
    
    Args:
    - sorting (si.BaseSorting): Sorted spike data.
    """
    try:
        spike_trains = [sorting.get_unit_spike_train(unit_id) * pq.s for unit_id in sorting.unit_ids]
        correlograms = escorr.corrcoef(spike_trains)
        plt.imshow(correlograms, cmap='viridis')
        plt.title('Cross-Correlograms')
        plt.colorbar()
        plt.show()
    except Exception as e:
        log_exception(e)
        raise

# Main function
def main(config):
    """
    Main function to perform advanced spike sorting and clustering analysis.
    
    Args:
    - config (dict): Configuration dictionary loaded from YAML file.
    """
    try:
        # Extract parameters from configuration
        file_path = config['data']['file_path']
        gpu_available = config['spike_sorting']['gpu_available']
        freq_min = config['preprocessing']['freq_min']
        freq_max = config['preprocessing']['freq_max']
        common_ref_type = config['preprocessing']['common_ref_type']
        sorter_name = config['spike_sorting']['sorter_name']
        ms_before = config['waveform_extraction']['ms_before']
        ms_after = config['waveform_extraction']['ms_after']
        reduction_method = config['dimensionality_reduction']['method']
        n_components = config['dimensionality_reduction']['n_components']
        clustering_method = config['clustering']['method']
        visualize_large_scale = config['visualization']['large_scale']

        # Step 1: Load Data
        recording = load_mea_data(file_path)
        
        # Step 2: Preprocess Data
        recording_preprocessed = preprocess_data(recording, freq_min, freq_max, common_ref_type)
        
        # Step 3: Perform Spike Sorting
        sorting = sort_spikes(recording_preprocessed, sorter_name, gpu_available)
        
        # Step 4: Extract Waveforms
        waveform_extractor = spost.WaveformExtractor.create(
            recording_preprocessed, sorting, folder='waveforms', remove_existing_folder=True
        )
        waveform_extractor.set_params(ms_before=ms_before, ms_after=ms_after)
        waveform_extractor.run()
        features = waveform_extractor.get_all_features()
        
        # Step 5: Dimensionality Reduction
        reduced_features = reduce_dimensions(features, method=reduction_method, n_components=n_components)
        
        # Step 6: Spike Clustering
        labels = cluster_spikes(reduced_features, method=clustering_method)
        
        # Step 7: Visualize Results
        plot_clusters(reduced_features, labels)
        if visualize_large_scale:
            plot_large_scale_visualization(reduced_features, labels)
        
        # Step 8: Compute and Plot Cross-Correlograms
        compute_and_plot_correlograms(sorting)
    
    except Exception as e:
        log_exception(e)
        raise

if __name__ == "__main__":
    # Load configuration file
    with open('config_advanced_spike_sorting_clustering.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    # Run the main analysis pipeline using configuration parameters
    main(config)