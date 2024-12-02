import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Leggi il file CSV
data = pd.read_csv("reducted.csv")

# Filtra i dati per rimuovere 'Unknown'
data = data[data['Road_Type'] != 'Unknown']

# Mappa Accident_Severity in valori numerici
severity_map = {"Slight": 1, "Serious": 2, "Fatal": 3}
data["Accident_Severity"] = data["Accident_Severity"].map(severity_map)

# Trova i valori unici di Road_Type
road_types = data["Road_Type"].unique()

# Funzione per creare il tachimetro
def create_gauge_chart(value, title, filename):
    # Controlla se il valore è valido
    if not np.isfinite(value) or not (1 <= value <= 3):
        print(f"Errore: valore non valido ({value}) per il grafico {title}")
        return

    print(f"Creazione del grafico per {title} con valore medio: {value}")

    fig, ax = plt.subplots(figsize=(6, 4), subplot_kw={'projection': 'polar'})

    # Definisci i colori (verde, giallo, rosso)
    colors = ['#DC3545', '#FFC107', '#28A745']  # Slight: verde, Serious: giallo, Fatal: rosso
    intervals = [1, 2, 3]  # Slight, Serious, Fatal

    # Crea il tachimetro come mezza ciambella
    for i, color in enumerate(colors):
        start = np.pi * (i / len(intervals))  # Inizia ogni colore a un'angolazione diversa
        end = np.pi * ((i + 1) / len(intervals))
        print(f"Segmento {i}: start={start}, end={end}, color={color}")
        ax.barh([1], [end - start], left=start, color=color, edgecolor="white", linewidth=1, height=0.5)

    # Calcola la posizione dell'indicatore (dove si trova il valore medio)
    value_theta = np.pi * (value - 1) / 2  # Mappa da [1, 3] a [0, pi]
    print(f"Lancetta: value_theta={value_theta}")

    # Inverti la direzione della lancetta
    value_theta_inverted = np.pi - value_theta  # Inverti la direzione della lancetta
    ax.plot([value_theta_inverted, value_theta_inverted], [0, 1.1], color="black", linewidth=3, zorder=5)  # Lancetta invertita

    # Titolo del grafico con il valore medio
    ax.set_title(f"{title} ({value:.2f})", va="bottom", fontsize=14, weight="bold")

    # Aggiungi etichette sotto il grafico
    ax.text(np.pi+0.07, 1.0, "Slight", ha="center", va="center", fontsize=12, color="black", weight="bold")  # A sinistra
    ax.text(0-0.07, 1.0, "Fatal", ha="center", va="center", fontsize=12, color="black", weight="bold")      # A destra

    # Rimuovi assi e sfondo
    ax.set_axis_off()

    # Salva il grafico
    plt.savefig(filename, bbox_inches="tight", dpi=300)
    plt.close()

# Genera i grafici per ciascun tipo di strada
for road_type in road_types:
    road_data = data[data["Road_Type"] == road_type]
    
    # Calcola la media della gravità
    mean_severity = road_data["Accident_Severity"].mean()
    
    # Debug: Stampa il valore calcolato
    print(f"Valore medio per {road_type}: {mean_severity}")
    
    create_gauge_chart(mean_severity, f"Road Type: {road_type}", f"{road_type}_Severity.png")
    print(f"Grafico creato per Road_Type: {road_type}")
