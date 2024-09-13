# synaptic_input_output_analysis.py

# Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os

# Function to load data
def load_data(file_path):
    """
    Load synaptic input-output data from a CSV file.
    
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
    if 'Input' not in data.columns or 'Output' not in data.columns:
        raise ValueError("The input data must contain 'Input' and 'Output' columns.")
    
    return data

# Function to perform synaptic input-output analysis
def analyze_synaptic_io(data, model='sigmoid'):
    """
    Analyze synaptic input-output relationships using curve fitting.
    
    Args:
        data (DataFrame): Synaptic data containing input and output columns.
        model (str): The model to use for curve fitting ('sigmoid' or 'linear').
    
    Returns:
        popt (ndarray): Optimal parameters for the fitted curve.
        pcov (ndarray): Covariance of the parameters.
    """
    # Validate model type
    if model not in ['sigmoid', 'linear']:
        raise ValueError("Model must be 'sigmoid' or 'linear'.")
    
    # Define model functions
    def sigmoid(x, a, b, c):
        return c / (1 + np.exp(-(x - a) / b))

    def linear(x, m, c):
        return m * x + c

    # Select model for curve fitting
    input_data = data['Input'].values
    output_data = data['Output'].values
    if model == 'sigmoid':
        popt, pcov = curve_fit(sigmoid, input_data, output_data, p0=[0, 1, 1])
    else:
        popt, pcov = curve_fit(linear, input_data, output_data)

    return popt, pcov

# Function to plot the results
def plot_results(data, popt, model='sigmoid'):
    """
    Plot synaptic input-output data and the fitted curve.
    
    Args:
        data (DataFrame): Synaptic data containing input and output columns.
        popt (ndarray): Optimal parameters for the fitted curve.
        model (str): The model used for curve fitting ('sigmoid' or 'linear').
    """
    # Define model functions for plotting
    def sigmoid(x, a, b, c):
        return c / (1 + np.exp(-(x - a) / b))

    def linear(x, m, c):
        return m * x + c

    # Plot data points
    plt.scatter(data['Input'], data['Output'], label='Data', color='blue')

    # Generate points for fitted curve
    x_fit = np.linspace(min(data['Input']), max(data['Input']), 100)
    y_fit = sigmoid(x_fit, *popt) if model == 'sigmoid' else linear(x_fit, *popt)

    # Plot fitted curve
    plt.plot(x_fit, y_fit, label=f'Fitted {model.capitalize()} Curve', color='red')
    plt.xlabel('Synaptic Input')
    plt.ylabel('Synaptic Output')
    plt.title('Synaptic Input-Output Analysis')
    plt.legend()
    plt.show()

# Main function to run the analysis
if __name__ == "__main__":
    try:
        # Load the data
        data = load_data('../../data/synaptic_io_data.csv')  # Ensure the data file exists in the 'data/' directory
        
        # Perform the analysis
        popt, pcov = analyze_synaptic_io(data, model='sigmoid')

        # Plot the results
        plot_results(data, popt, model='sigmoid')

    except Exception as e:
        print(f"An error occurred: {e}")