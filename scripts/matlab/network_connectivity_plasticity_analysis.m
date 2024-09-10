% network_connectivity_plasticity_analysis.m

% MATLAB Script for Analyzing Network Connectivity and Synaptic Plasticity

%% Function to Simulate a Random Network Connectivity
function G = simulate_network(n_neurons, connection_prob)
    % Simulate a random network connectivity using an Erdős-Rényi model.
    % Args:
    %     n_neurons (int): Number of neurons (nodes) in the network.
    %     connection_prob (float): Probability of connection between any two neurons.
    % Returns:
    %     G (graph): A MATLAB graph object representing the network.

    % Generate a random adjacency matrix
    adjacency_matrix = rand(n_neurons) < connection_prob;
    adjacency_matrix = triu(adjacency_matrix, 1);  % Make the matrix upper triangular
    adjacency_matrix = adjacency_matrix + adjacency_matrix';  % Symmetrize the matrix

    % Create a graph object
    G = graph(adjacency_matrix);
end

%% Function to Compute Network Connectivity Metrics
function metrics = compute_connectivity_metrics(G)
    % Compute network connectivity metrics such as degree, clustering coefficient, and path length.
    % Args:
    %     G (graph): A MATLAB graph object representing the network.
    % Returns:
    %     metrics (struct): Structure containing network metrics (degree, clustering coefficient, path length).

    % Calculate degree distribution
    degrees = degree(G);
    avg_degree = mean(degrees);
    
    % Calculate clustering coefficient
    clustering_coeff = mean(clustering_coef_bu(full(adjacency(G))));

    % Calculate average shortest path length
    if isconnected(G)
        avg_path_length = mean(mean(distances(G)));
    else
        avg_path_length = NaN;  % Not defined for disconnected graphs
    end

    % Store metrics in a structure
    metrics.AverageDegree = avg_degree;
    metrics.ClusteringCoefficient = clustering_coeff;
    metrics.AveragePathLength = avg_path_length;
end

%% Function to Simulate Synaptic Plasticity: LTP and LTD
function G_plastic = simulate_synaptic_plasticity(G, stim_node, model)
    % Simulate synaptic plasticity (LTP or LTD) on a network by modifying edge weights.
    % Args:
    %     G (graph): A MATLAB graph object representing the network.
    %     stim_node (int): Node index where the stimulation is applied.
    %     model (char): Type of plasticity model ('LTP' for long-term potentiation, 'LTD' for long-term depression).
    % Returns:
    %     G_plastic (graph): Modified graph after simulating plasticity.

    % Copy the graph to avoid modifying the original
    G_plastic = G;

    % Modify the edge weights based on the type of plasticity
    for i = 1:numedges(G_plastic)
        edge_nodes = G_plastic.Edges.EndNodes(i, :);
        if ismember(stim_node, edge_nodes)
            if strcmp(model, 'LTP')
                G_plastic.Edges.Weight(i) = G_plastic.Edges.Weight(i) * 1.5;  % Potentiate connection
            elseif strcmp(model, 'LTD')
                G_plastic.Edges.Weight(i) = G_plastic.Edges.Weight(i) * 0.5;  % Depress connection
            end
        end
    end
end

%% Function to Visualize Network Connectivity and Plasticity Effects
function plot_network(G, title_str)
    % Plot the network connectivity with node labels.
    % Args:
    %     G (graph): A MATLAB graph object representing the network.
    %     title_str (char): Title for the plot.

    figure;
    plot(G, 'Layout', 'force', 'NodeColor', 'lightblue', 'EdgeColor', 'gray', ...
        'NodeLabel', {}, 'LineWidth', 1.5);
    title(title_str);
end

%% Main Script to Run the Network Connectivity and Plasticity Analysis
try
    % Parameters for network simulation
    n_neurons = 10;  % Number of neurons in the network
    connection_prob = 0.3;  % Probability of connection between neurons
    stim_node = 1;  % Node index for stimulation

    % Simulate a random network
    G = simulate_network(n_neurons, connection_prob);

    % Compute network connectivity metrics
    metrics = compute_connectivity_metrics(G);
    disp('Network Connectivity Metrics:');
    disp(metrics);

    % Plot original network
    plot_network(G, 'Original Network Connectivity');

    % Simulate synaptic plasticity (LTP)
    G_ltp = simulate_synaptic_plasticity(G, stim_node, 'LTP');
    plot_network(G_ltp, 'Network with LTP');

    % Simulate synaptic plasticity (LTD)
    G_ltd = simulate_synaptic_plasticity(G, stim_node, 'LTD');
    plot_network(G_ltd, 'Network with LTD');

catch ME
    fprintf('An error occurred during analysis: %s\n', ME.message);
end