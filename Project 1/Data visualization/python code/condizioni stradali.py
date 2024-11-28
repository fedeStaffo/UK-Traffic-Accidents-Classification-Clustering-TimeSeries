import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Carica il dataset e seleziona la colonna Road_Surface_Conditions
df = pd.read_csv('accident_etl.csv', usecols=['Road_Surface_Conditions'])

# Filtra i dati per rimuovere le righe con 'Data missing or out of range'
df_clean = df[df['Road_Surface_Conditions'] != 'Data missing or out of range']

# Conta la frequenza di ogni valore nella colonna 'Road_Surface_Conditions'
condition_counts = df_clean['Road_Surface_Conditions'].value_counts()

# Calcola le percentuali per ogni categoria
percentages = (condition_counts / condition_counts.sum() * 100).round(1)

# Crea il grafico a torta con colori vivaci e ridimensiona per fare spazio alla legenda
sns.set_theme(style="whitegrid")
colors = sns.color_palette("deep", len(condition_counts))

# Disegna il grafico a torta
plt.figure(figsize=(8, 6))  # Dimensione del grafico
plt.pie(condition_counts, colors=colors)

# Crea una legenda con percentuali
legend_labels = [f"{label} ({percent}%)" for label, percent in zip(condition_counts.index, percentages)]
plt.legend(legend_labels, title='Road Surface Conditions', loc='center left', bbox_to_anchor=(1, 0.5))

# Aggiungi il titolo del grafico
plt.title('Distribution of Road Surface Conditions', fontsize=14)

# Salva il grafico come PNG
plt.savefig('surface_conditions.png', bbox_inches='tight')

# Non mostrare il grafico nel terminale
plt.close()
