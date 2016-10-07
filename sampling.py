# Code shamelessly stolen from:
# http://stats.stackexchange.com/questions/198327/sampling-from-gaussian-process-posterior
import GPy
import numpy as np
import matplotlib.pyplot as plt
"""
This gives a brief demo of drawing samples from a Gaussian process
"""
plt.ion()

sample_size = 200
full_X = np.random.uniform(0, 1., (sample_size, 1))
full_Y = np.sin(full_X) + np.random.randn(sample_size, 1) * 0.25

true_X = np.linspace(0, 1, 100)
true_Y = np.sin(true_X)
fig = plt.figure()
ax = fig.add_subplot(111)
for a in range(2, sample_size, 2):
    X = full_X[:a]
    Y = full_Y[:a]

    kernel = GPy.kern.RBF(input_dim=1, variance=1., lengthscale=1.)
    model = GPy.models.GPRegression(X, Y, kernel, noise_var=1e-10)
    model.optimize_restarts(num_restarts=3)
    testX = np.linspace(0, 1, 100).reshape(-1, 1)
    posteriorTestY = model.posterior_samples_f(testX, full_cov=True, size=10)
    simY, simMse = model.predict(testX)

    plt.cla()
    plt.plot(true_X, true_Y, 'k', linewidth=10, alpha=0.25)
    plt.plot(testX, posteriorTestY, alpha=0.5)
    plt.plot(X, Y, 'ok', markersize=10)
    plt.plot(testX, simY - 1.95 * simMse**0.5, '--g')
    plt.plot(testX, simY + 1.95 * simMse**0.5, '--g')
    plt.axis([0.0, 1.0, -0.3, +1.1])
    plt.pause(10.0 / a)
