import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Load the dataset and select the 'Day_of_Week' and 'Number_of_Casualties' columns
df = pd.read_csv('reducted.csv', usecols=['Day_of_Week', 'Number_of_Casualties'])

# Define the order of the days of the week
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Ensure that 'Day_of_Week' is treated as a categorical variable with the defined order
df['Day_of_Week'] = pd.Categorical(df['Day_of_Week'], categories=day_order, ordered=True)

# Count the frequency of each day of the week (percentages)
day_of_week_counts = df['Day_of_Week'].value_counts(normalize=True).sort_index() * 100  

# Calculate the average number of deaths for each day of the week
day_of_week_deaths = df.groupby('Day_of_Week', observed=False)['Number_of_Casualties'].mean().sort_index()

# Create a colormap that goes from green (fewer accidents) to red (more accidents)
norm = mcolors.Normalize(vmin=day_of_week_counts.min(), vmax=day_of_week_counts.max())
cmap = plt.cm.RdYlGn_r  # Colormap that goes from green to red

# Convert the colormap into a list of colors
palette_colors = [cmap(norm(value)) for value in day_of_week_counts.values]

# Create a vertical bar chart with colors mapped to the percentage of accidents
fig, ax1 = plt.subplots(figsize=(10, 6))

# Create the vertical bar for the percentage of accidents on the right axis
bars = sns.barplot(
    x=day_of_week_counts.index, 
    y=day_of_week_counts.values, 
    palette=palette_colors,  
    ax=ax1
)

# Set the title and labels
ax1.set_title('Percentage of Accidents and Average Deaths by Day of the Week', fontsize=14)
ax1.set_xlabel('Day of the Week', fontsize=12)
ax1.set_ylabel('Percentage of Accidents (%)', fontsize=12)

# Create a second y-axis on the left for the average number of deaths (now on the left axis)
ax2 = ax1.twinx()
ax2.plot(
    day_of_week_deaths.index, 
    day_of_week_deaths.values, 
    color='red', 
    marker='o', 
)
ax2.set_ylabel('Average Number of Deaths', fontsize=12, color='red')  

# Add a legend for the colormap next to the graph
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # Empty array needed for ScalarMappable
cbar = fig.colorbar(sm, ax=ax1, orientation='vertical', pad=0.02, aspect=30)

# Further extend the figure margins
plt.subplots_adjust(left=0.2, right=0.75)  

# Position the color bar much further to the right
cbar.ax.set_position([0.1, 0.15, 0.03, 0.7])  

# Save the plot as PNG
plt.savefig('days.png', bbox_inches='tight')

# Display the plot
plt.show()
