import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carica il dataset e seleziona la colonna Weather_Conditions
df = pd.read_csv('accident_etl.csv', usecols=['Weather_Conditions'])

# Filtra i dati per rimuovere "Data missing or out of range"
df_clean = df[df['Weather_Conditions'] != 'Data missing or out of range']

# Conta la frequenza dei valori e calcola le proporzioni percentuali
condition_counts = df_clean['Weather_Conditions'].value_counts(normalize=True) * 100

# Ordina le condizioni per frequenza
sorted_conditions = condition_counts.sort_values(ascending=False)

# Usa la palette "deep" per i colori
colors = sns.color_palette("deep", len(sorted_conditions))

# Disegna il grafico a torta
plt.figure(figsize=(10, 8))
plt.pie(
    sorted_conditions, 
    labels=None,  # Rimuove le etichette dal grafico
    colors=colors, 
    startangle=90,  # Allinea la prima fetta in modo leggibile
    wedgeprops={'edgecolor': 'white'}  # Bordo bianco tra le fette
)

# Crea una legenda con etichette e percentuali
legend_labels = [f"{condition} ({percentage:.1f}%)" for condition, percentage in zip(sorted_conditions.index, sorted_conditions.values)]
plt.legend(legend_labels, title="Weather Conditions", loc='center left', bbox_to_anchor=(1, 0.5))

# Aggiungi un titolo
plt.title('Most Dangerous Weather Conditions (Percentage)', fontsize=14)

# Salva il grafico come PNG
plt.savefig('weather_conditions.png', bbox_inches='tight')

# Non mostrare il grafico nel terminale
plt.close()
