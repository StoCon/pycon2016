import csv
import gzip

files = [("precipitation.csv.gz", "cape_town_preci.csv.gz"),
         ("min_temp.csv.gz", "cape_town_min_t.csv.gz"),
         ("max_temp.csv.gz", "cape_town_max_t.csv.gz"), ]

for (inp, out) in files:
    i_f = gzip.open(inp, "rb")
    o_f = gzip.open(out, "wb")
    reader = csv.reader(i_f)
    writer = csv.writer(o_f)
    try:
        # Cape Town is now defined by this bounding box:
        (minlong, maxlong, minlat, maxlat) = [18, 19, -34.4, -33.6]
        for row in reader:
            lat = float(row[0])
            lon = float(row[1])
            if lat > maxlat or lat < minlat:
                continue
            if lon > maxlong or lon < minlong:
                continue
            # Hooray - data for Cape Town
            writer.writerow(row)
    finally:
        i_f.close()
        o_f.close()
