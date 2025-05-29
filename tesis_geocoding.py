import pandas as pd
import googlemaps
import folium
import time
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_excel("CLEAN_COORDS.xlsx")

# Tu clave API
API_KEY = ""
gmaps = googlemaps.Client(key=API_KEY)

# Geocodificación
coordenadas = []
for direccion in df['final_address']:
    try:
        result = gmaps.geocode(direccion)
        if result:
            loc = result[0]['geometry']['location']
            coordenadas.append((loc['lat'], loc['lng']))
        else:
            coordenadas.append((None, None))
    except Exception as e:
        print(f"Error con {direccion}: {e}")
        coordenadas.append((None, None))
    time.sleep(0.3)

# Añadir coordenadas
df[['latitud', 'longitud']] = pd.DataFrame(coordenadas, index=df.index)
df.to_excel("RESULTADOS_COORDENADAS_500.xlsx", index=False)

# Filtrar válidos
df_validos = df.dropna(subset=['latitud', 'longitud'])

# Crear mapa interactivo
mapa = folium.Map(location=[14.6349, -90.5069], zoom_start=12)
for _, row in df_validos.iterrows():
    folium.Marker(
        location=[row['latitud'], row['longitud']],
        popup=row['final_address'],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(mapa)
mapa.save("MAPA_GEOCODING_500.html")

# Gráfico de dispersión
plt.figure(figsize=(10, 6))
plt.scatter(df_validos['longitud'], df_validos['latitud'], alpha=0.6, edgecolors='k')
plt.title("Distribución de Direcciones Geocodificadas")
plt.xlabel("Longitud")
plt.ylabel("Latitud")
plt.grid(True)
plt.savefig("GRAFICO_DISPERSION.png")
plt.show()
