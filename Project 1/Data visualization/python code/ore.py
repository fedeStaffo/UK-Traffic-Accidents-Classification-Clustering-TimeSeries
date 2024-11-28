import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Caricamento dei dati e selezione delle colonne rilevanti
accident_data = pd.read_csv('accident_etl.csv', usecols=['Accident_Index', 'Time', 'Accident_Severity'])

# Step 1: Esaminare i primi valori della colonna Time
print("Primi 20 valori della colonna Time:")
print(accident_data['Time'].head(20))

# Step 2: Pulizia della colonna Time (estrazione del formato HH:MM, se presente)
accident_data['Time'] = accident_data['Time'].str.extract(r'(\d{1,2}:\d{2})')
print("\nPrimi 20 valori della colonna Time dopo la pulizia:")
print(accident_data['Time'].head(20))

# Step 3: Conversione per estrarre solo l'ora
accident_data['Hour'] = pd.to_datetime(accident_data['Time'], format='%H:%M', errors='coerce').dt.hour

# Step 4: Controllo per valori NaN nella colonna Hour
print("\nNumero di valori NaN nella colonna Hour:", accident_data['Hour'].isna().sum())
print("\nPrimi 20 valori di Time e Hour dopo la conversione:")
print(accident_data[['Time', 'Hour']].head(20))

# Step 5: Filtraggio dei dati validi (eliminare righe con Hour NaN)
accident_data = accident_data.dropna(subset=['Hour'])

# Step 6: Elimino la colonna Accident_Severity dal DataFrame, poiché non la consideriamo nel grafico
accident_data = accident_data.drop(columns=['Accident_Severity'])

# Step 7: Calcolo del numero di incidenti per ora
accidents_per_hour = accident_data.groupby('Hour').size().reset_index(name='Number_of_Accidents')

# Debug: Controllo dei dati per il grafico
print("\nDati finali per il grafico (numero di incidenti per ora):")
print(accidents_per_hour.head())

# Step 8: Creazione del grafico con Seaborn
sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 6))

# Istogramma: Numero di incidenti per ora
sns.barplot(
    x='Hour', y='Number_of_Accidents', data=accidents_per_hour, 
    palette="coolwarm", alpha=0.8
)
plt.xlabel('Hour')
plt.ylabel('Number of Accidents')
plt.title('Number of Accidents per Hour', fontsize=14)

# Step 9: Salvataggio del grafico
plt.tight_layout()
plt.savefig('hours.png', dpi=300)
plt.show()
