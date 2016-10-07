import gzip
from datetime import datetime
import csv
import traceback

seconds_per_year = 366 * 24 * 60 * 60.0
years = {year: datetime(year, 1, 1) for year in range(1800, 2100)}


def to_float_year(dt):
    year = dt.year
    start = years[year]
    fractional = (dt - start).total_seconds() / seconds_per_year
    return year + fractional


def add_to_file(writer, lat, lon, date, row, index):
    try:
        datum = float(row[index])
        writer.writerow([lat, lon, date, datum])
    except ValueError:
        if index == 5:  # Only print failing precipitation
            print("Failed:")
            print(repr(row))


def add_to_all(pre_writer, min_writer, max_writer, row):
    try:
        lat = float(row[2])
        lon = float(row[3])
        date = datetime.strptime(row[4], "%Y-%m-%d")
        fyear = to_float_year(date)

        add_to_file(pre_writer, lat, lon, fyear, row, 5)
        add_to_file(min_writer, lat, lon, fyear, row, 6)
        add_to_file(max_writer, lat, lon, fyear, row, 7)

    except Exception:
        traceback.print_exc()


precipit_file = gzip.open("precipitation.csv.gz", "wb")
min_temp_file = gzip.open("min_temp.csv.gz", "wb")
max_temp_file = gzip.open("max_temp.csv.gz", "wb")

precipit_csv = csv.writer(precipit_file)
min_temp_csv = csv.writer(min_temp_file)
max_temp_csv = csv.writer(max_temp_file)

try:
    for year in range(1850, 2016):

        filename = "sa_weather_{year}.csv".format(year=year)
        with open(filename, 'rb') as csvfile:
            csvreader = csv.reader(csvfile)

            for row in csvreader:
                add_to_all(precipit_csv, min_temp_csv, max_temp_csv, row)

finally:
    max_temp_file.close()
    min_temp_file.close()
    precipit_file.close()
