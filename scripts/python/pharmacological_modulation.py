# pharmacological_modulation_analysis.py

# Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os

# Function to simulate dose-response data
def simulate_dose_response(doses, ec50, hill_coefficient, response_max):
    """
    Simulate dose-response data using a sigmoidal model.

    Args:
        doses (ndarray): Array of drug concentrations (in µM).
        ec50 (float): Concentration of the drug that gives half-maximal response (in µM).
        hill_coefficient (float): Hill coefficient that describes the slope of the dose-response curve.
        response_max (float): Maximum possible response.

    Returns:
        responses (ndarray): Simulated response values for each concentration in doses.
    """
    responses = response_max * (doses ** hill_coefficient) / (ec50 ** hill_coefficient + doses ** hill_coefficient)
    return responses

# Function to fit dose-response data to a sigmoidal curve
def fit_dose_response(doses, responses):
    """
    Fit dose-response data to a sigmoidal model to determine EC50 and Hill coefficient.

    Args:
        doses (ndarray): Array of drug concentrations (in µM).
        responses (ndarray): Observed response values for each concentration in doses.

    Returns:
        popt (ndarray): Optimal parameters (EC50, Hill coefficient, and maximum response).
        pcov (ndarray): Covariance of the parameters.
    """
    # Sigmoidal model function for curve fitting
    def sigmoid(dose, ec50, hill_coefficient, response_max):
        return response_max * (dose ** hill_coefficient) / (ec50 ** hill_coefficient + dose ** hill_coefficient)

    # Initial parameter guesses for curve fitting
    initial_guess = [np.median(doses), 1, max(responses)]

    # Perform curve fitting
    popt, pcov = curve_fit(sigmoid, doses, responses, p0=initial_guess)

    return popt, pcov

# Function to plot dose-response curve
def plot_dose_response(doses, responses, popt):
    """
    Plot the dose-response curve and fitted sigmoidal model.

    Args:
        doses (ndarray): Array of drug concentrations (in µM).
        responses (ndarray): Observed response values for each concentration in doses.
        popt (ndarray): Optimal parameters from curve fitting (EC50, Hill coefficient, maximum response).
    """
    # Generate fine doses for plotting the fitted curve
    doses_fine = np.logspace(np.log10(min(doses)), np.log10(max(doses)), 100)
    
    # Calculate the fitted response using the optimized parameters
    fitted_responses = popt[2] * (doses_fine ** popt[1]) / (popt[0] ** popt[1] + doses_fine ** popt[1])

    # Plot the experimental data
    plt.figure(figsize=(8, 6))
    plt.scatter(doses, responses, color='blue', label='Observed Data')
    
    # Plot the fitted curve
    plt.plot(doses_fine, fitted_responses, color='red', label=f'Fitted Curve (EC50={popt[0]:.2f} µM)')
    plt.xscale('log')
    plt.xlabel('Drug Concentration (µM)')
    plt.ylabel('Response')
    plt.title('Dose-Response Curve')
    plt.legend()
    plt.grid(True)
    plt.show()

# Main function to run the pharmacological modulation analysis
if __name__ == "__main__":
    # Define dose-response simulation parameters
    doses = np.array([0.1, 0.3, 1, 3, 10, 30, 100])  # Drug concentrations (in µM)
    ec50 = 10  # Half-maximal effective concentration (in µM)
    hill_coefficient = 1  # Hill coefficient
    response_max = 100  # Maximum response

    try:
        # Simulate dose-response data
        simulated_responses = simulate_dose_response(doses, ec50, hill_coefficient, response_max)
        
        # Fit the simulated data to a sigmoidal model
        popt, pcov = fit_dose_response(doses, simulated_responses)
        
        # Plot the dose-response curve
        plot_dose_response(doses, simulated_responses, popt)

    except Exception as e:
        print(f"An error occurred during analysis: {e}")
