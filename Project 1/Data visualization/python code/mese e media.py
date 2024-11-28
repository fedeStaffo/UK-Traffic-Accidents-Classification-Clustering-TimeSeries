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
    Number_of_Fatalities=('Number_of_Casualties', 'mean')
).reset_index()

# Crea il grafico
fig, ax1 = plt.subplots(figsize=(10, 6))

# Grafico per il numero di incidenti (asse sinistro)
sns.lineplot(x='Month', y='Number_of_Accidents', data=monthly_data, color='violet', label='Number of Accidents', linewidth=2, ax=ax1)

# Crea un secondo asse y per il numero medio di morti (asse destro)
ax2 = ax1.twinx()
sns.lineplot(x='Month', y='Number_of_Fatalities', data=monthly_data, color='orange', label='Average Fatalities', linewidth=2, ax=ax2)

# Aggiungi etichette e titolo
ax1.set_xlabel('Month', fontsize=12)
ax1.set_ylabel('Number of Accidents', fontsize=12, color='violet')
ax2.set_ylabel('Average Fatalities', fontsize=12, color='orange')
plt.title('Accidents and Fatalities by Month', fontsize=14)

# Mostra i mesi come numeri da 01 a 12
plt.xticks(ticks=range(1, 13), labels=[f'{i:02d}' for i in range(1, 13)])

# Mostra la legenda
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Salva il grafico come PNG
plt.savefig('month.png', bbox_inches='tight')

# Non mostrare il grafico nel terminale
plt.close()
