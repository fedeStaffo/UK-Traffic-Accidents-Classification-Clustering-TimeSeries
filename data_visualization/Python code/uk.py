import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Load the CSV file with the accident data
file_path = 'reducted.csv'  
df = pd.read_csv(file_path)

# Load the shapefile with the district boundaries
shapefile_path = 'C:/Users/emsar/OneDrive/Desktop/Progetto Data science/UK/LAD_MAY_2024_UK_BUC.shp'
districts_shapefile = gpd.read_file(shapefile_path)

# Set the CRS to EPSG:4326 for both GeoDataFrames
districts_shapefile = districts_shapefile.to_crs('EPSG:4326')
df = gpd.GeoDataFrame(df, geometry=gpd.GeoSeries.from_xy(df['Longitude'], df['Latitude']), crs='EPSG:4326')

# Check the validity of geometries and remove invalid ones
districts_shapefile = districts_shapefile[districts_shapefile.is_valid]

# Aggregate the accidents by district
incident_counts = df['Local_Authority_(District)'].value_counts()

# Calculate the percentage of accidents by district
total_incidents = incident_counts.sum()
incident_percentages = (incident_counts / total_incidents) * 100

# Associate the accident percentages with the districts
districts_shapefile['incident_percentage'] = districts_shapefile['LAD24NM'].map(incident_percentages).fillna(0)

# Create the choropleth map
fig, ax = plt.subplots(figsize=(14, 14)) 

plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

# Plot the choropleth map with the inverted RdYlGn palette
districts_shapefile.plot(column='incident_percentage', cmap='RdYlGn_r', legend=True,  
                         legend_kwds={'label': "Percentage of Accidents by District",
                                      'orientation': "horizontal"},
                         edgecolor='black', ax=ax)

# Set the aspect ratio
ax.set_aspect('equal')

# Add the title
plt.title('Accident Density by District in the United Kingdom (Percentage)', fontsize=14) 
plt.axis('off') 

# Save the plot as PNG
plt.savefig('uk.png', bbox_inches='tight', dpi=300)
plt.show()

# Generate a table with districts and their accident percentage
incident_table = incident_percentages.reset_index()
incident_table.columns = ['District', 'Incident Percentage'] 

# Print the table
print(incident_table)

# Save the table as CSV
incident_table.to_csv('incident_percentage_by_district.csv', index=False)
