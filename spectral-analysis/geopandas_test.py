import geopandas as gpd
import matplotlib.pyplot as plt

# Create a GeoDataFrame with a single point
# Replace the latitude and longitude values with your desired point
latitude = 40.7128
longitude = -74.0060
geometry = gpd.points_from_xy([longitude], [latitude])
gdf = gpd.GeoDataFrame({'Latitude': [latitude], 'Longitude': [longitude]}, geometry=geometry)

# Define the coordinate reference system (CRS) for the GeoDataFrame
# For this example, we'll use the WGS 84 coordinate system (EPSG:4326)
gdf.crs = "EPSG:4326"

# Plot the map using Geopandas and Matplotlib
fig, ax = plt.subplots(figsize=(8, 6))
gdf.plot(ax=ax, marker='o', color='red', markersize=100)

# Add a title to the plot
plt.title("Single Point on Map")

# Show the plot
plt.show()
