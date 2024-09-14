# network_dynamics_analysis.py

# Import necessary libraries
import neo  # For handling Neo-compatible formats
import numpy as np  # For numerical operations
import scipy.sparse as sp  # For sparse matrix representation
import matplotlib.pyplot as plt  # For static visualization
import plotly.express as px  # For interactive visualization
import networkx as nx  # For graph construction and analysis
from scipy.optimize import minimize  # For parameter optimization
from cdlib import algorithms as cd  # For community detection algorithms
import logging  # For logging errors and debugging
import yaml  # For configuration management

# Configure logging
logging.basicConfig(level=logging.INFO)

# 1. Utility Functions
def log_exception(exception):
    logging.error(f"An error occurred: {exception}")

# 2. Data Loading and Preprocessing Module
def load_data(file_path):
    """
    Load data using Neo and convert to appropriate format for analysis.
    
    Args:
    - file_path (str): Path to the file containing raw data.
    
    Returns:
    - data (np.ndarray): Loaded data in NumPy array format.
    """
    try:
        reader = neo.io.NeoHdf5IO(file_path)
        block = reader.read_block()
        segment = block.segments[0]
        analog_signal = np.array(segment.analogsignals[0].magnitude).flatten()
        return analog_signal
    except Exception as e:
        log_exception(e)
        raise ValueError("Failed to load data. Check file format and path.")

def preprocess_data(data, threshold=0.5, normalize=True):
    """
    Preprocess the data by normalizing and thresholding.
    
    Args:
    - data (np.ndarray): Raw data array.
    - threshold (float): Threshold for preprocessing.
    - normalize (bool): Whether to normalize the data.
    
    Returns:
    - processed_data (sp.csr_matrix): Preprocessed data in sparse matrix format.
    """
    try:
        if normalize:
            data = (data - np.mean(data)) / np.std(data)
        sparse_data = sp.csr_matrix(data > threshold)
        return sparse_data
    except Exception as e:
        log_exception(e)
        raise

# 3. Network Construction Module
def construct_connectivity_matrix(data, method='correlation', threshold=0.5):
    """
    Construct a connectivity matrix using pairwise correlations or other methods.
    
    Args:
    - data (np.ndarray): Preprocessed data.
    - method (str): Method for constructing connectivity ('correlation', 'covariance').
    - threshold (float): Threshold for determining connections.
    
    Returns:
    - connectivity_matrix (sp.csr_matrix): Sparse connectivity matrix.
    """
    try:
        if method == 'correlation':
            corr_matrix = np.corrcoef(data)
        elif method == 'covariance':
            corr_matrix = np.cov(data)
        else:
            raise ValueError("Invalid method. Choose 'correlation' or 'covariance'.")

        # Apply threshold and convert to sparse matrix
        sparse_matrix = sp.csr_matrix(corr_matrix > threshold)
        return sparse_matrix
    except Exception as e:
        log_exception(e)
        raise

# 4. Graph Construction and Analysis Module
def create_network(connectivity_matrix):
    """
    Create a network graph from the connectivity matrix.
    
    Args:
    - connectivity_matrix (sp.csr_matrix): Sparse connectivity matrix.
    
    Returns:
    - G (networkx.Graph): Constructed graph object.
    """
    try:
        G = nx.from_scipy_sparse_matrix(connectivity_matrix)
        return G
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
    try:
        metrics = {
            'degree': dict(nx.degree(G)),
            'betweenness': nx.betweenness_centrality(G),
            'closeness': nx.closeness_centrality(G)
        }
        return metrics
    except Exception as e:
        log_exception(e)
        raise

# 5. Community Detection Module
def detect_communities(G, method='louvain'):
    """
    Detect communities using different algorithms.
    
    Args:
    - G (networkx.Graph): Network graph.
    - method (str): Community detection method ('louvain', 'leiden', 'girvan_newman').
    
    Returns:
    - communities (list): List of detected communities.
    """
    try:
        if method == 'louvain':
            communities = cd.louvain(G)
        elif method == 'leiden':
            communities = cd.leiden(G)
        elif method == 'girvan_newman':
            communities = list(nx.community.girvan_newman(G))
        else:
            raise ValueError("Invalid method. Choose 'louvain', 'leiden', or 'girvan_newman'.")
        return communities
    except Exception as e:
        log_exception(e)
        raise

# 6. Parameter Optimization and Sensitivity Analysis Module
def optimize_parameters(data, objective_function, initial_guess):
    """
    Optimize parameters to improve network analysis.
    
    Args:
    - data (np.ndarray): Data used for optimization.
    - objective_function (callable): Objective function to minimize.
    - initial_guess (list): Initial guess for the parameters.
    
    Returns:
    - optimized_params (ndarray): Optimized parameters.
    """
    try:
        result = minimize(objective_function, initial_guess, args=(data,))
        return result.x
    except Exception as e:
        log_exception(e)
        raise

# 7. Visualization Module
def plot_network(G, communities=None):
    """
    Plot the network graph and highlight communities if provided.
    
    Args:
    - G (networkx.Graph): Network graph.
    - communities (list): List of detected communities (optional).
    """
    try:
        pos = nx.spring_layout(G)
        plt.figure(figsize=(10, 8))
        nx.draw(G, pos, node_color='skyblue', edge_color='gray', with_labels=True)
        
        if communities:
            for community in communities:
                nx.draw_networkx_nodes(G, pos, nodelist=community, node_color=np.random.rand(3,))
        
        plt.title("Network Graph with Community Structure")
        plt.show()
    except Exception as e:
        log_exception(e)
        raise

def plot_graph_metrics(metrics):
    """
    Plot histograms of graph metrics using Plotly.
    
    Args:
    - metrics (dict): Dictionary of graph metrics.
    """
    try:
        for metric_name, metric_values in metrics.items():
            fig = px.histogram(x=list(metric_values.values()), title=f"{metric_name.capitalize()} Distribution")
            fig.show()
    except Exception as e:
        log_exception(e)
        raise

# Main function
def main(config):
    """
    Main function to perform network dynamics analysis.
    
    Args:
    - config (dict): Configuration dictionary loaded from YAML file.
    """
    try:
        # Extract parameters from configuration
        file_path = config['data']['file_path']
        threshold = config['preprocessing']['threshold']
        normalize = config['preprocessing']['normalize']
        method = config['connectivity']['method']
        community_method = config['community_detection']['method']
        
        # Step 1: Load Data
        data = load_data(file_path)
        
        # Step 2: Preprocess Data
        processed_data = preprocess_data(data, threshold, normalize)
        
        # Step 3: Construct Connectivity Matrix
        connectivity_matrix = construct_connectivity_matrix(processed_data, method=method, threshold=threshold)
        
        # Step 4: Create Network Graph
        G = create_network(connectivity_matrix)
        
        # Step 5: Compute Graph Metrics
        metrics = compute_graph_metrics(G)
        print("Graph Metrics:", metrics)
        
        # Step 6: Detect Communities
        communities = detect_communities(G, method=community_method)
        print("Detected Communities:", communities)
        
        # Step 7: Visualize Results
        plot_network(G, communities)
        plot_graph_metrics(metrics)
    
    except Exception as e:
        log_exception(e)
        raise

if __name__ == "__main__":
    # Load configuration file
    with open('config_network_dynamics_analysis.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    # Run the main analysis pipeline using configuration parameters
    main(config)