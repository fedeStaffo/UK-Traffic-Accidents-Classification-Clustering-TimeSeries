import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

# Read the CSV file
data = pd.read_csv("reducted.csv")

# Filter data to remove 'Unknown'
data = data[data['Road_Type'] != 'Unknown']

# Filter data to remove 'Unknown'
data = data[data['Accident_Severity'] != 'Slight']

# Map Accident_Severity to numeric values
severity_map = {"Serious": 0, "Fatal": 1}
data["Accident_Severity"] = data["Accident_Severity"].map(severity_map)

# Find unique values of Road_Type
road_types = data["Road_Type"].unique()

# Function to create the gauge chart
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

def create_gauge_chart(value, title, filename):
    # Check if the value is valid
    if not np.isfinite(value) or not (0 <= value <= 1):
        print(f"Error: invalid value ({value}) for the chart {title}")
        return

    print(f"Creating chart for {title} with average value: {value}")

    fig, ax = plt.subplots(figsize=(6, 4), subplot_kw={'projection': 'polar'})

    # Create a continuous color scale
    colors = ['#B22222', '#FF4500', '#FFC107']  # Yellow -> Intense orange -> Intense red
    cmap = LinearSegmentedColormap.from_list("CustomMap", colors)

    # Angles for the scale
    theta = np.linspace(0, np.pi, 500)  # 500 steps from 0 to pi
    radii = np.ones_like(theta)  # A constant radius to draw the scale

    # Create the colored scale
    values = np.linspace(0, 1, 500)  # Values from 0 to 1 along theta
    colors = cmap(values)  # Apply the color map

    ax.barh(radii, np.pi / 500, left=theta, color=colors, edgecolor="white", linewidth=0)

    # Position of the needle (where the average value is located)
    value_theta = np.pi * value  # Map the value to [0, pi]
    value_theta_inverted = np.pi - value_theta  # Invert the direction of the needle
    ax.plot([value_theta_inverted, value_theta_inverted], [0, 1.1], color="black", linewidth=3, zorder=5)
    value_perc = value * 100  # Convert the value to percentage
    value_perc_string = f"{value_perc:.2f}%"  # Format as percentage string with two decimal places

    # Chart title with the average value
    ax.set_title(f"{title} ({value_perc_string})", va="bottom", fontsize=14, weight="bold")

    # Labels for the scale edges
    ax.text(np.pi+0.07, 1.0, "Serious", ha="center", va="center", fontsize=12, color="black", weight="bold")
    ax.text(0-0.07, 1.0, "Fatal", ha="center", va="center", fontsize=12, color="black", weight="bold")

    # Remove axes and background
    ax.set_axis_off()

    # Save the chart
    plt.savefig(filename, bbox_inches="tight", dpi=300)
    plt.close()

# Generate charts for each road type
for road_type in road_types:
    road_data = data[data["Road_Type"] == road_type]
    
    # Calculate the average severity
    mean_severity = road_data["Accident_Severity"].mean()
    mean_severity_perc = mean_severity * 100
    
    # Debug: Print the calculated value
    print(f"Average value for {road_type}: {mean_severity_perc}%")
    
    create_gauge_chart(mean_severity, f"Road Type: {road_type}", f"{road_type}_Severity.png")
    print(f"Chart created for Road_Type: {road_type}")
