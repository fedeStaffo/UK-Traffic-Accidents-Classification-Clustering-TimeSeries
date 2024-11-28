import pandas as pd

# Load the two CSV files
file1 = pd.read_csv('accident_etl.csv')
file2 = pd.read_csv('vehicle_etl.csv')

# Perform an outer join between the two DataFrames on the 'Accident_Index' column
df_merged = pd.merge(file1, file2, how='outer', on='Accident_Index', indicator=True)

# Print the number of rows that did not have matching values in both files (these are the discarded rows)
scartati = df_merged[df_merged['_merge'] != 'both']
print(f"Number of discarded values: {len(scartati)}")

# Save the merged DataFrame into a new CSV file, removing the '_merge' column used for the join
df_merged.drop('_merge', axis=1, inplace=True)
df_merged.to_csv('complete.csv', index=False)
