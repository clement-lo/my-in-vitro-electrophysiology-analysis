# My In Vitro Electrophysiology Analysis Repository

## Overview
This repository provides a comprehensive toolkit for analyzing in vitro electrophysiology data, focusing on both classic electrophysiology setups (e.g., single-channel recordings, patch-clamp data) and multi-electrode array (MEA) setups. It integrates well-established libraries like Neo, Elephant, OpenElectrophy, and PyABF, offering robust support for a wide range of data formats and advanced analytical methods. It is designed to support researchers and analysts in neuroscience with modular, flexible, and extensible tools for data analysis, visualization, and interpretation.

## Repository Structure
The repository is organized into the following directories to ensure modularity, clarity, and ease of navigation:
```plaintext
├── README.md                                     # Main documentation file
├── requirements.txt                              # Python dependencies for the project
├── data/                                         # Directory for storing raw and preprocessed data
├── results/                                      # Output directory for results from analyses
├── scripts/                                      # Main directory containing all the analysis scripts
│   ├── classic_in_vitro/                            # Directory for single-channel or limited-channel analyses
│   │   ├── python/                               # Python scripts for classic setup analyses
│   │   │   ├── spike_sorting_patch_clamp_analysis.py
│   │   │   ├── synaptic_current_analysis.py
│   │   │   ├── action_potential_analysis.py
│   │   ├── matlab/                               # MATLAB scripts for classic setup analyses
│   │   │   ├── spike_sorting_patch_clamp_analysis.m
│   │   │   ├── synaptic_current_analysis.m
│   │   │   ├── action_potential_analysis.m
│   │   ├── notebooks/                            # Jupyter Notebooks for classic setup analyses
│   │   │   ├── 01_Spike_Sorting_Patch_Clamp_Analysis.ipynb
│   │   │   ├── 02_Synaptic_Current_Analysis.ipynb
│   │   │   ├── 03_Action_Potential_Analysis.ipynb
│   ├── mea_in_vitro/                             # Directory for multi-electrode array analyses
│   │   ├── python/                               # Python scripts for MEA analyses
│   │   │   ├── advanced_spike_sorting_clustering.py
│   │   │   ├── connectivity_analysis.py
│   │   │   ├── pharmacological_modulation_analysis.py
│   │   │   ├── network_dynamics_analysis.py
│   │   ├── matlab/                               # MATLAB scripts for MEA analyses
│   │   │   ├── advanced_spike_sorting_clustering.m
│   │   │   ├── connectivity_analysis.m
│   │   │   ├── pharmacological_modulation_analysis.m
│   │   │   ├── network_dynamics_analysis.m
│   │   ├── notebooks/                            # Jupyter Notebooks for MEA analyses
│   │   │   ├── 01_Advanced_Spike_Sorting_Clustering.ipynb
│   │   │   ├── 02_Connectivity_Analysis.ipynb
│   │   │   ├── 03_Pharmacological_Modulation_Analysis.ipynb
│   │   │   ├── 04_Network_Dynamics_Analysis.ipynb
├── tests/                                        # Unit tests for the analysis scripts
│   ├── test_spike_sorting_patch_clamp_analysis.py
│   ├── test_synaptic_current_analysis.py
│   ├── test_action_potential_analysis.py
│   ├── test_advanced_spike_sorting_clustering.py
│   ├── test_connectivity_analysis.py
│   ├── test_pharmacological_modulation_analysis.py
│   ├── test_network_dynamics_analysis.py
├── examples/                                     # Example datasets and workflows
│   ├── example_data.abf
│   └── example_workflow.ipynb
├── CONTRIBUTING.md                               # Guidelines for contributing to the repository
└── LICENSE.md                                    # Licensing information
```
## Key Features

