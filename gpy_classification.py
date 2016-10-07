import GPy
import numpy as np
import matplotlib.pyplot as plt

import utils

files = [("cape_town_preci.csv.gz", "Precipitation"), ]
funcs = [(utils.daily, "Daily")]
num_inducing = 50

for (f, ylabel) in files:
    for (func, xlabel) in funcs:
        (X, Y) = utils.get_data(func, f)
        print("Loaded")
        N = len(X)
        X = X[:N / 50]
        Y = Y[:N / 50]
        # Convert to boolean:
        Y = [y > 1.0 for y in Y]
        # (X, Y, _) = utils.average(X, Y)

        X = np.reshape(np.array(X), (-1, 1))
        Y = np.reshape(np.array(Y), (-1, 1))
        plt.scatter(X, Y)
        plt.xlabel("Rain?")
        plt.ylabel("Day of year")
        plt.savefig("./png/classification-data.png", bbox_inches='tight')
        break
        if func == utils.yearly:
            print("yearly")
            kernel = GPy.kern.RBF(input_dim=1, variance=1., lengthscale=10.)
        if func == utils.daily:
            print("daily")
            kernel = GPy.kern.StdPeriodic(
                input_dim=1, variance=.1, lengthscale=1., period=366.0)

        # lik = GPy.likelihoods.Bernoulli()
        m = GPy.models.SparseGPClassification(
            X, Y, kernel=kernel, num_inducing=num_inducing)
        # m.unconstrain('')  # may be used to remove the previous constrains
        # m.optimize(messages=True)
        # m.optimize_restarts(num_restarts=3, messages=True)
        print(m)

        name = xlabel + "-" + ylabel
        fig = m.plot()
        fig.axes.set_xlabel(xlabel)
        fig.axes.set_ylabel(ylabel)
        plt.savefig(
            "./png/classification-" + name + '.png', bbox_inches='tight')

plt.show()
