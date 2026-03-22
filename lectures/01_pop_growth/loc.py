import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Dictionary of locations (Latitude, Longitude)
# Added 'offset' (lon_adjust, lat_adjust) and 'ha' (horizontalalignment)
locations = {
    "Uni Braunschweig": {"coords": [52.2736, 10.5303], "color": "green", "offset": (0.2, 0), "ha": "left"},
    "Uni Göttingen": {"coords": [51.5398, 9.9371], "color": "green", "offset": (-0.2, 0.1), "ha": "right"}, # Pushed left and slightly up
    "RWTH Aachen": {"coords": [50.7785, 6.0600], "color": "green", "offset": (0.2, 0), "ha": "left"},
    "Uni Leipzig": {"coords": [51.3397, 12.3731], "color": "green", "offset": (0.2, 0.2), "ha": "left"}, # Pushed right and slightly up
    "FSU Jena": {"coords": [50.9298, 11.5831], "color": "green", "offset": (0.2, -0.3), "ha": "left"}, # Pushed right and down
    "Uni Trier": {"coords": [49.7483, 6.6850], "color": "green", "offset": (0.2, 0), "ha": "left"},
    "RPTU Campus Landau": {"coords": [49.2045, 8.1157], "color": "green", "offset": (0.2, 0), "ha": "left"},
    "TUM": {"coords": [48.1485, 11.5679], "color": "red", "offset": (0.2, 0), "ha": "left"}, 
    "Uni Freiburg": {"coords": [47.9940, 7.8496], "color": "green", "offset": (-0.2, 0.1), "ha": "right"},
    "Uni Basel": {"coords": [47.5584, 7.5830], "color": "green", "offset": (0.2, -0.2), "ha": "left"}, # Pushed down to clear Freiburg
    "Trinity College Dublin": {"coords": [53.3438, -6.2546], "color": "red", "offset": (0.3, 0), "ha": "left"},
    "Lund University": {"coords": [55.7058, 13.1932], "color": "red", "offset": (-0.2, 0), "ha": "right"}
}

# 1. Create the Figure and Axes
fig = plt.figure(figsize=(14, 10))
ax = plt.axes(projection=ccrs.Mercator())

# 2. Set the map boundaries [lon_min, lon_max, lat_min, lat_max]
ax.set_extent([-11, 16, 46, 58], crs=ccrs.PlateCarree())

# 3. Add styling features
ax.add_feature(cfeature.OCEAN, facecolor='#E5F5FA')
ax.add_feature(cfeature.LAND, facecolor='#FDFDF3')
ax.add_feature(cfeature.COASTLINE, linewidth=1, edgecolor='#444444')
ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=1, edgecolor='#777777')

# 4. Draw Dashed Connections Centered on Jena
jena_lat, jena_lon = locations["FSU Jena"]["coords"]

for name, info in locations.items():
    if name != "FSU Jena":
        lat, lon = info["coords"]
        ax.plot([jena_lon, lon], [jena_lat, lat], 
                color='gray', linestyle='--', linewidth=1.2, alpha=0.6,
                transform=ccrs.Geodetic(), zorder=1)

# 5. Plot the points and labels
for name, info in locations.items():
    lat, lon = info["coords"]
    color = info["color"]
    lon_offset, lat_offset = info["offset"]
    ha = info["ha"]
    
    # Plot the dot
    ax.plot(lon, lat, marker='o', color=color, markersize=9, 
            markeredgecolor='black', markeredgewidth=1, 
            transform=ccrs.PlateCarree(), zorder=2)
    
    # Add the text label using the custom offsets and alignments
    ax.text(lon + lon_offset, lat + lat_offset, name, 
            verticalalignment='center', horizontalalignment=ha,
            fontsize=16, transform=ccrs.PlateCarree(),
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=1.5), 
            zorder=3)

plt.title("Selected Universities Connected to FSU Jena", fontsize=16, pad=20)

# 6. Save the result
output_filename = "universities_map_cartopy.png"
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
print(f"Map successfully saved as {output_filename}!")