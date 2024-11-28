import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Carica il file CSV con i dati degli incidenti
file_path = 'reducted.csv'  # Sostituisci con il percorso del tuo file CSV
df = pd.read_csv(file_path)

# Carica il file shapefile con i confini dei distretti
# Sostituisci con il percorso del file shapefile
shapefile_path = 'C:/Users/emsar/OneDrive/Desktop/Progetto Data science/UK/LAD_MAY_2024_UK_BUC.shp'
districts_shapefile = gpd.read_file(shapefile_path)

# Imposta il CRS su EPSG:4326 per entrambi i GeoDataFrame
districts_shapefile = districts_shapefile.to_crs('EPSG:4326')
df = gpd.GeoDataFrame(df, geometry=gpd.GeoSeries.from_xy(df['Longitude'], df['Latitude']), crs='EPSG:4326')

# Verifica la validità delle geometrie e rimuove quelle non valide
districts_shapefile = districts_shapefile[districts_shapefile.is_valid]

# Aggrega gli incidenti per distretto
incident_counts = df['Local_Authority_(District)'].value_counts()

# Associa i dati degli incidenti ai distretti
districts_shapefile['incident_count'] = districts_shapefile['LAD24NM'].map(incident_counts).fillna(0)

# Crea il grafico della mappa coropletica
fig, ax = plt.subplots(figsize=(16, 14))  # Aumentato la dimensione della mappa

# Plot della mappa coropletica con la palette YlOrRd (tonalità scure per valori bassi e chiare per valori alti)
districts_shapefile.plot(column='incident_count', cmap='YlOrRd', legend=True,  # Cambiato cmap
                         legend_kwds={'label': "Number of Accidents by District",
                                      'orientation': "horizontal"},
                         edgecolor='black', ax=ax)

# Imposta l'aspetto
ax.set_aspect('equal')

# Aggiungi il titolo
plt.title('Accident Density by District in the United Kingdom', fontsize=16)  # Maggiore dimensione del titolo
plt.axis('off')  # Rimuovi assi

# Salva il grafico come PNG
plt.savefig('uk.png', bbox_inches='tight', dpi=300)
plt.show()

# Genera una tabella con i distretti e il loro numero di incidenti
incident_table = incident_counts.reset_index()
incident_table.columns = ['District', 'Incident Count']  # Rinomina le colonne per chiarezza

# Stampa la tabella
print(incident_table)

# Salva la tabella come CSV
incident_table.to_csv('incident_counts_by_district.csv', index=False)
