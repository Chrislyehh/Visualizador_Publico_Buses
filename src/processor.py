import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
import os

def procesar_shapes_a_geojson(folder_input="data/gtfs", folder_output="data/processed"):
    """
    Transforma el archivo shapes.txt (puntos) en un archivo GeoJSON (líneas)
    mucho más eficiente para visualización.
    """
    path_shapes = os.path.join(folder_input, "shapes.txt")
    
    if not os.path.exists(path_shapes):
        print("❌ No se encontró shapes.txt. ¿Corriste el scraper primero?")
        return
    
    print("⏳ Procesando rutas... esto puede tardar unos segundos.")
    
    # 1. Leer shapes.txt
    # Solo leemos las columnas que necesitamos para ahorrar memoria
    df_shapes = pd.read_csv(path_shapes, usecols=['shape_id', 'shape_pt_lat', 'shape_pt_lon', 'shape_pt_sequence'])
    
    # 2. Ordenar por ID de trayecto y secuencia de puntos
    df_shapes = df_shapes.sort_values(by=['shape_id', 'shape_pt_sequence'])
    
    # 3. Convertir puntos en Líneas (Agrupamos por shape_id)
    # Creamos una lista de tuplas (lon, lat) para cada trayecto
    lines = (
        df_shapes.groupby('shape_id')
        .apply(lambda x: LineString(zip(x['shape_pt_lon'], x['shape_pt_lat'])))
    )
    
    # 4. Crear un GeoDataFrame
    gdf_rutas = gpd.GeoDataFrame(lines, columns=['geometry'], crs="EPSG:4326")
    gdf_rutas = gdf_rutas.reset_index()
    
    # 5. Guardar el resultado
    os.makedirs(folder_output, exist_ok=True)
    output_path = os.path.join(folder_output, "rutas_santiago.geojson")
    
    # Guardamos como GeoJSON (estándar para mapas web)
    gdf_rutas.to_file(output_path, driver='GeoJSON')
    
    print(f"✅ ¡Éxito! Mapa estático procesado en: {output_path}")
    return output_path