import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Aggiorna con il percorso corretto del tuo file CSV
df = pd.read_csv('accident_etl.csv')  # Sostituisci con il tuo percorso

# Estrazione del mese dalla data, escludendo l'anno
df['Month'] = pd.to_datetime(df['Date'], errors='coerce').dt.month

# Rimuovi eventuali righe con valori mancanti (se ce ne sono)
df_clean = df.dropna(subset=['Month', 'Number_of_Casualties'])

# Raggruppa i dati per mese
monthly_data = df_clean.groupby('Month').agg(
    Number_of_Accidents=('Accident_Index', 'count'),
    Number_of_Fatalities=('Number_of_Casualties', 'sum')
).reset_index()

# Crea il grafico
plt.figure(figsize=(10, 6))
sns.lineplot(x='Month', y='Number_of_Accidents', data=monthly_data, color='violet', label='Number of Accidents', linewidth=2)
sns.lineplot(x='Month', y='Number_of_Fatalities', data=monthly_data, color='orange', label='Number of Fatalities', linewidth=2)

# Aggiungi etichette e titolo
plt.xlabel('Month', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.title('Accidents and Fatalities by Month', fontsize=14)

# Mostra i mesi come numeri da 01 a 12
plt.xticks(ticks=range(1, 13), labels=[f'{i:02d}' for i in range(1, 13)])

# Mostra la legenda
plt.legend()

# Salva il grafico come PNG
plt.savefig('monthly_accidents_fatalities.png', bbox_inches='tight')

# Non mostrare il grafico nel terminale
plt.close()
