# quantum_mitigation/regression.py

import numpy as np
from sklearn.linear_model import LinearRegression

def perform_regression(noisy_exp_vals, noiseless_exp_vals):
    """
        perform regression for the noisy and noiseless expectation values 

        parameters:
        - noisy_exp_vals (list): a list of all noisy expectation values 
        - noiseless_exp_vals (list): a list of all noiseless expectation values 

        returns:
        - modesl: the regression model for given data
    """
    # get the input values and reshape them into a column vector
    X = np.array(noisy_exp_vals).reshape(-1, 1)
    # get the exact output to perform linear regression
    y = np.array(noiseless_exp_vals)

    # initalize linear regression model
    model = LinearRegression()
    # fir the data to the model
    model.fit(X, y)
    return model

def plot_regression(noisy_exp_vals, noiseless_exp_vals, model):
    import matplotlib.pyplot as plt
    # get slope and intercept from the model
    slope = model.coef_[0]
    intercept = model.intercept_
    # plot the regression line and all the points
    plt.figure(figsize=(8,6))
    plt.scatter(noisy_exp_vals, noiseless_exp_vals, alpha = 0.5, label = 'Training data')
    noisy_range = np.linspace(min(noisy_exp_vals), max(noisy_exp_vals), 100)
    plt.plot(noisy_range, slope * noisy_range + intercept, 'r', label = 'Fitted line')
    plt.xlabel('Noisy Expectation Values')
    plt.ylabel('Noiseless Expectation Values')
    plt.legend()
    plt.title('Regression Model Plot')
    plt.show()
