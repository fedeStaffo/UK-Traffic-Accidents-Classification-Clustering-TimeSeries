import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Leggi il file CSV
data = pd.read_csv("reducted.csv")

# Filtra i dati per rimuovere valori "Unknown"
data = data[data['Road_Type'] != 'Unknown']

# Conta il numero di incidenti per gravità e tipo di strada
severity_counts = data.groupby(["Road_Type", "Accident_Severity"]).size().reset_index(name="Count")

# Calcola il totale degli incidenti per ogni tipo di strada
total_counts = severity_counts.groupby("Road_Type")["Count"].sum().reset_index(name="Total")

# Calcola il totale generale di tutti gli incidenti
overall_total = total_counts["Total"].sum()

# Aggiungi una colonna per la percentuale del totale generale
total_counts["Overall_Percentage"] = (total_counts["Total"] / overall_total) * 100

# Unisci i conteggi totali ai dati
severity_counts = severity_counts.merge(total_counts, on="Road_Type")

# Calcola la percentuale di ogni severità rispetto al totale per tipo di strada
severity_counts["Percentage"] = (severity_counts["Count"] / severity_counts["Total"]) * 100

# Trasforma i dati in formato pivot per un grafico a barre
severity_pivot = severity_counts.pivot(index="Road_Type", columns="Accident_Severity", values="Percentage").fillna(0)

# Ordina i tipi di strada per totale incidenti (in ordine decrescente)
severity_pivot = severity_pivot.loc[total_counts.sort_values("Total", ascending=False)["Road_Type"]]

# Colori per le severità
colors = {
    "Slight": "#28a745",  # Verde
    "Serious": "#ffc107",  # Giallo
    "Fatal": "#dc3545",  # Rosso
}

# Crea il grafico a colonne sovrapposte
fig, ax = plt.subplots(figsize=(10, 6))
bottoms = np.zeros(len(severity_pivot))  # Inizializza le altezze di partenza per ogni colonna

# Disegna le barre
for severity in ["Slight", "Serious", "Fatal"]:
    bars = ax.bar(
        severity_pivot.index,
        severity_pivot[severity],
        bottom=bottoms,
        color=colors[severity],
        label=severity,
        edgecolor="black",
    )
    # Aggiungi etichette con le percentuali
    for bar, percent in zip(bars, severity_pivot[severity]):
        if percent > 0:  # Mostra solo percentuali maggiori di 0
            if severity == "Fatal":  # Percentuali sopra per Fatal
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + bar.get_y() + 2,
                    f"{percent:.1f}%",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                    color="black",
                )
            else:  # Percentuali al centro per Slight e Serious
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_y() + bar.get_height() / 2,
                    f"{percent:.1f}%",
                    ha="center",
                    va="center",
                    fontsize=9,
                    color="black",
                )
    bottoms += severity_pivot[severity]  # Aggiorna l'altezza per la prossima severità

# Aggiungi la linea per il totale percentuale degli incidenti
line_values = total_counts.sort_values("Total", ascending=False)["Overall_Percentage"].values
line, = ax.plot(severity_pivot.index, line_values, color="blue", marker="o", label="Total accidents (%)", linewidth=2, markersize=6)

# Aggiungi etichette sopra la linea blu
for i, (x, y) in enumerate(zip(severity_pivot.index, line_values)):
    ax.text(
        i + 0.1,  # Aggiungi un piccolo offset a destra
        y + 2,  # Offset verso l'alto
        f"{y:.1f}%",
        ha="center",
        va="bottom",
        fontsize=9,
        color="blue"
    )


# Aggiungi il titolo e le etichette
ax.set_title("Percentage of Incidents by Road Type and Severity", fontsize=16, fontweight="bold", pad=20)
ax.set_xlabel("Road Type", fontsize=12)
ax.set_ylabel("Percentage (%)", fontsize=12)
ax.set_ylim(0, 120)  # Scala dell'asse Y portata a 120
ax.set_yticks(range(0, 121, 20))
ax.set_yticklabels([str(i) if i != 120 else "" for i in range(0, 121, 20)])  # Nasconde il valore 120

ax.set_xticks(range(len(severity_pivot)))
ax.set_xticklabels(severity_pivot.index, rotation=45, ha="right", fontsize=10)

# Sposta la legenda fuori dal grafico
ax.legend(title="Severity", fontsize=10, loc='center left', bbox_to_anchor=(1, 0.5))

# Save the plot as PNG
plt.savefig('road_type_severity.png', bbox_inches='tight')
