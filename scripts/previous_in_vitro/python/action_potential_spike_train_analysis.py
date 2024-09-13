# action_potential_analysis.py

# Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import os

# Function to load electrophysiology data
def load_data(file_path):
    """
    Load electrophysiology data from a CSV file.

    Args:
        file_path (str): Path to the input data file.

    Returns:
        data (DataFrame): Loaded data as a Pandas DataFrame.

    Raises:
        FileNotFoundError: If the file is not found at the specified path.
        ValueError: If the data format is incorrect or missing columns.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    
    data = pd.read_csv(file_path)
    if 'Time' not in data.columns or 'Voltage' not in data.columns:
        raise ValueError("The input data must contain 'Time' and 'Voltage' columns.")
    
    return data

# Function to detect action potentials and analyze properties
def analyze_action_potentials(data, threshold=0):
    """
    Analyze action potential properties in electrophysiology data.

    Args:
        data (DataFrame): Electrophysiology data containing time and voltage columns.
        threshold (float): Voltage threshold for peak detection.

    Returns:
        ap_properties (DataFrame): DataFrame containing detected AP properties (e.g., amplitude, half-width).
    """
    time = data['Time'].values
    voltage = data['Voltage'].values
    
    # Detect action potentials (APs) using peak detection
    peaks, _ = find_peaks(voltage, height=threshold)

    # Calculate action potential properties
    amplitudes = voltage[peaks]
    half_widths = np.diff(peaks) * (time[1] - time[0])  # Rough estimate based on sample rate

    ap_properties = pd.DataFrame({
        'AP_Index': peaks,
        'Amplitude': amplitudes,
        'Half_Width': half_widths
    })

    return ap_properties

# Function to analyze spike train dynamics
def analyze_spike_train(data, bin_size=0.01):
    """
    Analyze spike train dynamics such as firing rate and interspike interval (ISI) distribution.

    Args:
        data (DataFrame): Electrophysiology data containing detected action potentials.
        bin_size (float): Bin size for calculating firing rate histogram (in seconds).

    Returns:
        firing_rate_hist (ndarray): Firing rate histogram.
        isi_distribution (ndarray): Interspike interval distribution.
    """
    spike_times = data['Time'].values[data['AP_Index'].values]
    
    # Calculate ISI (Interspike Interval)
    isi = np.diff(spike_times)

    # Calculate Firing Rate Histogram
    firing_rate_hist, bin_edges = np.histogram(spike_times, bins=np.arange(0, spike_times[-1] + bin_size, bin_size))
    
    return firing_rate_hist, isi

# Function to plot results
def plot_results(data, ap_properties, firing_rate_hist, isi):
    """
    Plot action potential properties, firing rate histogram, and ISI distribution.

    Args:
        data (DataFrame): Electrophysiology data.
        ap_properties (DataFrame): Detected action potential properties.
        firing_rate_hist (ndarray): Firing rate histogram.
        isi (ndarray): Interspike interval distribution.
    """
    # Plot raw data with detected APs
    plt.figure(figsize=(10, 4))
    plt.plot(data['Time'], data['Voltage'], label='Voltage Trace')
    plt.scatter(data['Time'][ap_properties['AP_Index']], ap_properties['Amplitude'], color='red', label='Detected APs')
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (mV)')
    plt.title('Action Potential Detection')
    plt.legend()
    plt.show()

    # Plot firing rate histogram
    plt.figure(figsize=(10, 4))
    plt.hist(firing_rate_hist, bins=50, color='blue', alpha=0.7)
    plt.xlabel('Firing Rate (Hz)')
    plt.ylabel('Count')
    plt.title('Firing Rate Histogram')
    plt.show()

    # Plot ISI distribution
    plt.figure(figsize=(10, 4))
    plt.hist(isi, bins=50, color='green', alpha=0.7)
    plt.xlabel('Interspike Interval (s)')
    plt.ylabel('Count')
    plt.title('Interspike Interval (ISI) Distribution')
    plt.show()

# Main function to run the analysis
if __name__ == "__main__":
    try:
        # Load the data
        data = load_data('../../data/action_potential_data.csv')  # Ensure the data file exists in the 'data/' directory

        # Perform AP analysis
        ap_properties = analyze_action_potentials(data, threshold=0)

        # Analyze spike train
        firing_rate_hist, isi = analyze_spike_train(ap_properties)

        # Plot the results
        plot_results(data, ap_properties, firing_rate_hist, isi)

    except Exception as e:
        print(f"An error occurred: {e}")