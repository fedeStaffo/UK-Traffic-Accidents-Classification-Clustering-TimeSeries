import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Carica il dataset e seleziona le colonne 'Day_of_Week' e 'Number_of_Casualties'
df = pd.read_csv('reducted.csv', usecols=['Day_of_Week', 'Number_of_Casualties'])

# Definisce l'ordine dei giorni della settimana
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Assicurati che 'Day_of_Week' sia trattato come una variabile categorica con l'ordine definito
df['Day_of_Week'] = pd.Categorical(df['Day_of_Week'], categories=day_order, ordered=True)

# Conta la frequenza di ciascun giorno della settimana
day_of_week_counts = df['Day_of_Week'].value_counts().sort_index()

# Calcola la media di morti per ciascun giorno della settimana
day_of_week_deaths = df.groupby('Day_of_Week')['Number_of_Casualties'].mean().sort_index()

# Crea una colormap che va da blu (meno incidenti) a rosso (più incidenti)
norm = mcolors.Normalize(vmin=day_of_week_counts.min(), vmax=day_of_week_counts.max())
cmap = plt.cm.coolwarm  # Colormap che va dal blu al rosso

# Crea il grafico a barre verticali con i colori mappati sulla frequenza
fig, ax1 = plt.subplots(figsize=(10, 6))

# Barre verticali per il numero di incidenti
sns.barplot(x=day_of_week_counts.index, y=day_of_week_counts.values, 
            palette=cmap(norm(day_of_week_counts.values)), ax=ax1)

# Imposta il titolo e le etichette
ax1.set_title('Accidents and Average Deaths by Day of the Week', fontsize=14)
ax1.set_xlabel('Day of the Week', fontsize=12)
ax1.set_ylabel('Number of Accidents', fontsize=12)

# Crea un secondo asse y a destra per la media dei morti
ax2 = ax1.twinx()
ax2.plot(day_of_week_deaths.index, day_of_week_deaths.values, color='red', marker='o', label='Average Deaths')
ax2.set_ylabel('Average Number of Deaths', fontsize=12)
ax2.legend(loc='upper right')

# Salva il grafico come PNG
plt.tight_layout()
plt.savefig('day_of_week_accidents_and_deaths.png', bbox_inches='tight')

# Mostra il grafico
plt.show()
