import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset and select the 'Road_Surface_Conditions' column
df = pd.read_csv('accident_etl.csv', usecols=['Road_Surface_Conditions'])

# Filter the data to remove rows with 'Data missing or out of range'
df_clean = df[df['Road_Surface_Conditions'] != 'Data missing or out of range']

# Count the frequency of each value in the 'Road_Surface_Conditions' column
condition_counts = df_clean['Road_Surface_Conditions'].value_counts()

# Calculate the percentages for each category
percentages = (condition_counts / condition_counts.sum() * 100).round(1)

# Create a donut-shaped pie chart with bright colors
sns.set_theme(style="whitegrid")
colors = sns.color_palette("deep", len(condition_counts))

# Draw the donut-shaped pie chart
plt.figure(figsize=(8, 6))  
plt.pie(condition_counts, colors=colors, wedgeprops={'width': 0.3})  

# Create a legend with percentages
legend_labels = [f"{label} ({percent}%)" for label, percent in zip(condition_counts.index, percentages)]
plt.legend(legend_labels, title='Road Surface Conditions', loc='center left', bbox_to_anchor=(1, 0.5))

# Add the chart title
plt.title('Distribution of Road Surface Conditions', fontsize=14)

# Save the chart as PNG
plt.savefig('surface_conditions.png', bbox_inches='tight')

# Do not display the chart in the terminal
plt.close()
