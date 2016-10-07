# Author: Vincent Dubourg <vincent.dubourg@gmail.com>
#         Jake Vanderplas <vanderplas@astro.washington.edu>
#         Jan Hendrik Metzen <jhm@informatik.uni-bremen.de>s
# License: BSD 3 clause

import numpy as np
from matplotlib import pyplot as plt

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel

import utils

files = [("cape_town_min_t.csv.gz", "Min Temp", 'b-'),
         ("cape_town_max_t.csv.gz", "Max Temp", 'r-'),
         #  ("cape_town_preci.csv.gz", "Precipitation"),
         ]
funcs = [(utils.daily, "Daily"), (utils.yearly, "Yearly")]

for (func, xlabel) in funcs:
    fig = plt.figure()
    for (f, ylabel, col) in files:
        (X, Y) = utils.get_data(func, f)
        (X, Y, _) = utils.average(X, Y)

        # Mesh the input space for evaluations of the real function, the
        # prediction and its MSE
        x = np.atleast_2d(np.linspace(min(X), max(X), 1000)).T

        X = np.reshape(np.array(X), (-1, 1))
        Y = np.reshape(np.array(Y), (-1, 1))

        # Instantiate a Gaussian Process model
        kernel = RBF(length_scale=1.0, length_scale_bounds=(1e-1, 1e3)) \
            + WhiteKernel(noise_level=1e-1, noise_level_bounds=(1e-2, 1e+2))
        gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9)

        # Fit to data using Maximum Likelihood Estimation of the parameters
        gp.fit(X, Y)

        # Make the prediction on the meshed x-axis (ask for MSE as well)
        y_pred, sigma = gp.predict(x, return_std=True)

        sigma = np.reshape(np.array(sigma), (-1, 1))
        # Plot the function, the prediction and the 95% confidence interval
        # based on the MSE
        # plt.errorbar(
        #     X.ravel(), y, dy, fmt='r.', markersize=10, label=u'Observations')
        plt.plot(x, y_pred, col, label=u'Prediction')
        plt.fill(
            np.concatenate([x, x[::-1]]),
            np.concatenate(
                [y_pred - 1.9600 * sigma, (y_pred + 1.9600 * sigma)[::-1]]),
            alpha=.5,
            fc=col[0],
            ec='None',
            label='95% confidence interval')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        # plt.legend()

plt.show()
