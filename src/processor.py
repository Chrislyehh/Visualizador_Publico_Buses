import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
import os

def procesar_shapes_a_geojson(folder_input="data/gtfs", folder_output="data/processed"):
    print("🚀 INICIANDO PROCESADOR VERSION 3.0 (SUPER MERGE)")
    
    # Rutas de archivos
    f_shapes = os.path.join(folder_input, "shapes.txt")
    f_trips = os.path.join(folder_input, "trips.txt")
    f_routes = os.path.join(folder_input, "routes.txt")

    # Leer archivos
    shapes = pd.read_csv(f_shapes)
    trips = pd.read_csv(f_trips)
    routes = pd.read_csv(f_routes)

    # UNIÓN PASO A PASO
    # 1. Unir trips con routes
    meta_recorridos = pd.merge(trips[['route_id', 'shape_id']], 
                               routes[['route_id', 'route_short_name', 'route_color']], 
                               on='route_id', how='left').drop_duplicates('shape_id')

    # 2. Crear las líneas
    shapes = shapes.sort_values(by=['shape_id', 'shape_pt_sequence'])
    gdf_list = []
    for sid, group in shapes.groupby('shape_id'):
        if len(group) > 1:
            geom = LineString(zip(group['shape_pt_lon'], group['shape_pt_lat']))
            gdf_list.append({'shape_id': sid, 'geometry': geom})
    
    gdf_final = gpd.GeoDataFrame(gdf_list, crs="EPSG:4326")

    # 3. EL MOMENTO DE LA VERDAD: Pegamos la metadata
    gdf_final = gdf_final.merge(meta_recorridos, on='shape_id', how='left')

    # RELLENO FORZOSO (Si esto no está, Streamlit fallará)
    if 'route_short_name' not in gdf_final.columns:
        gdf_final['route_short_name'] = 'DESCONOCIDO'
    if 'route_color' not in gdf_final.columns:
        gdf_final['route_color'] = '808080'

    # Guardar
    os.makedirs(folder_output, exist_ok=True)
    ruta_destino = os.path.join(folder_output, "rutas_santiago.geojson")
    
    # Borrar archivo viejo si existe antes de guardar
    if os.path.exists(ruta_destino):
        os.remove(ruta_destino)
        
    gdf_final.to_file(ruta_destino, driver='GeoJSON')
    print(f"🔥 ARCHIVO GUARDADO. COLUMNAS: {gdf_final.columns.tolist()}")