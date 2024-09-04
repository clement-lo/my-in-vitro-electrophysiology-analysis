 In Vitro Electrophysiology Data Analysis

This repository contains Python and MATLAB code for processing and analyzing **in vitro electrophysiology datasets**. The project showcases a robust and automated pipeline for data preprocessing, feature extraction, and various types of electrophysiological data analyses tailored to the study of neural activity.

## Overview

**In vitro electrophysiology** involves recording the electrical properties of neurons in a controlled environment, such as in brain slices or cultured cells. This repository provides a comprehensive analysis workflow with a focus on reproducibility, modularity, and clarity. The analyses covered in this repository include:

1. **Synaptic Input and Output Analysis**
2. **Action Potential Properties and Spike Train Analysis**
3. **Ion Channel Kinetics and Conductance-Based Modeling**
4. **Pharmacological Modulation Analysis**
5. **Network Connectivity and Plasticity Analysis**
6. **Time-Frequency Analysis for Intrinsic Oscillations**

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

- **Python** (>=3.8) and **MATLAB** (with Signal Processing Toolbox recommended)
- **VSCode** with **Python** and **Jupyter** extensions installed.

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
