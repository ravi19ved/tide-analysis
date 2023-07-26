# All Library Imports

import geopandas as gpd
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

def plot_points_on_map(points_list):

    # Create a GeoDataFrame from the list of points

    gdf = gpd.GeoDataFrame({'geometry': gpd.points_from_xy([point[1] for point in points_list], [point[0] for point in points_list])})
    gdf.crs = 'EPSG:4326'

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
  
  
    ax = world.plot(figsize=(10, 8), color='white', edgecolor='black')
    gdf.plot(ax=ax, color='red', markersize=50)

    plt.show()


if __name__ == "__main__":
    # Example list of points (latitude, longitude)
    points_list = [
        (40.7128, -74.0060),  # New York City
        (34.0522, -118.2437),  # Los Angeles
        (51.5074, -0.1278),    # London
        (35.6895, 139.6917),   # Tokyo
    ]

    plot_points_on_map(points_list)