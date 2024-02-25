import numpy as np
import pandas as pd
from matplotlib import colors
import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap
from geopy.geocoders import Nominatim
from sklearn.cluster import KMeans


def run_concentricity(num_circles: int = 10, circle_distance: float = 500.0):
    """
    Reads the data and plots the capital with a specific color scheme.
    After that plots Kiyv and Mocscow with concentric circles off 500 km distance.
    Adds label for all capitals.    
    """
    data = pd.read_parquet("data.parquet")
    data.sort_values(by=["Total Assistance"], inplace=True, ascending=False)

    num_steps = len(data)
    data.reset_index(drop=True, inplace=True)
    # Create a custom colormap from white to darkgreen
    colors_list = [(0, 0.5, 0), (1, 1, 0.25)]  # White to Dark Green
    cmap_name = 'custom_cmap'
    cm = colors.LinearSegmentedColormap.from_list(
        cmap_name, colors_list, N=num_steps)
    fig = plt.figure(figsize=(20, 10))

    m = Basemap(projection='mill', llcrnrlat=30, urcrnrlat=70,
                llcrnrlon=-10, urcrnrlon=40, resolution='c')

    # Draw basemap
    m.drawcoastlines()
    m.drawcountries()
    m.fillcontinents(color="lightskyblue")

    # Plot Moscow

    # Plot capitals
    for idx, row in data.iterrows():
        color = cm(idx / len(data))
        m.plot(row['Longitudes'], row['Latitudes'],
               color=color, markersize=5*row["Total Assistance"], marker="o", latlon=True, label=row["Capital"])

    # Plot Moscow
    moscow_lat, moscow_lon = 55.7558, 37.6173
    m.plot(moscow_lon, moscow_lat, color="firebrick", marker="o",
           markersize=5, label='Moscow', latlon=True)

    # Plot Kiev
    kiev_lat, kiev_lon = 50.4501, 30.5234
    m.plot(kiev_lon, kiev_lat, marker="o", color="navy",
           markersize=5, label='Kyiv', latlon=True)

    # Plot concentric circles around Moscow

    for i in range(1, num_circles + 1):
        circle_radius = i * circle_distance
        lats = []
        lons = []
        for theta in np.linspace(0, 2*np.pi, 100):
            circle_lon = moscow_lon + \
                (circle_radius / (111.32 * np.cos(np.radians(moscow_lat)))) * np.cos(theta)
            circle_lat = moscow_lat + (circle_radius / 111.32) * np.sin(theta)
            lats.append(circle_lat)
            lons.append(circle_lon)

        x, y = m(lons, lats)
        linewidth = 3 / i  # Adjust linewidth based on distance from Moscow
        m.plot(x, y, color="darkorange", linewidth=linewidth)

    fig.suptitle(
        "EU Capitals distance to Moscow, concentric circle width 500 km", fontsize=20, y=.95)
    plt.title(
        "Capital sizes are scaled by support given/GDP, coloring represents that order \n Kyiv and Mocscow have unscaled size(would imply 1% of GDP as aid).")
    plt.legend(loc='center left', bbox_to_anchor=(-0.25, 0.5))
    plt.savefig("CapitalsMoscowCircle.png", format="png", dpi=300)
    plt.show()


def run_support_gravity_center():
    """
    Aggregating function to run the clustering and plot the result
    """
    data = pd.read_parquet("data.parquet")
    point = simple_weights(data)
    plot_support_gravity_center(data, point)


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


def plot_support_gravity_center(data, point):
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


def extract_support_gravity_center() -> None:
    """
    Extracts the relevant data from the excel file, drops first, last and EU-lines(no geolocation).
    Saves the result as a parquet file after renaming the second column.
    """
    data = pd.read_excel(io="ukrainesupporttracker.xlsx",
                         sheet_name="Country Summary (€)", skiprows=10, usecols="B,C, Q")
    capitals = pd.read_csv("country-list.csv", index_col=0, usecols=[0, 1,])
    data.drop(data[data.iloc[:, 1] == 0].index, inplace=True)
    data.drop(data.index[-1], inplace=True)
    data.drop(data.index[0], inplace=True)
    data['Capital'] = data["Country"].apply(
        lambda x: get_capital_name(x, capitals))
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


def get_capital_name(country: str, lookup_df) -> str:
    return lookup_df.loc[country]


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
