# connectivity_analysis.py

# Import necessary libraries
import neo  # For data handling
import elephant  # For advanced spike train analysis
import elephant.spike_train_correlation as escorr  # For cross-correlation analysis
import elephant.statistics as estat  # For statistical measures
import quantities as pq  # For unit handling
import matplotlib.pyplot as plt  # For static visualization
import plotly.express as px  # For interactive visualization
import numpy as np  # For numerical operations
import scipy.signal as signal  # For preprocessing
import statsmodels.api as sm  # For Granger causality analysis
import networkx as nx  # For network visualization
import logging  # For logging
from neo.io import Spike2IO  # Example IO for Neo data loading
from joblib import Parallel, delayed  # For parallel processing

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global configuration parameters
DEFAULT_MAX_LAG = 10
DEFAULT_BIN_SIZE = 5 * pq.ms
SIGNIFICANCE_LEVEL = 0.05

# 1. Data Loading Module
def load_data(file_path):
    """
    Load spike train data from an MEA recording using Neo.
    
    Args:
    - file_path (str): Path to the file containing raw data.
    
    Returns:
    - spike_trains (list): List of spike trains for each neuron.
    - sampling_rate (float): Sampling rate of the recording.
    
    Raises:
    - ValueError: If the file cannot be loaded or is not in the expected format.
    """
    try:
        reader = Spike2IO(filename=file_path)
        block = reader.read_block()
        segment = block.segments[0]
        spike_trains = [spiketrain.magnitude for spiketrain in segment.spiketrains]
        sampling_rate = segment.spiketrains[0].sampling_rate
        if not spike_trains:
            raise ValueError("No spike trains found in the data.")
        logging.info(f"Successfully loaded data from {file_path}")
        return spike_trains, sampling_rate
    except Exception as e:
        logging.error(f"Failed to load data: {e}")
        raise

# 2. Preprocessing Module
def preprocess_spike_trains(spike_trains, bin_size=DEFAULT_BIN_SIZE):
    """
    Preprocess spike trains by binning them to create binned spike trains.
    
    Args:
    - spike_trains (list): List of spike trains.
    - bin_size (Quantity): Bin size for creating binned spike trains.
    
    Returns:
    - binned_spike_trains (elephant.BinnedSpikeTrain): Binned spike trains.
    """
    try:
        if not spike_trains:
            raise ValueError("Empty spike train list provided.")
        binned_spike_trains = [estat.BinnedSpikeTrain(spiketrain, binsize=bin_size) for spiketrain in spike_trains]
        logging.info("Spike trains binned successfully.")
        return binned_spike_trains
    except Exception as e:
        logging.error(f"Failed to preprocess spike trains: {e}")
        raise

# 3. Cross-Correlation Analysis Module
def compute_cross_correlation(binned_spike_trains):
    """
    Compute cross-correlation between spike trains to infer connectivity.
    
    Args:
    - binned_spike_trains (list): List of binned spike trains.
    
    Returns:
    - cross_corr_matrix (np.ndarray): Cross-correlation matrix.
    """
    try:
        cross_corr_matrix = escorr.corrcoef(binned_spike_trains)
        logging.info("Cross-correlation computed successfully.")
        return cross_corr_matrix
    except Exception as e:
        logging.error(f"Failed to compute cross-correlation: {e}")
        raise

# 4. Granger Causality Analysis Module
def compute_granger_causality(spike_trains, max_lag=DEFAULT_MAX_LAG):
    """
    Compute Granger causality between neurons to infer directional interactions.
    
    Args:
    - spike_trains (list): List of spike trains.
    - max_lag (int): Maximum number of lags to test.
    
    Returns:
    - causality_matrix (np.ndarray): Granger causality matrix.
    """
    try:
        num_neurons = len(spike_trains)
        causality_matrix = np.zeros((num_neurons, num_neurons))
        
        # Parallel processing for efficiency
        def compute_granger_for_pair(i, j):
            if i != j:
                result = sm.tsa.stattools.grangercausalitytests(np.column_stack((spike_trains[i], spike_trains[j])), max_lag, verbose=False)
                return i, j, min([result[lag][0]['ssr_ftest'][1] for lag in range(1, max_lag+1)])
            return i, j, 1.0  # P-value of 1.0 indicates no causality
        
        results = Parallel(n_jobs=-1)(delayed(compute_granger_for_pair)(i, j) for i in range(num_neurons) for j in range(num_neurons))
        for i, j, p_value in results:
            causality_matrix[i, j] = p_value
        
        logging.info("Granger causality computed successfully.")
        return causality_matrix
    except Exception as e:
        logging.error(f"Failed to compute Granger causality: {e}")
        raise

# 5. Visualization Module
def plot_connectivity_matrix(matrix, title='Connectivity Matrix'):
    """
    Plot a connectivity matrix using matplotlib.
    
    Args:
    - matrix (np.ndarray): Connectivity matrix.
    - title (str): Title for the plot.
    """
    plt.figure(figsize=(8, 6))
    plt.imshow(matrix, cmap='hot', interpolation='nearest')
    plt.colorbar(label='Connectivity Strength')
    plt.title(title)
    plt.xlabel('Neuron Index')
    plt.ylabel('Neuron Index')
    plt.show()

def plot_causality_graph(causality_matrix, threshold=SIGNIFICANCE_LEVEL):
    """
    Plot a graph of Granger causality using NetworkX.
    
    Args:
    - causality_matrix (np.ndarray): Granger causality matrix.
    - threshold (float): Significance level for causality (p-value threshold).
    """
    try:
        G = nx.DiGraph()
        for i in range(causality_matrix.shape[0]):
            for j in range(causality_matrix.shape[1]):
                if causality_matrix[i, j] < threshold:
                    G.add_edge(i, j, weight=1 - causality_matrix[i, j])
        
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=12, font_weight="bold")
        nx.draw_networkx_edge_labels(G, pos, edge_labels={(i, j): f"{1-causality_matrix[i, j]:.2f}" for i, j in G.edges()}, font_color='red')
        plt.title('Granger Causality Graph')
        plt.show()
    except Exception as e:
        logging.error(f"Failed to plot causality graph: {e}")
        raise

# Main function
def main(file_path):
    """
    Main function to perform connectivity analysis on MEA data.
    
    Args:
    - file_path (str): Path to the data file.
    """
    try:
        # Step 1: Load Data
        spike_trains, sampling_rate = load_data(file_path)
        
        # Step 2: Preprocess Data
        binned_spike_trains = preprocess_spike_trains(spike_trains)
        
        # Step 3: Compute Cross-Correlation
        cross_corr_matrix = compute_cross_correlation(binned_spike_trains)
        
        # Step 4: Compute Granger Causality
        causality_matrix = compute_granger_causality(spike_trains)
        
        # Step 5: Visualize Results
        plot_connectivity_matrix(cross_corr_matrix, title='Cross-Correlation Matrix')
        plot_causality_graph(causality_matrix)
    
    except Exception as e:
        logging.error(f"An error occurred in the main function: {e}")
        raise

if __name__ == "__main__":
    # Example file path for demonstration purposes
    example_file_path = 'data/example_mea_data.smr'  # Adjust the path for your dataset
    main(example_file_path)
