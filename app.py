import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import os

st.set_page_config(page_title="Red Metropolitana", layout="wide")

st.title("🚌 Visualizador de Transporte Público")

RUTA_GEOJSON = "data/processed/rutas_santiago.geojson"

if os.path.exists(RUTA_GEOJSON):
    # Cargamos sin caché por ahora para debuguear
    gdf = gpd.read_file(RUTA_GEOJSON)
    
    # MOSTRAR COLUMNAS PARA DEBUG (Solo para nosotros)
    st.write(f"Columnas detectadas en el archivo: `{gdf.columns.tolist()}`")

    # Verificar si la columna existe antes de usarla
    columna_nombre = 'route_short_name'
    
    if columna_nombre in gdf.columns:
        # Asegurarse de que no haya nulos y convertir a texto
        recorridos = sorted(gdf[columna_nombre].dropna().unique().astype(str))
        
        seleccion = st.multiselect(
            "Selecciona recorridos:", 
            options=recorridos, 
            default=recorridos[:2] if len(recorridos) > 0 else None
        )

        # Mapa
        m = folium.Map(location=[-33.4489, -70.6693], zoom_start=12, tiles="cartodbpositron")
        
        gdf_filtrado = gdf[gdf[columna_nombre].isin(seleccion)]
        
        for _, fila in gdf_filtrado.iterrows():
            # Manejo de color seguro
            color = f"#{fila['route_color']}" if 'route_color' in fila and str(fila['route_color']) != 'nan' else 'blue'
            
            # Dibujar línea
            folium.GeoJson(
                fila['geometry'],
                style_function=lambda x, color=color: {'color': color, 'weight': 3}
            ).add_to(m)

        st_folium(m, width=1200, height=600)
    else:
        st.error(f"⚠️ La columna '{columna_nombre}' no se encuentra. Revisa el Processor.")
else:
    st.warning("No hay datos. Ejecuta el scraper/processor primero.")