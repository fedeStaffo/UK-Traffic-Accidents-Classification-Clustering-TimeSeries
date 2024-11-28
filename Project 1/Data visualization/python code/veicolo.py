import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Carica il dataset e seleziona la colonna Vehicle_Type
df = pd.read_csv('reducted.csv', usecols=['Vehicle_Type'])

# Filtra i dati per rimuovere "Data missing or out of range"
df_clean = df[df['Vehicle_Type'] != 'Data missing or out of range']

# Filtra i dati per rimuovere "Car" 
# df_clean = df_clean[df_clean['Vehicle_Type'] != 'Car']

# Conta la frequenza dei valori e ordina in ordine decrescente
vehicle_counts = df_clean['Vehicle_Type'].value_counts()

# Crea una colormap che va dal rosso al verde e la inverte
norm = mcolors.Normalize(vmin=vehicle_counts.values.min(), vmax=vehicle_counts.values.max())
cmap = plt.cm.RdYlGn_r  # Colormap invertita (dal rosso al verde in ordine inverso)

# Crea il grafico a barre orizzontali
plt.figure(figsize=(10, 6))
bars = sns.barplot(x=vehicle_counts.values, y=vehicle_counts.index, palette=cmap(vehicle_counts.values / vehicle_counts.values.max()))

# Aggiungi etichette e titolo
plt.xlabel('Number of Vehicles', fontsize=12)
plt.ylabel('Vehicle Type', fontsize=12)
plt.title('Vehicle Type Distribution', fontsize=14)

# Salva il grafico come PNG
plt.savefig('vehicle_distribution.png', bbox_inches='tight')

# Non mostrare il grafico nel terminale
plt.close()
