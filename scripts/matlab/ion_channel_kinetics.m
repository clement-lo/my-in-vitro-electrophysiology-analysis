% ion_channel_kinetics.m

% MATLAB Script for Analyzing Ion Channel Kinetics Using Conductance-Based Models

%% Function to Simulate Ion Channel Kinetics Using Hodgkin-Huxley Model
function i_ion = simulate_ion_channel_kinetics(voltage_range, g_max, e_rev, model)
    % Simulate ion channel kinetics using conductance-based models (e.g., Hodgkin-Huxley).
    % Args:
    %     voltage_range (array): Array of membrane voltages (in mV) for the simulation.
    %     g_max (double): Maximum conductance of the ion channel (in µS).
    %     e_rev (double): Reversal potential of the ion channel (in mV).
    %     model (char): The model to use for simulation ('hh' for Hodgkin-Huxley).
    % Returns:
    %     i_ion (array): Simulated ionic currents for each voltage in voltage_range.

    % Validate model type
    if ~strcmp(model, 'hh')
        error('ValueError: Currently, only the Hodgkin-Huxley (hh) model is supported.');
    end

    % Hodgkin-Huxley model parameters for sodium (Na) and potassium (K) channels
    alpha_m = @(v) 0.1 * (v + 40) ./ (1 - exp(-(v + 40) / 10));
    beta_m = @(v) 4 * exp(-(v + 65) / 18);
    alpha_h = @(v) 0.07 * exp(-(v + 65) / 20);
    beta_h = @(v) 1 ./ (1 + exp(-(v + 35) / 10));
    alpha_n = @(v) 0.01 * (v + 55) ./ (1 - exp(-(v + 55) / 10));
    beta_n = @(v) 0.125 * exp(-(v + 65) / 80);

    % Initialize variables for gating variables and current
    m = 0.05;
    h = 0.6;
    n = 0.32;
    dt = 0.01;  % Time step for simulation
    i_ion = zeros(size(voltage_range));

    % Simulate ionic current for each voltage in the range
    for i = 1:length(voltage_range)
        v = voltage_range(i);
        
        % Update gating variables
        m = m + dt * (alpha_m(v) * (1 - m) - beta_m(v) * m);
        h = h + dt * (alpha_h(v) * (1 - h) - beta_h(v) * h);
        n = n + dt * (alpha_n(v) * (1 - n) - beta_n(v) * n);

        % Calculate ionic current using Hodgkin-Huxley equations
        g_na = g_max * (m^3) * h;  % Sodium conductance
        g_k = g_max * (n^4);       % Potassium conductance
        i_na = g_na * (v - e_rev); % Sodium current
        i_k = g_k * (v - e_rev);   % Potassium current
        i_ion(i) = i_na + i_k;
    end
end

%% Function to Plot the Current-Voltage (I-V) Relationship
function plot_iv_curve(voltage_range, i_ion)
    % Plot the current-voltage (I-V) relationship for ion channel kinetics.
    % Args:
    %     voltage_range (array): Array of membrane voltages (in mV).
    %     i_ion (array): Simulated ionic currents for each voltage in voltage_range.
    
    figure;
    plot(voltage_range, i_ion, 'LineWidth', 2);
    xlabel('Membrane Voltage (mV)');
    ylabel('Ionic Current (µA)');
    title('Current-Voltage (I-V) Relationship');
    grid on;
end

%% Function to Calculate and Plot Conductance Curves
function plot_conductance_curve(voltage_range, i_ion, e_rev)
    % Plot the conductance curve for ion channel kinetics.
    % Args:
    %     voltage_range (array): Array of membrane voltages (in mV).
    %     i_ion (array): Simulated ionic currents for each voltage in voltage_range.
    %     e_rev (double): Reversal potential of the ion channel (in mV).

    % Calculate conductance
    conductance = i_ion ./ (voltage_range - e_rev);  % Conductance calculation

    % Plot conductance curve
    figure;
    plot(voltage_range, conductance, 'LineWidth', 2);
    xlabel('Membrane Voltage (mV)');
    ylabel('Conductance (µS)');
    title('Conductance Curve');
    grid on;
end

%% Main Script to Run the Analysis
try
    % Define simulation parameters
    voltage_range = -80:1:60;  % Membrane voltage range (in mV)
    g_max = 120.0;  % Maximum conductance (in µS)
    e_rev = -65.0;  % Reversal potential (in mV)
    
    % Simulate ion channel kinetics
    i_ion = simulate_ion_channel_kinetics(voltage_range, g_max, e_rev, 'hh');
    
    % Plot I-V curve
    plot_iv_curve(voltage_range, i_ion);
    
    % Plot conductance curve
    plot_conductance_curve(voltage_range, i_ion, e_rev);

catch ME
    fprintf('An error occurred: %s\n', ME.message);
end