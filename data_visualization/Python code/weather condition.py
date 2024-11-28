import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset and select the Weather_Conditions column
df = pd.read_csv('accident_etl.csv', usecols=['Weather_Conditions'])

# Filter the data to remove "Data missing or out of range" and "Unknown"
df_clean = df[~df['Weather_Conditions'].isin(['Data missing or out of range', 'Unknown'])]

# Count the frequency of values and calculate the percentage proportions
condition_counts = df_clean['Weather_Conditions'].value_counts(normalize=True) * 100

# Sort the conditions by frequency
sorted_conditions = condition_counts.sort_values(ascending=False)

# Use the "deep" color palette
colors = sns.color_palette("deep", len(sorted_conditions))

# Draw the pie chart
plt.figure(figsize=(10, 8))
plt.pie(
    sorted_conditions, 
    labels=None, 
    colors=colors, 
    startangle=90, 
    wedgeprops={'edgecolor': 'white'} 
)

# Create a legend with labels and percentages
legend_labels = [f"{condition} ({percentage:.1f}%)" for condition, percentage in zip(sorted_conditions.index, sorted_conditions.values)]
plt.legend(legend_labels, title="Weather Conditions", loc='center left', bbox_to_anchor=(1, 0.5))

# Add a title
plt.title('Most Dangerous Weather Conditions (Percentage)', fontsize=14)

# Save the chart as PNG
plt.savefig('weather_conditions.png', bbox_inches='tight')

# Do not display the chart in the terminal
plt.close()
