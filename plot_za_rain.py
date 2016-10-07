import GPy
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

import utils


def process(X, Y):
    print("earliest year : " + str(X[:, 2].min()))
    print("latest year : " + str(X[:, 2].max()))
    X[:, 0] = (X[:, 0] - X[:, 0].min()) / (X[:, 0].max() - X[:, 0].min())
    X[:, 1] = (X[:, 1] - X[:, 1].min()) / (X[:, 1].max() - X[:, 1].min())
    X[:, 2] = (X[:, 2] - np.floor(X[:, 2])) * 366

    # Convert to boolean:
    Y = Y > 1.0
    return X, Y


files = [("precipitation.csv.gz", "Precipitation"), ]

(X, Y) = utils.get_data(utils.all_data, "precipitation.csv.gz")
print("Loaded")

# do some ad-hoc processing:
N = len(X)
from_ind = int(8.0 * N / 10.0)
to_ind = int(9.0 * N / 10.0)
X = X[from_ind:to_ind]
Y = Y[from_ind:to_ind]

X = np.reshape(np.array(X), (-1, 3))
Y = np.reshape(np.array(Y), (-1, 1))

X, Y = process(X, Y)

np.save("X.npy", X)
np.save("Y.npy", Y)
# X = np.load("X.npy")
# Y = np.load("Y.npy")
num_days = 2

# Wettest week
# day_range_middle = 178

# # Driest week:
day_range_middle = 9
day_range_lower = day_range_middle - num_days
day_range_upper = day_range_middle + num_days

ind = (day_range_lower <= X[:, 2]) & (X[:, 2] <= day_range_upper)
X = X[ind, :2]  # Drop the days
X = X[:, (1, 0)]
Y = Y[ind]

print("Processed")
num_inducing = 10
kernel = GPy.kern.RBF(input_dim=2, variance=1., lengthscale=1.)
m = GPy.models.SparseGPClassification(
    X, Y, kernel=kernel, num_inducing=num_inducing)
m.optimize_restarts(num_restarts=1)
print(m)

za_mp = Basemap(
    width=2200000,
    height=2000000,
    projection='lcc',
    resolution='l',
    lat_0=-28,
    lon_0=25)
za_mp.shadedrelief()
za_mp.drawcountries()
za_mp.drawcoastlines()

fig1 = m.plot()
plt.show()
