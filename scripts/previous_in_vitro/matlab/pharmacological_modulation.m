% pharmacological_modulation_analysis.m

% MATLAB Script for Pharmacological Modulation Analysis Using Dose-Response Curves

%% Function to Simulate Dose-Response Data
function responses = simulate_dose_response(doses, ec50, hill_coefficient, response_max)
    % Simulate dose-response data using a sigmoidal model.
    % Args:
    %     doses (array): Array of drug concentrations (in µM).
    %     ec50 (double): Concentration of the drug that gives half-maximal response (in µM).
    %     hill_coefficient (double): Hill coefficient that describes the slope of the dose-response curve.
    %     response_max (double): Maximum possible response.
    % Returns:
    %     responses (array): Simulated response values for each concentration in doses.

    responses = response_max * (doses .^ hill_coefficient) ./ (ec50 ^ hill_coefficient + doses .^ hill_coefficient);
end

%% Function to Fit Dose-Response Data to a Sigmoidal Curve
function [popt, gof] = fit_dose_response(doses, responses)
    % Fit dose-response data to a sigmoidal model to determine EC50 and Hill coefficient.
    % Args:
    %     doses (array): Array of drug concentrations (in µM).
    %     responses (array): Observed response values for each concentration in doses.
    % Returns:
    %     popt (array): Optimal parameters (EC50, Hill coefficient, and maximum response).
    %     gof (struct): Goodness of fit structure.

    % Sigmoidal model function for curve fitting
    sigmoid = @(p, dose) p(3) * (dose .^ p(2)) ./ (p(1) ^ p(2) + dose .^ p(2));

    % Initial parameter guesses for curve fitting
    initial_guess = [median(doses), 1, max(responses)];

    % Perform curve fitting using non-linear least squares
    [popt, ~, ~, ~, gof] = nlinfit(doses, responses, @(p, dose) sigmoid(p, dose), initial_guess);
end

%% Function to Plot Dose-Response Curve
function plot_dose_response(doses, responses, popt)
    % Plot the dose-response curve and fitted sigmoidal model.
    % Args:
    %     doses (array): Array of drug concentrations (in µM).
    %     responses (array): Observed response values for each concentration in doses.
    %     popt (array): Optimal parameters from curve fitting (EC50, Hill coefficient, maximum response).

    % Generate fine doses for plotting the fitted curve
    doses_fine = logspace(log10(min(doses)), log10(max(doses)), 100);

    % Calculate the fitted response using the optimized parameters
    fitted_responses = popt(3) * (doses_fine .^ popt(2)) ./ (popt(1) ^ popt(2) + doses_fine .^ popt(2));

    % Plot the experimental data
    figure;
    scatter(doses, responses, 'filled', 'b', 'DisplayName', 'Observed Data');
    hold on;

    % Plot the fitted curve
    plot(doses_fine, fitted_responses, 'r-', 'LineWidth', 2, 'DisplayName', sprintf('Fitted Curve (EC50=%.2f µM)', popt(1)));
    set(gca, 'XScale', 'log');  % Set x-axis to log scale
    xlabel('Drug Concentration (µM)');
    ylabel('Response');
    title('Dose-Response Curve');
    legend('show');
    grid on;
    hold off;
end

%% Main Script to Run the Pharmacological Modulation Analysis
try
    % Define dose-response simulation parameters
    doses = [0.1, 0.3, 1, 3, 10, 30, 100];  % Drug concentrations (in µM)
    ec50 = 10;  % Half-maximal effective concentration (in µM)
    hill_coefficient = 1;  % Hill coefficient
    response_max = 100;  % Maximum response

    % Simulate dose-response data
    simulated_responses = simulate_dose_response(doses, ec50, hill_coefficient, response_max);

    % Fit the simulated data to a sigmoidal model
    [popt, gof] = fit_dose_response(doses, simulated_responses);

    % Plot the dose-response curve
    plot_dose_response(doses, simulated_responses, popt);

    % Display goodness of fit
    disp('Goodness of Fit:');
    disp(gof);

catch ME
    fprintf('An error occurred during analysis: %s\n', ME.message);
end