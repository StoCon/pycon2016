import GPy
import numpy as np
import matplotlib.pyplot as plt

import utils

plotly = False
if plotly:
    GPy.plotting.change_plotting_library('plotly')

files = [("cape_town_min_t.csv.gz", "Min Temp"),
         ("cape_town_max_t.csv.gz", "Max Temp"), ]

funcs = [(utils.daily, "Daily"), (utils.yearly, "Yearly")]
for (f, ylabel) in files:
    for (func, xlabel) in funcs:
        (X, Y) = utils.get_data(func, f)
        (X, Y, _) = utils.average(X, Y)
        X = np.reshape(np.array(X), (-1, 1))
        Y = np.reshape(np.array(Y), (-1, 1))

        if func == utils.yearly:
            print("yearly")
            kernel = GPy.kern.RBF(input_dim=1, variance=1., lengthscale=1.)
        if func == utils.daily:
            print("daily")
            kernel = GPy.kern.StdPeriodic(
                input_dim=1, variance=.1, lengthscale=20., period=366.0)

        m = GPy.models.GPRegression(X, Y, kernel=kernel)
        m.optimize_restarts(num_restarts=3)
        print(m)

        name = xlabel + "-" + ylabel
        fig = m.plot()
        fig.axes.set_xlabel(xlabel)
        fig.axes.set_ylabel(ylabel)
        plt.savefig("./png/" + name + '.png', bbox_inches='tight')

plt.show()
