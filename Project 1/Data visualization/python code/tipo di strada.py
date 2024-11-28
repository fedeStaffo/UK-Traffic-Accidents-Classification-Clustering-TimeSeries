import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Carica il dataset e seleziona le colonne 'Road_Type' e 'Number_of_Casualties'
df = pd.read_csv('reducted.csv', usecols=['Road_Type', 'Number_of_Casualties'])

# Filtra i dati per rimuovere le righe con "Unknown"
df_clean = df[df['Road_Type'] != 'Unknown']

# Calcola la percentuale di ogni tipo di strada rispetto al totale
road_type_counts = df_clean['Road_Type'].value_counts(normalize=True) * 100

# Calcola il numero totale di morti per ciascun tipo di strada
road_type_deaths = df_clean.groupby('Road_Type')['Number_of_Casualties'].sum()

# Calcola la percentuale di morti per ciascun tipo di strada rispetto al totale delle morti
total_deaths = road_type_deaths.sum()
road_type_death_percentage = (road_type_deaths / total_deaths) * 100

# Combina i risultati in un DataFrame
data = pd.DataFrame({
    'Road_Type_Percentage': road_type_counts,
    'Death_Percentage': road_type_death_percentage
}).reset_index()

# Rinomina le colonne per chiarezza
data.columns = ['Road_Type', 'Road_Type_Percentage', 'Death_Percentage']

# Reshape per utilizzare seaborn in modo corretto (per avere due colonne separate)
data_melted = data.melt(id_vars='Road_Type', value_vars=['Road_Type_Percentage', 'Death_Percentage'],
                        var_name='Category', value_name='Percentage')

# Crea il grafico a barre con seaborn, affiancando le colonne per ogni tipo di strada
plt.figure(figsize=(12, 6))
sns.barplot(x='Road_Type', y='Percentage', hue='Category', data=data_melted, palette=['blue', 'red'])

# Imposta il titolo e le etichette
plt.title('Road Type and Death Percentage Comparison', fontsize=14)
plt.xlabel('Road Type', fontsize=10)
plt.ylabel('Percentage (%)', fontsize=10)

# Aggiungi una legenda
plt.legend(loc='upper right')

# Salva il grafico come PNG
plt.tight_layout()
plt.savefig('road_type.png', bbox_inches='tight')

# Mostra il grafico
plt.show()
