# ion_channel_kinetics.py

# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os

# Function to simulate ion channel kinetics using Hodgkin-Huxley model
def simulate_ion_channel_kinetics(voltage_range, g_max, e_rev, model='hh'):
    """
    Simulate ion channel kinetics using conductance-based models.

    Args:
        voltage_range (ndarray): Array of membrane voltages (in mV) for the simulation.
        g_max (float): Maximum conductance of the ion channel (in µS).
        e_rev (float): Reversal potential of the ion channel (in mV).
        model (str): The model to use for simulation ('hh' for Hodgkin-Huxley).

    Returns:
        i_ion (ndarray): Simulated ionic currents for each voltage in voltage_range.
    """
    # Validate model type
    if model != 'hh':
        raise ValueError("Currently, only the Hodgkin-Huxley (hh) model is supported.")

    # Hodgkin-Huxley model parameters for sodium (Na) and potassium (K) channels
    def alpha_m(v): return 0.1 * (v + 40) / (1 - np.exp(-(v + 40) / 10))
    def beta_m(v): return 4 * np.exp(-(v + 65) / 18)
    def alpha_h(v): return 0.07 * np.exp(-(v + 65) / 20)
    def beta_h(v): return 1 / (1 + np.exp(-(v + 35) / 10))
    def alpha_n(v): return 0.01 * (v + 55) / (1 - np.exp(-(v + 55) / 10))
    def beta_n(v): return 0.125 * np.exp(-(v + 65) / 80)

    # Initialize variables for gating variables and current
    m = 0.05
    h = 0.6
    n = 0.32
    dt = 0.01  # Time step for simulation
    i_ion = np.zeros_like(voltage_range)

    # Simulate ionic current for each voltage in the range
    for i, v in enumerate(voltage_range):
        # Update gating variables
        m += dt * (alpha_m(v) * (1 - m) - beta_m(v) * m)
        h += dt * (alpha_h(v) * (1 - h) - beta_h(v) * h)
        n += dt * (alpha_n(v) * (1 - n) - beta_n(v) * n)

        # Calculate ionic current using Hodgkin-Huxley equations
        g_na = g_max * (m ** 3) * h  # Sodium conductance
        g_k = g_max * (n ** 4)       # Potassium conductance
        i_na = g_na * (v - e_rev)    # Sodium current
        i_k = g_k * (v - e_rev)      # Potassium current
        i_ion[i] = i_na + i_k

    return i_ion

# Function to plot the current-voltage (I-V) relationship
def plot_iv_curve(voltage_range, i_ion):
    """
    Plot the current-voltage (I-V) relationship for ion channel kinetics.

    Args:
        voltage_range (ndarray): Array of membrane voltages (in mV).
        i_ion (ndarray): Simulated ionic currents for each voltage in voltage_range.
    """
    plt.figure(figsize=(8, 6))
    plt.plot(voltage_range, i_ion, label='Ionic Current')
    plt.xlabel('Membrane Voltage (mV)')
    plt.ylabel('Ionic Current (µA)')
    plt.title('Current-Voltage (I-V) Relationship')
    plt.legend()
    plt.grid(True)
    plt.show()

# Function to calculate and plot conductance curves
def plot_conductance_curve(voltage_range, i_ion, g_max):
    """
    Plot the conductance curve for ion channel kinetics.

    Args:
        voltage_range (ndarray): Array of membrane voltages (in mV).
        i_ion (ndarray): Simulated ionic currents for each voltage in voltage_range.
        g_max (float): Maximum conductance of the ion channel (in µS).
    """
    conductance = i_ion / (voltage_range - e_rev)  # Conductance calculation
    plt.figure(figsize=(8, 6))
    plt.plot(voltage_range, conductance, label='Conductance (g)')
    plt.xlabel('Membrane Voltage (mV)')
    plt.ylabel('Conductance (µS)')
    plt.title('Conductance Curve')
    plt.legend()
    plt.grid(True)
    plt.show()

# Main function to run the analysis
if __name__ == "__main__":
    # Define simulation parameters
    voltage_range = np.arange(-80, 60, 1)  # Membrane voltage range (in mV)
    g_max = 120.0  # Maximum conductance (in µS)
    e_rev = -65.0  # Reversal potential (in mV)
    
    # Simulate ion channel kinetics
    try:
        i_ion = simulate_ion_channel_kinetics(voltage_range, g_max, e_rev, model='hh')
        
        # Plot I-V curve
        plot_iv_curve(voltage_range, i_ion)
        
        # Plot conductance curve
        plot_conductance_curve(voltage_range, i_ion, g_max)

    except Exception as e:
        print(f"An error occurred: {e}")
