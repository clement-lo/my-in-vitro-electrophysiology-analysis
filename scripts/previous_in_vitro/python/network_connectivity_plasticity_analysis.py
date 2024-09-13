# network_connectivity_plasticity_analysis.py

# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy.optimize import curve_fit

# Function to simulate a random network connectivity
def simulate_network(n_neurons, connection_prob):
    """
    Simulate a random network connectivity using an Erdős-Rényi model.

    Args:
        n_neurons (int): Number of neurons (nodes) in the network.
        connection_prob (float): Probability of connection between any two neurons.

    Returns:
        G (Graph): A NetworkX graph object representing the network.
    """
    # Generate a random graph using Erdős-Rényi model
    G = nx.erdos_renyi_graph(n_neurons, connection_prob)
    return G

# Function to compute network connectivity metrics
def compute_connectivity_metrics(G):
    """
    Compute network connectivity metrics such as degree, clustering coefficient, and path length.

    Args:
        G (Graph): A NetworkX graph object representing the network.

    Returns:
        metrics (dict): Dictionary containing network metrics (degree, clustering coefficient, path length).
    """
    # Calculate degree distribution
    degree = dict(G.degree())
    avg_degree = np.mean(list(degree.values()))
    
    # Calculate clustering coefficient
    clustering_coeff = nx.average_clustering(G)
    
    # Calculate average shortest path length
    if nx.is_connected(G):
        avg_path_length = nx.average_shortest_path_length(G)
    else:
        avg_path_length = np.nan  # Not defined for disconnected graphs

    metrics = {
        'Average Degree': avg_degree,
        'Clustering Coefficient': clustering_coeff,
        'Average Path Length': avg_path_length
    }
    return metrics

# Function to simulate synaptic plasticity: LTP and LTD
def simulate_synaptic_plasticity(G, stim_node, model='LTP'):
    """
    Simulate synaptic plasticity (LTP or LTD) on a network by modifying edge weights.

    Args:
        G (Graph): A NetworkX graph object representing the network.
        stim_node (int): Node index where the stimulation is applied.
        model (str): Type of plasticity model ('LTP' for long-term potentiation, 'LTD' for long-term depression).

    Returns:
        G_plastic (Graph): Modified graph after simulating plasticity.
    """
    # Copy the graph to avoid modifying the original
    G_plastic = G.copy()

    # Modify the edge weights based on the type of plasticity
    for u, v, data in G_plastic.edges(data=True):
        if stim_node in [u, v]:
            if model == 'LTP':
                G_plastic[u][v]['weight'] = G_plastic[u][v].get('weight', 1) * 1.5  # Potentiate connection
            elif model == 'LTD':
                G_plastic[u][v]['weight'] = G_plastic[u][v].get('weight', 1) * 0.5  # Depress connection
    return G_plastic

# Function to visualize network connectivity and plasticity effects
def plot_network(G, title='Network Connectivity'):
    """
    Plot the network connectivity with node labels.

    Args:
        G (Graph): A NetworkX graph object representing the network.
        title (str): Title for the plot.
    """
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)
    plt.title(title)
    plt.show()

# Main function to run the network connectivity and plasticity analysis
if __name__ == "__main__":
    # Parameters for network simulation
    n_neurons = 10  # Number of neurons in the network
    connection_prob = 0.3  # Probability of connection between neurons
    stim_node = 0  # Node index for stimulation

    try:
        # Simulate a random network
        G = simulate_network(n_neurons, connection_prob)

        # Compute network connectivity metrics
        metrics = compute_connectivity_metrics(G)
        print("Network Connectivity Metrics:")
        for key, value in metrics.items():
            print(f"{key}: {value:.2f}")

        # Plot original network
        plot_network(G, title='Original Network Connectivity')

        # Simulate synaptic plasticity (LTP)
        G_ltp = simulate_synaptic_plasticity(G, stim_node, model='LTP')
        plot_network(G_ltp, title='Network with LTP')

        # Simulate synaptic plasticity (LTD)
        G_ltd = simulate_synaptic_plasticity(G, stim_node, model='LTD')
        plot_network(G_ltd, title='Network with LTD')

    except Exception as e:
        print(f"An error occurred during analysis: {e}")