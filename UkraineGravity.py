import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap
from geopy.geocoders import Nominatim
from sklearn.cluster import KMeans


def run():
    """
    Aggregating function to run the clustering and plot the result
    """
    data = pd.read_parquet("data.parquet")
    point = simple_weights(data)
    plot_result(data, point)


def simple_weights(data) -> tuple:
    """
    Fits a KMeans clustering algorithm onto the geolocations using the contributions as naive weights
    Returns the point with minimal weighted distance
    """
    # Reshape and normalise both series, combine into matrix
    latitudes = data["Latitudes"].to_numpy().reshape(-1, 1) + 90
    longitudes = data["Longitudes"].to_numpy().reshape(-1, 1) + 180
    feature_matrix = np.concatenate(
        (longitudes, latitudes), axis=1)
    # Convert data to list
    weights = data["Total Assistance"].tolist()
    kmeans = KMeans(n_clusters=1, init="random")
    kmeans.fit(feature_matrix, sample_weight=weights)
    # Get optimal point and convert back to reular geodata
    optimal_point = kmeans.cluster_centers_[0]
    optimal_point[0] = optimal_point[0] - 180
    optimal_point[1] = optimal_point[1] - 90

    return optimal_point


def plot_result(data, point):
    """
    Plots the results
    """
    fig = plt.figure(figsize=(20, 10))
    m = Basemap(projection='mill', llcrnrlat=30, urcrnrlat=70,
                llcrnrlon=-10, urcrnrlon=40, resolution='c')
    m.drawcoastlines()
    m.drawcountries()
    m.fillcontinents(color="lightskyblue")
    # Get optimal point
    x_opt, y_opt = (point[0], point[1])
    # Plot capitals
    for idx, row in data.iterrows():
        m.plot([row['Longitudes'], x_opt], [row['Latitudes'], y_opt],
               color='seagreen', markersize=5, marker="o", linewidth=row["Total Assistance"]*2, latlon=True)
    # Plot optimal point
    m.plot(x_opt, y_opt, 'o', markersize=10, color="orangered", latlon=True)
    # Add titel and subtitle
    plt.title(
        "If clustered by KMeans using % of 2021 BIP as weight (indicated by linewidth)")
    fig.suptitle(
        "Gravitation Center of EU Assistance to Ukraine", fontsize=20, y=.95)
    plt.savefig("UkraineSupportGravityPlot.png", format="png", dpi=300)
    plt.show()


def extract_data() -> None:
    """
    Extracts the relevant data from the excel file, drops first, last and EU-lines(no geolocation).
    Saves the result as a parquet file after renaming the second column.
    """
    data = pd.read_excel(io="ukrainesupporttracker.xlsx",
                         sheet_name="Country Summary (€)", skiprows=10, usecols="B,C, Q")
    data.drop(data[data.iloc[:, 1] == 0].index, inplace=True)
    data.drop(data.index[-1], inplace=True)
    data.drop(data.index[0], inplace=True)
    data['Geolocation'] = data["Country"].apply(lambda x: get_location(x))
    data.drop(data.columns[1], axis=1, inplace=True)
    data.columns.values[1] = "Total Assistance"
    data["Latitudes"] = data['Geolocation'].apply(
        lambda x: x[0]).values.reshape(-1, 1)
    data["Longitudes"] = data['Geolocation'].apply(
        lambda x: x[1]).values.reshape(-1, 1)
    data.reset_index(drop=True, inplace=True)
    data.drop(columns=["Geolocation"], inplace=True)
    # Greece gets strange data?
    data._set_value(11, "Latitudes", 37.98381)
    data._set_value(11, "Longitudes", 23.727539)
    data.to_parquet("data.parquet")
    # Print to check if everything went well
    print(data)


def get_location(country) -> tuple:
    """
    Takes name, returns tuple of geolocation
    """
    geolocator = Nominatim(user_agent="UkrSup")
    location = geolocator.geocode(country)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None
