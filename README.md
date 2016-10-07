To download the data from Google bigquery:

 - get google bigquery credentials
 - run the following:
    python download_sa_weather.py <credential_file>

The following files munge the data:

 - `python write_data.py` - converts
 - `python find_cape_town.py` - processes the big data file into the smaller cape town dataset


The following files plot various figures:

 - `python sampling.py` - is the brief demo that draws samples from a Gaussian Process
 - `python plot_stations.py`- shows where the weather stations are
 - `python scikit_test.py` - Simple 1D code for scikit.learn Gaussian processes
 - `python gpy_regression.py` - Simple 1D code for GPy regression
 - `python gpy_classification.py` - Simple 1D code for GPy classification
 - `python plot_za_rain` - Simple 2D code for GPy classification
