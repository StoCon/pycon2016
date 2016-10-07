# # Let's display the weather stations on a map of SA
# # Bounding box:
# # Bottom left: -35, 15
# # Top right:   -21, 35

import csv

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

# Let's open 1973 and plot all the stations we find there
filename = "csv/sa_weather_1973.csv"
with open(filename, 'rb') as csvfile:
    csvreader = csv.reader(csvfile)

    coords = set()
    for row in csvreader:
        coord = (row[3], row[2])
        coords.add(coord)

longitudes = [float(x) for (x, y) in coords]
latitudes = [float(y) for (x, y) in coords]
# Time to plot things
# setup Lambert Conformal basemap.
m = Basemap(
    width=2200000,
    height=2000000,
    projection='lcc',
    resolution='l',
    lat_0=-28,
    lon_0=25)
m.shadedrelief()
m.drawcountries()
m.drawcoastlines()
(x, y) = ([15, 35, 15, 35, 18, 19, 18, 19],
          [-35, -35, -21, -21, -33.6, -33.6, -34.4, -34.4])

m.scatter(*m(x, y), color='red')
m.scatter(*m(longitudes, latitudes), color='blue')

plt.savefig("./png/weather_stations.png", bbox_inches='tight')
plt.show()
