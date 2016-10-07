import numpy as np
import csv
import gzip


def get_data(func, filename):
    with gzip.open(filename, 'rb') as f:
        reader = csv.reader(f)
        (xs, ys) = ([], [])
        for row in reader:
            try:
                x = func(row)
                y = float(row[3])
            except ValueError:
                continue
            xs.append(x)
            ys.append(y)
        return (xs, ys)


def average(xs, ys):
    N = 10000
    counts = np.zeros(N)
    sums = np.zeros(N)
    for (x, y) in zip(xs, ys):
        idx = int(x)
        counts[idx] += 1
        sums[idx] += y
    ind = counts != 0
    xs = np.arange(N)[ind]
    ys = sums[ind] / counts[ind]
    counts = counts[ind]
    return (xs, ys, counts)


def daily(row):
    dt = float(row[2])
    return int((dt - int(dt)) * 366)


def yearly(row):
    return int(float(row[2]))


def all_data(row):
    return map(float, row[:-1])


def beautiful_plot(x, y, ax, col, label, xlabel, ylabel):
    ax.scatter(x, y, color=col, label=label, alpha=0.1)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
