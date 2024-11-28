import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Load the dataset and select the 'Vehicle_Type' column
df = pd.read_csv('reducted.csv', usecols=['Vehicle_Type'])

# Filter the data to remove "Data missing or out of range"
df_clean = df[df['Vehicle_Type'] != 'Data missing or out of range']

# Count the frequency of values and sort them in descending order
vehicle_counts = df_clean['Vehicle_Type'].value_counts()

# Calculate the percentages relative to the total number of incidents
vehicle_percentage = (vehicle_counts / vehicle_counts.sum()) * 100

# Create a colormap that goes from red to green and invert it
norm = mcolors.LogNorm(vmin=vehicle_percentage.values.min(), vmax=vehicle_percentage.values.max())  
cmap = plt.cm.RdYlGn_r  

# Create a list of colors to use for the bars, with logarithmic normalization
colors = [cmap(norm(value)) for value in vehicle_percentage.values] 

# Create the horizontal bar chart
plt.figure(figsize=(10, 6))
ax = sns.barplot(x=vehicle_percentage.values, y=vehicle_percentage.index, palette=colors)

# Set the logarithmic scale on the x-axis
plt.xscale('log')

# Add labels and title
plt.xlabel('Percentage of Vehicles (%) (Log Scale)', fontsize=12)
plt.ylabel('Vehicle Type', fontsize=12)
plt.title('Vehicle Type Distribution (Percentage)', fontsize=14)

# Create the ScalarMappable object for the colorbar with LogNorm
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  

# Add the colorbar to the right of the chart
cbar = plt.colorbar(sm, ax=ax, pad=0.01)

# Save the chart as PNG
plt.savefig('vehicle_log.png', bbox_inches='tight')

# Do not display the chart in the terminal
plt.close()