- Modular Codebase: Easy to extend and integrate new analysis methods.
- Python and MATLAB Compatibility: Scripts are provided in both Python and MATLAB for flexibility.
- Detailed Documentation: Step-by-step instructions for setting up and running each analysis.
- Comprehensive Examples: Jupyter Notebooks provided for interactive data exploration and visualization.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Installation](#installation)
3. [General Usage Guide](#usage-guide)
   - [Python Scripts (.py)](#python-scripts-py)
   - [Jupyter Notebooks (.ipynb)](#jupyter-notebooks-ipynb)
   - [MATLAB Scripts](#matlab-scripts)
4. [Data Formats and Handling](#4-data-formats-and-handling)   
5. [Analysis Types](#analysis-types)
5.1 [Classic Electrophysiology Setups](#classic-electrophysiology-setups)
   - [Spike Sorting](#spike-sorting)
   - [Synaptic Current Analysis](#synaptic-current-analysis)
   - [Action Potential Analysis](#action-potential-analysis)
5.2 [Multi-Electrode Array (MEA) Setups](#multi-electrode-array-mea-setups)
   - [Advanced Spike Sorting and Clustering](#advanced-spike-sorting-and-clustering)   
   - [Connectivity Analysis](#connectivity-analysis)
   - [Pharmacological Modulation Analysis](#pharmacological-modulation-analysis)
   - [Network Dynamics Analysis](#network-dynamics-analysis)   
6. [Modularity and Extensibility](#modularity-and-extensibility)
7. [Integration with established libraries](#integration-with-established-libraries)
8. [Code, Data Visualisation and Interactive Notebooks](#code-data-visualisation-and-interactive-notebooks)
9. [Unit Testing and Continuous Integration (CI)](#unit-testing-and-continuous-integration-ci)
10. [Example Datasets and Detailed Workflows](#10-example-datasets-and-detailed-workflows)
11. [License](#11-license)
12. [References](#references)

## 1. Getting Started

This section will guide you through setting up the repository on your local machine and understanding the fundamental steps to run analyses.

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.10 or higher
- Jupyter Notebook
- MATLAB (optional, for some analyses)
- Git (for version control)

## 2. Installation

To get started with this repository, follow the steps below:

1. **Clone the Repository**: Open Terminal (Mac) or Command Prompt (Windows), and run:

   ```bash
   git clone https://github.com/clement-lo/my-in-vitro-electrophysiology-analysis.git
   cd my-in-vitro-electrophysiology-analysis
   ```

2. **Create a Virtual Environment**:

   ```bash
   python3 -m venv env
   source env/bin/activate  # For Mac/Linux
   .\env\Scripts\activate  # For Windows
   ```

3. **Install Required Python Libraries**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation**:
   Run `python --version` and `pip list` to confirm Python and required packages are installed correctly.

## 3. Usage Guide

This repository provides tools for analyzing electrophysiological data using Python scripts, Jupyter Notebooks, and MATLAB. Follow the instructions below to understand how to use each type of script.

### Python Scripts (.py)

1. **Navigate to the Python Scripts Directory**:
   ```bash
   cd scripts/python
   ```
2. **Run a Script**:
   For example, to run a synaptic input-output analysis script:
   ```bash
   python synaptic_input_output_analysis.py
   ```
3. **View Output**: The output will be saved in the `results/` directory, and visualizations will be generated as PNG files.

#### Jupyter Notebooks (.ipynb)

1. **Start Jupyter Notebook**:
   ```bash
   jupyter notebook
   ```
2. **Open the Notebook**: Navigate to the `notebooks/` directory and open `Synaptic_Input_Output_Analysis.ipynb`.
3. **Run Cells**: Click "Run" for each cell sequentially or "Run All" from the "Cell" menu.

#### MATLAB Scripts

1. **Open MATLAB**.
2. **Navigate to the MATLAB Scripts Directory**: Use the "Current Folder" panel or type in the MATLAB command window:
   ```matlab
   cd('scripts/matlab')
   ```
3. **Run the Script**:
   ```matlab
   run('synaptic_input_output_analysis.m')
   ```
4. **View Output**: Plots and results will be displayed in the MATLAB environment.

## 4. Data Formats and Handling
This repository supports various data formats commonly used in in vitro electrophysiology research, including:

ABF (Axon Binary Format): Supported by libraries like PyABF for easy data handling.
Neo Data Format: Supported by libraries like Neo for standardized data handling.
MATLAB Files: For users with custom data formats, we provide functions to load and preprocess these data types.
Ensure your data is properly formatted and organized in the data/ directory before running any analysis.

## 5. Analysis Types
This repository is divided into two main types of analyses for in vitro electrophysiology:
### 5.1 Classic Electrophysiology Setups
Classic electrophysiology setups focus on single-channel recordings, such as patch-clamp recordings. These setups are common in traditional in vitro studies to capture single-neuron or synaptic activity.
#### a. Spike Sorting and Patch Clamp Analysis
- Objective: Detect and sort spikes from intracellular patch-clamp data and compute firing rates.
- Methods:
- - Spike Detection: Threshold-based approaches to detect spikes in intracellular signals.
- - Feature Extraction: Extract key features like spike amplitude and waveform shape for clustering.
- - Clustering Algorithms: Methods like K-means and Gaussian Mixture Models (GMM) for sorting spikes into units.
- Tools: Python, MATLAB, PyABF, OpenElectrophy.
- Outcome: Sorted spikes, firing rate histograms, raster plots.
#### b. Synaptic Current Analysis
- Objective: Analyze synaptic currents like excitatory postsynaptic currents (EPSCs) and inhibitory postsynaptic currents (IPSCs).
- Methods:
- - Peak Detection: Find peaks in synaptic currents.
- - Kinetic Analysis: Fit decay and rise times of synaptic events.
- Tools: Python, MATLAB, OpenElectrophy.
- Outcome: Synaptic current traces, kinetics plots.
#### c. Action Potential Analysis
- Objective: Analyze action potentials to study neuronal excitability and firing patterns.
- Methods:
- - Threshold Crossing: Detect action potentials based on a voltage threshold.
- - Interspike Interval (ISI) Analysis: Analyze the timing between consecutive spikes.
- Tools: Python, MATLAB, OpenElectrophy.
- Outcome: ISI histograms, action potential traces.

### 5.2. Multi-Electrode Array (MEA) Setups
Multi-electrode array (MEA) setups are designed for high-density recordings, allowing for more comprehensive analysis of network-level dynamics in vitro.
#### a. Advanced Spike Sorting and Clustering
- Objective: Perform advanced spike sorting and clustering for MEA recordings to analyze network activity.
- Methods:
- - Dimensionality Reduction Techniques: PCA, t-SNE, and UMAP for visualizing high-dimensional spike features.
- - Spike Clustering Algorithms: HDBSCAN, Kilosort, MountainSort for clustering spikes across electrodes.
- Tools: Python, MATLAB, SpikeInterface, Kilosort.
- Outcome: Clustered spikes, spike train cross-correlograms.
#### b. Connectivity Analysis
- Objective: Analyze functional connectivity between neurons recorded from MEA setups to understand network communication.
- Methods:
- - Cross-Correlation: Measure correlation between spike trains to infer connectivity.
- - Granger Causality: Identify directional interactions between neurons.
- Tools: Python, MATLAB, Elephant.
- Outcome: Connectivity matrices, causality graphs.
#### c. Pharmacological Modulation Analysis
- Objective: Assess the effect of pharmacological agents on neuronal activity.
- Methods:
- - Drug Application Protocols: Apply pharmacological agents and record responses.
- - Response Quantification: Measure changes in firing rates, synaptic currents.
- Tools: Python, MATLAB.
- Outcome: Dose-response curves, modulation plots.
#### d. Network Dynamics Analysis
- Objective: Model the brain as a network and analyze its structure, dynamics, and modular organization.
- Methods:
- - Graph Theory Metrics: Degree, betweenness, closeness centrality.
- - Community Detection Algorithms: Louvain, Leiden algorithms for detecting clusters in brain networks.
- Tools: Python, MATLAB, NetworkX.
- Outcome: Network graphs, community structures.

## 6. Modularity and Extensibility
The repository is designed to be modular, allowing for easy extension by adding new modules for specific analyses. Each type of analysis is encapsulated in its own script or function to enable reuse and extension. Contributing new analysis modules or extending existing ones can be done by following the structure and guidelines provided.

## 7. Integration with Established Libraries
The repository integrates popular libraries such as:
- Neo: For standardized data handling and storage.
- Elephant: For advanced time-frequency analysis and spike train analysis.
- OpenElectrophy: For cellular-level data analysis and handling.
- PyABF: For handling Axon Binary Format (ABF) files commonly used in patch-clamp recordings.

## 8. Code, Data Visualization and Interactive Notebooks
This repository provides Jupyter Notebooks for each analysis type, offering step-by-step guidance and interactive visualizations. Notebooks allow users to explore data interactively, modify parameters, and visualize results dynamically.

## 9. Unit Testing and Continuous Integration (CI)
Unit tests are provided for each analysis script to ensure robustness and reliability. We recommend using GitHub Actions for Continuous Integration (CI) to run these tests automatically upon code updates.

## 10. Example Datasets and Detailed Workflows
Example datasets and workflows are included to guide users through data preprocessing, analysis, and interpretation. These examples are located in the examples/ directory and provide end-to-end tutorials for various analyses.

## 11. License
This repository is available under a dual-license model:

1. **Academic Use License - GNU General Public License v3.0 (GPL-3.0):**

   - The code in this repository is available for academic, research, and educational purposes under the GNU General Public License v3.0. This license allows you to use, modify, and distribute the code, provided that any derivative works are also licensed under the GPL-3.0.

2. **Commercial License:**

   - For companies, organizations, or individuals seeking to use this code in proprietary software or for commercial purposes, a separate commercial license is required. This license allows the use of the code without the restrictions of the GPL, including the ability to keep derivative works closed-source.

   If you are interested in obtaining a commercial license, please contact me to discuss further

# References
- [Neo](https://neo.readthedocs.io/en/latest/)
- [Elephant](https://elephant.readthedocs.io/en/latest/)
- [OpenElectrophy](https://open-ephys.github.io/analysis-tools/)
- [PyABF](https://github.com/swharden/pyabf)
- [Kilosort](https://github.com/MouseLand/Kilosort)
- [NetworkX](https://networkx.org/)