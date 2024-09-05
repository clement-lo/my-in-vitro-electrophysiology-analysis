# My In Vitro Electrophysiology Analysis Repository


## Overview
**In vitro electrophysiology** involves recording the electrical properties of neurons in a controlled environment, such as in brain slices or cultured cells. This repository provides a comprehensive analysis workflow with a focus on reproducibility, modularity, and clarity. The analysis pipelines contain Python scripts, Jupyter Notebooks, and MATLAB code for in vitro electrophysiology data analysis, particularly focusing on basic pain research. The code is modular and organized to perform a variety of analyses including synaptic input/output characterization, action potential properties, ion channel kinetics modeling, pharmacological modulation studies, network connectivity, and time-frequency analysis for intrinsic oscillations.


## Table of Contents
1. [Getting Started](#getting-started)
2. [Installation](#installation)
3. [Usage Guide](#usage-guide)
    - [Python Scripts (.py)](#python-scripts-py)
    - [Jupyter Notebooks (.ipynb)](#jupyter-notebooks-ipynb)
    - [MATLAB Scripts](#matlab-scripts)
4. [Analytical Functions Overview](#analytical-functions-overview)
    - [Synaptic Input and Output Analysis](#i-synaptic-input-and-output-analysis)
    - [Action Potential Properties and Spike Train Analysis](#ii-action-potential-properties-and-spike-train-analysis)
    - [Ion Channel Kinetics and Conductance-Based Modeling](#iii-ion-channel-kinetics-and-conductance-based-modeling)
    - [Pharmacological Modulation Analysis](#iv-pharmacological-modulation-analysis)
    - [Network Connectivity and Plasticity Analysis](#v-network-connectivity-and-plasticity-analysis)
    - [Time-Frequency Analysis for Intrinsic Oscillations](#vi-time-frequency-analysis-for-intrinsic-oscillations)
5. [Contributing](#contributing)
6. [License](#license)

## Getting Started

This section will guide you through setting up the repository on your local machine and understanding the fundamental steps to run analyses.

### Prerequisites

Ensure you have the following installed on your system:
- Python 3.8 or higher
- Jupyter Notebook
- MATLAB (optional, for some analyses)
- Git (for version control)

### Installation

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

### Usage Guide

This repository provides tools for analyzing electrophysiological data using Python scripts, Jupyter Notebooks, and MATLAB. Follow the instructions below to understand how to use each type of script.

#### Python Scripts (.py)

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

## Analytical Functions Overview
### 1. **Synaptic Input and Output Analysis**: 
Scripts and Notebooks for characterizing synaptic input/output curves, synaptic integration, and synaptic plasticity.
- Objective: Characterize synaptic input-output relationships.
- Methods: Curve fitting, response normalization, and plasticity induction protocols.
- Outputs: Input-output curves, synaptic strength indices.

### 2. **Action Potential Properties and Spike Train Analysis**:
Tools for extracting action potential properties such as amplitude, half-width, and spike-frequency adaptation. Includes spike train analysis methods like autocorrelation and burst detection.
- Objective: Quantify action potential waveform features and analyze spike train dynamics.
- Methods: Peak detection, inter-spike interval histogram, and bursting analysis.
- Outputs: Spike train raster plots, firing rate histograms.

### 3. **Ion Channel Kinetics and Conductance-Based Modeling**:
Scripts for modeling ion channel kinetics using Hodgkin-Huxley models or more advanced conductance-based models.
- Objective: Simulate and analyze ion channel kinetics and neuronal excitability.
- Methods: Hodgkin-Huxley and other conductance-based models.
- Outputs: Simulated action potentials, current-voltage relationships.

### 4. **Pharmacological Modulation Analysis**:
Analysis tools for assessing the effects of pharmacological agents on synaptic transmission and intrinsic membrane properties.
- Objective: Assess the effects of pharmacological agents on neurons.
- Methods: Dose-response curves, statistical significance testing.
- Outputs: Concentration-response curves, EC50 values.

### 5. **Network Connectivity and Plasticity Analysis**:
Functions for analyzing network connectivity using graph theory metrics, and for modeling synaptic plasticity phenomena (e.g., LTP/LTD).
- Objective: Analyze network connectivity and synaptic plasticity.
- Methods: Graph theory metrics, LTP/LTD induction protocols.
- Outputs: Network graphs, synaptic weight matrices.

### 6. **Time-Frequency Analysis for Intrinsic Oscillations**:
Wavelet and Fourier transform-based methods for analyzing intrinsic oscillations, including phase-amplitude coupling and coherence analysis.
- Objective: Characterize oscillatory activity and its modulation.
- Methods: Fourier and wavelet transforms, coherence analysis.
- Outputs: Time-frequency plots, phase-amplitude coupling indices.

## Key Features
- Modular Codebase: Easy to extend and integrate new analysis methods.
- Python and MATLAB Compatibility: Scripts are provided in both Python and MATLAB for flexibility.
- Detailed Documentation: Step-by-step instructions for setting up and running each analysis.
- Comprehensive Examples: Jupyter Notebooks provided for interactive data exploration and visualization.

## Repository Structure
The repository is organized as follows:
- `python/`: Python scripts for automated data processing and analysis.
- `matlab/`: MATLAB scripts for data processing and modeling.
- `notebooks/`: Jupyter notebooks providing step-by-step interactive analysis workflows.
- `data/`: Folder for storing raw and preprocessed datasets. (Excluded from version control using `.gitignore`)
- `results/`: Folder for saving analysis results, plots, and reports. (Excluded from version control using `.gitignore`)
- `tests/`: Unit tests to validate the functionality of key modules, ensuring code reliability.
- `LICENSE`: Licensing information for the repository.
- `AUTHORS`: List of contributors to the repository.
- `CITATION.cff`: Citation file to provide proper referencing for this repository.
- `.gitignore`: Specifies files and folders to be ignored by Git.
- `environment.yml`: Conda environment file listing all dependencies for a consistent setup.
- `requirements.txt`: Dependencies list for pip users.


## Getting Started

This project supports both Python and MATLAB for in vitro electrophysiology data analysis. Follow the steps below to set up your environment and run the analyses.

### Prerequisites

- **Python** (>=3.8) and **MATLAB** (with Signal Processing Toolbox, [... specify other toolboxes too] recommended)


### Data Requirements
This repository is designed to work with in vitro electrophysiology data typically recorded from patch-clamp or extracellular recordings. Ensure your data is in a standard format such as .abf, .mat, or .csv.
- Example Data Format: We recommend .csv format for importing and processing data in Python.
- Data Preprocessing: Raw data should be preprocessed (e.g., baseline subtraction, filtering) before analysis.


### Option 1: Installation Using Conda (Python)

1. **Clone the Repository**:
    ```bash

    git clone https://github.com/clement-lo/my-in-vitro-electrophysiology-analysis.git
    cd my-in-vitro-electrophysiology-analysis
    ```

2. **Set Up the Conda Environment**:
    ```bash
    conda env create -f environment.yml
    conda activate electrophysiology
    ```

3. **Run the Analysis Pipeline Using Python Scripts**:
    ```bash
    python python/example_analysis.py
    ```

### Option 2: Installation Using `venv` (Python)

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/clement-lo/my-in-vitro-electrophysiology-analysis.git
    cd my-in-vitro-electrophysiology-analysis
    ```

2. **Set Up the Virtual Environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Mac/Linux
    .venv\Scripts\activate     # On Windows
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Jupyter Notebook**:
    - Launch Jupyter Notebook and open `01_example_analysis.ipynb`:
    ```bash
    jupyter notebook
    ```

### Option 3: Running MATLAB Scripts

1. **Open MATLAB**:
   - Navigate to the `matlab/` folder in MATLAB.

2. **Run the MATLAB Script**:
   ```matlab
   synaptic_analysis

## Running the Analyses

### 1. **Synaptic Input and Output Analysis**
- **Python**: `python/synaptic_analysis.py`
- **Jupyter Notebook**: `notebooks/01_Synaptic_Analysis.ipynb`
- **MATLAB**: `matlab/synaptic_analysis.m`

### 2. **Action Potential Properties and Spike Train Analysis**
- **Python**: `python/spike_train_analysis.py`
- **Jupyter Notebook**: `notebooks/02_Spike_Train_Analysis.ipynb`
- **MATLAB**: `matlab/spike_train_analysis.m`

### 3. **Ion Channel Kinetics and Conductance-Based Modeling**
- **Python**: `python/ion_channel_kinetics.py`
- **Jupyter Notebook**: `notebooks/03_Ion_Channel_Kinetics.ipynb`
- **MATLAB**: `matlab/ion_channel_kinetics.m`

(Additional analyses are outlined similarly...)

## Contributing
We welcome contributions from the community! Please refer to our CONTRIBUTING.md file for guidelines on how to contribute to this repository.

## Licensing
This repository is available under a dual-license model:

1. **Academic Use License - GNU General Public License v3.0 (GPL-3.0):**
   - The code in this repository is available for academic, research, and educational purposes under the GNU General Public License v3.0. This license allows you to use, modify, and distribute the code, provided that any derivative works are also licensed under the GPL-3.0.

2. **Commercial License:**
   - For companies, organizations, or individuals seeking to use this code in proprietary software or for commercial purposes, a separate commercial license is required. This license allows the use of the code without the restrictions of the GPL, including the ability to keep derivative works closed-source.

   If you are interested in obtaining a commercial license, please contact me to discuss terms and pricing.

### Key Features of the Commercial License:

- No obligation to disclose source code modifications.
- Ability to use the code in closed-source projects.
- Custom support and maintenance options are available.
- Licensing fees and/or royalties apply.

### How to Apply for a Commercial License

To obtain a commercial license, please contact with the following information:

- Your name, company, and contact information.
- A brief description of how you intend to use the software.
- Any specific requirements or support needs you may have.

I will review your request and provide a quote and licensing agreement tailored to your needs.
