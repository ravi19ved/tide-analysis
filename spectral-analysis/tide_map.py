import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# Sample data: list of latitude and longitude coordinates
latitude = [40.7128, 37.7749, 34.0522, 41.8781]
longitude = [-74.0060, -122.4194, -118.2437, -87.6298]

# Create the figure and axis objects using Cartopy
plt.figure(figsize=(10, 6))
ax = plt.axes(projection=ccrs.PlateCarree())

# Set the extent of the map (in this case, it will show the entire world)
ax.set_global()

# Add a coastline feature to the map
ax.coastlines()

# Plot the points on the map
ax.scatter(longitude, latitude, color='red', s=100, transform=ccrs.PlateCarree())

# Add a title to the plot
plt.title("Map with a Set of Points")

# Show the plot
plt.show()
