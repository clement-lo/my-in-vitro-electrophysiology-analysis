# synaptic_input_output_analysis.py

# Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Function to load data
def load_data(file_path):
    """
    Load synaptic input-output data from a CSV file.
    
    Args:
        file_path (str): Path to the input data file.
    
    Returns:
        data (DataFrame): Loaded data as a Pandas DataFrame.
    """
    data = pd.read_csv(file_path)
    return data

# Function to perform synaptic input-output analysis
def analyze_synaptic_io(data):
    """
    Analyze synaptic input-output relationships using curve fitting.
    
    Args:
        data (DataFrame): Synaptic data containing input and output columns.
    
    Returns:
        popt (ndarray): Optimal parameters for the fitted curve.
        pcov (ndarray): Covariance of the parameters.
    """
    # Define a sigmoid function for curve fitting
    def sigmoid(x, a, b, c):
        return c / (1 + np.exp(-(x - a) / b))
    
    # Fit the sigmoid curve to the data
    input_data = data['Input'].values
    output_data = data['Output'].values
    popt, pcov = curve_fit(sigmoid, input_data, output_data, p0=[0, 1, 1])
    
    return popt, pcov

# Function to plot the results
def plot_results(data, popt):
    """
    Plot synaptic input-output data and the fitted curve.
    
    Args:
        data (DataFrame): Synaptic data containing input and output columns.
        popt (ndarray): Optimal parameters for the fitted curve.
    """
    # Define the sigmoid function again for plotting
    def sigmoid(x, a, b, c):
        return c / (1 + np.exp(-(x - a) / b))
    
    # Plot data points
    plt.scatter(data['Input'], data['Output'], label='Data', color='blue')
    
    # Generate points for fitted curve
    x_fit = np.linspace(min(data['Input']), max(data['Input']), 100)
    y_fit = sigmoid(x_fit, *popt)
    
    # Plot fitted curve
    plt.plot(x_fit, y_fit, label='Fitted Curve', color='red')
    plt.xlabel('Synaptic Input')
    plt.ylabel('Synaptic Output')
    plt.title('Synaptic Input-Output Analysis')
    plt.legend()
    plt.show()

# Main function to run the analysis
if __name__ == "__main__":
    # Load the data
    data = load_data('../../data/synaptic_io_data.csv')  # Ensure the data file exists in the 'data/' directory

    # Perform the analysis
    popt, pcov = analyze_synaptic_io(data)

    # Plot the results
    plot_results(data, popt)