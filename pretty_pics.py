import matplotlib.pyplot as plt
import utils

figures = [
    "FIGURE",
    ("cape_town_preci.csv.gz", utils.daily, "k", "Precipitation", "Daily",
     "Rainfall"),
    "LEGEND",
    "FIGURE",
    ("cape_town_min_t.csv.gz", utils.daily, "b", "Min temp", "Daily", "Temp"),
    ("cape_town_max_t.csv.gz", utils.daily, "r", "Max temp", "Daily", "Temp"),
    "LEGEND",
    "FIGURE",
    ("cape_town_preci.csv.gz", utils.yearly, "k", "Precipitation", "Yearly",
     "Rainfall"),
    "LEGEND",
    "FIGURE",
    ("cape_town_min_t.csv.gz", utils.yearly, "b", "Min temp", "Yearly",
     "Temp"),
    ("cape_town_max_t.csv.gz", utils.yearly, "r", "Max temp", "Yearly",
     "Temp"),
    "LEGEND",
]

for average_data in [False, True]:
    for f in figures:
        if f == "FIGURE":
            name = ""
            fig, ax = plt.subplots()
            continue
        if f == "LEGEND":
            ax.legend()
            if average_data:
                name += "Averaged"
            plt.savefig("./png/" + name + '.png', bbox_inches='tight')
            continue
        (filename, func, col, label, xlabel, ylabel) = f
        name += label + xlabel
        (xs, ys) = utils.get_data(func, filename)
        print(filename, len(xs))
        if average_data:
            (xs, ys, counts) = utils.average(xs, ys)
        utils.beautiful_plot(xs, ys, ax, col, label, xlabel, ylabel)
