import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Update with the correct path to your CSV file
df = pd.read_csv('accident_etl.csv')  

# Extract the month from the date, excluding the year
df['Month'] = pd.to_datetime(df['Date'], errors='coerce').dt.month

# Remove any rows with missing values (if any)
df_clean = df.dropna(subset=['Month', 'Number_of_Casualties'])

# Group the data by month
monthly_data = df_clean.groupby('Month').agg(
    Number_of_Accidents=('Accident_Index', 'count'),
    Number_of_Fatalities=('Number_of_Casualties', 'mean')
).reset_index()

# Calculate the percentage of accidents for each month
total_accidents = monthly_data['Number_of_Accidents'].sum()
monthly_data['Percentage_of_Accidents'] = (monthly_data['Number_of_Accidents'] / total_accidents) * 100

# Create the plot
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot for the number of accidents (left axis) as a percentage
sns.lineplot(x='Month', y='Percentage_of_Accidents', data=monthly_data, color='violet', label=None, linewidth=2, ax=ax1)

# Create a second y-axis for the average number of fatalities (right axis)
ax2 = ax1.twinx()
sns.lineplot(x='Month', y='Number_of_Fatalities', data=monthly_data, color='orange', label=None, linewidth=2, ax=ax2)

# Add labels and title
ax1.set_xlabel('Month', fontsize=12)
ax1.set_ylabel('Percentage of Accidents (%)', fontsize=12, color='violet')
ax2.set_ylabel('Average Fatalities', fontsize=12, color='orange')
plt.title('Accidents and Fatalities by Month', fontsize=14)

# Set month names for the x-axis ticks
month_names = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.']
plt.xticks(ticks=range(1, 13), labels=month_names, rotation=45, ha='right')

# Save the plot as PNG
plt.savefig('months.png', bbox_inches='tight')

# Do not display the plot in the terminal
plt.close()
