import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LogNorm
import matplotlib.cm as cm
import warnings

warnings.filterwarnings('ignore')

# 1. COVID-19 Daten laden
print("Lade COVID-19 Daten...")
url_covid = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
df_covid = pd.read_csv(url_covid, usecols=['location', 'date', 'total_cases'])

# Datum konvertieren
df_covid['date'] = pd.to_datetime(df_covid['date'])

# FILTER: Nur das Jahr 2021
start_date = '2020-02-15'
end_date = '2020-06-30'
df_covid = df_covid[(df_covid['date'] >= start_date) & (df_covid['date'] <= end_date)]


# Wir speichern das genaue Datum als Text für den Titel der Animation (z.B. "2021-08-16")
df_covid['Week_Date'] = df_covid['date'].dt.strftime('%Y-%m-%d')

# Nullen durch 1 ersetzen (für die LogNorm Skala)
df_covid['total_cases'] = df_covid['total_cases'].fillna(1).replace(0, 1)

# 2. Weltkarte laden und robust umbenennen
print("Lade Weltkarte...")
url_map = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
world = gpd.read_file(url_map)

# Der kugelsichere Sucher
moegliche_spalten_namen = ['ADMIN', 'name', 'NAME', 'sovereignt', 'admin']
for spalte in moegliche_spalten_namen:
    if spalte in world.columns:
        world = world.rename(columns={spalte: 'location'})
        break

# Namensabweichungen korrigieren
replacements = {
    'United States of America': 'United States',
    'Dem. Rep. Congo': 'Democratic Republic of Congo',
    'Central African Rep.': 'Central African Republic'
}
world['location'] = world['location'].replace(replacements)

# 3. Setup für die Animation
# Wir sortieren die verfügbaren Wochen chronologisch
existing_weeks = sorted(df_covid['Week_Date'].unique())

fig, ax = plt.subplots(1, 1, figsize=(15, 8))
cmap = cm.viridis

# Farbskala an das Jahr 2021 anpassen
norm = LogNorm(vmin=1, vmax=df_covid['total_cases'].max()) 

sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
cbar = fig.colorbar(sm, ax=ax, orientation='horizontal', fraction=0.046, pad=0.04)
cbar.set_label('Total Confirmed COVID-19 Cases (Logarithmische Skala)', fontsize=12)

def update(frame_week):
    ax.clear()
    ax.set_axis_off()
    ax.set_title(f'Globale COVID-19 Fälle (Stand: {frame_week})', fontsize=22, pad=20, fontweight='bold')
    
    current_data = df_covid[df_covid['Week_Date'] == frame_week]
    merged = world.merge(current_data, on='location', how='left')
    
    # Basis-Karte (grau)
    world.plot(ax=ax, color='#e0e0e0', edgecolor='black', linewidth=0.2)
    # Eingefärbte Karte (rot)
    merged.plot(column='total_cases', ax=ax, cmap=cmap, norm=norm, 
                edgecolor='black', linewidth=0.2, missing_kwds={'color': 'none'})

# 4. Animation speichern
print(f"Generiere wöchentliche Animation für {len(existing_weeks)} Wochen (Jahr 2021)...")
ani = animation.FuncAnimation(fig, update, frames=existing_weeks, blit=False)

gif_name = 'covid_spread_2021_weekly.gif'
# fps=5 bedeutet: 5 Wochen (Bilder) pro Sekunde. Die 52 Wochen dauern also gut 10 Sekunden.
ani.save(gif_name, writer=animation.PillowWriter(fps=5))
print(f"Erfolg! Gespeichert als {gif_name}")