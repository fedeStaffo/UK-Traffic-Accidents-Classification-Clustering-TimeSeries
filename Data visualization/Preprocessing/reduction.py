import pandas as pd

# Carica il dataset e seleziona solo le colonne desiderate
accident_data = pd.read_csv('accident_etl.csv', usecols=['Accident_Index', 'Latitude', 'Longitude', 'Local_Authority_(District)', 'Number_of_Casualties'])

# Salva il file CSV con i dati originali, senza alcuna modifica
accident_data.to_csv('reducted.csv', index=False)

# Estrai la colonna e rimuovi i duplicati
unique_values = accident_data['Latitude'].drop_duplicates()

# Mostra le stringhe uniche
print(unique_values)

# Estrai la colonna e rimuovi i duplicati
unique_values = accident_data['Longitude'].drop_duplicates()

# Mostra le stringhe uniche
print(unique_values)
