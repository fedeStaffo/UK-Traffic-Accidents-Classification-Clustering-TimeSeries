import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors
import numpy as np

# Load the data and select the relevant columns
accident_data = pd.read_csv('accident_etl.csv', usecols=['Accident_Index', 'Time', 'Accident_Severity'])

# Clean the 'Time' column (extract HH:MM format if present)
accident_data['Time'] = accident_data['Time'].str.extract(r'(\d{1,2}:\d{2})')

# Convert to extract only the hour
accident_data['Hour'] = pd.to_datetime(accident_data['Time'], format='%H:%M', errors='coerce').dt.hour

# Filter out invalid data (remove rows with NaN in the 'Hour' column)
accident_data = accident_data.dropna(subset=['Hour'])

# Calculate the number of accidents per hour in percentage
total_accidents = len(accident_data)
accidents_per_hour = (
    accident_data.groupby('Hour').size().reset_index(name='Number_of_Accidents')
)
accidents_per_hour['Percentage_of_Accidents'] = (
    accidents_per_hour['Number_of_Accidents'] / total_accidents * 100
)

# Convert 'Hour' to integers to ensure correct ticks
accidents_per_hour['Hour'] = accidents_per_hour['Hour'].astype(int)

# Define the custom colormap
norm = mcolors.Normalize(
    vmin=accidents_per_hour['Percentage_of_Accidents'].min(),
    vmax=accidents_per_hour['Percentage_of_Accidents'].max()
)
cmap = plt.cm.RdYlGn_r  # Green (fewer accidents) to red (more accidents)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])

# Apply the mapped colors directly to the values
colors = accidents_per_hour['Percentage_of_Accidents'].apply(lambda x: cmap(norm(x)))

# Create the plot with green-yellow-red palette
sns.set_theme(style="whitegrid")
plt.figure(figsize=(14, 6))

# Create the bar plot (with width=1.0 to reduce padding)
bars = sns.barplot(
    x='Hour', y='Percentage_of_Accidents', data=accidents_per_hour,
    palette=colors.tolist(), alpha=0.9, edgecolor="black", width=1.0
)

# Labels and title
plt.xlabel('Hour', fontsize=12)
plt.ylabel('Percentage of Accidents (%)', fontsize=12)
plt.title('Percentage of Accidents per Hour', fontsize=14)

# Modify the position of ticks on the X-axis to shift them slightly to the right
# We set the ticks slightly to the right of their default position
xticks_position = np.arange(24)  
xticks_offset = 0.5 

# Update the tick positions and use the `ha` parameter for alignment
plt.xticks(xticks_position - xticks_offset, [str(i) for i in range(24)], ha='center')

# Add the color legend bar next to the plot
cbar = plt.colorbar(sm, ax=plt.gca(), orientation='vertical', pad=0.02)
cbar.ax.tick_params(labelsize=10)

# Position the color bar to the right of the plot
cbar.ax.set_position([0.92, 0.2, 0.02, 0.6])

# Save the plot
plt.tight_layout()
plt.savefig('hours.png', dpi=300)
plt.show()
