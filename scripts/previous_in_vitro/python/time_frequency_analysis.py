# time_frequency_analysis.py

# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram, welch, coherence
from scipy import signal
import os

# Function to load electrophysiological data
def load_data(file_path):
    """
    Load electrophysiological data from a CSV file.
    
    Args:
        file_path (str): Path to the input data file.
    
    Returns:
        time (ndarray): Array of time points.
        voltage (ndarray): Array of voltage values corresponding to time points.
    
    Raises:
        FileNotFoundError: If the file is not found at the specified path.
        ValueError: If the data format is incorrect or missing columns.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    
    data = np.loadtxt(file_path, delimiter=',', skiprows=1)
    if data.shape[1] < 2:
        raise ValueError("The input data must contain at least two columns: Time and Voltage.")
    
    time = data[:, 0]
    voltage = data[:, 1]
    
    return time, voltage

# Function to compute and plot the power spectral density (PSD)
def plot_psd(time, voltage, fs):
    """
    Compute and plot the power spectral density (PSD) of the electrophysiological signal.

    Args:
        time (ndarray): Array of time points.
        voltage (ndarray): Array of voltage values corresponding to time points.
        fs (float): Sampling frequency of the data (in Hz).
    """
    f, Pxx = welch(voltage, fs=fs, nperseg=1024)
    plt.figure(figsize=(8, 6))
    plt.semilogy(f, Pxx)
    plt.title('Power Spectral Density (PSD)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power/Frequency (dB/Hz)')
    plt.grid(True)
    plt.show()

# Function to compute and plot the spectrogram
def plot_spectrogram(time, voltage, fs):
    """
    Compute and plot the spectrogram of the electrophysiological signal.

    Args:
        time (ndarray): Array of time points.
        voltage (ndarray): Array of voltage values corresponding to time points.
        fs (float): Sampling frequency of the data (in Hz).
    """
    f, t, Sxx = spectrogram(voltage, fs=fs, nperseg=256, noverlap=128)
    plt.figure(figsize=(10, 6))
    plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
    plt.title('Spectrogram')
    plt.ylabel('Frequency (Hz)')
    plt.xlabel('Time (s)')
    plt.colorbar(label='Power/Frequency (dB/Hz)')
    plt.show()

# Function to compute and plot coherence between two signals
def plot_coherence(time, voltage1, voltage2, fs):
    """
    Compute and plot the coherence between two electrophysiological signals.

    Args:
        time (ndarray): Array of time points.
        voltage1 (ndarray): Array of voltage values for the first signal.
        voltage2 (ndarray): Array of voltage values for the second signal.
        fs (float): Sampling frequency of the data (in Hz).
    """
    f, Cxy = coherence(voltage1, voltage2, fs=fs, nperseg=1024)
    plt.figure(figsize=(8, 6))
    plt.plot(f, Cxy)
    plt.title('Coherence between Two Signals')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Coherence')
    plt.grid(True)
    plt.show()

# Main function to run the time-frequency analysis
if __name__ == "__main__":
    # Define file path and sampling frequency
    file_path = '../data/intrinsic_oscillations_data.csv'  # Update this path as needed
    fs = 1000  # Sampling frequency in Hz
    
    try:
        # Load the data
        time, voltage = load_data(file_path)
        print("Data loaded successfully.")

        # Plot Power Spectral Density (PSD)
        plot_psd(time, voltage, fs)

        # Plot Spectrogram
        plot_spectrogram(time, voltage, fs)

        # Simulate another signal for coherence analysis (using filtered noise)
        voltage2 = signal.filtfilt(*signal.butter(4, [0.1, 0.4], btype='band'), np.random.normal(size=len(voltage)))

        # Plot Coherence between the original and simulated signals
        plot_coherence(time, voltage, voltage2, fs)

    except Exception as e:
        print(f"An error occurred during analysis: {e}")