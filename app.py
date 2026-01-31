import os
from src.scraper import actualizar_gtfs_si_es_necesario
from src.processor import procesar_shapes_a_geojson

def main():
    URL_GTFS = "https://www.dtpm.cl/descargas/gtfs/GTFS.zip"
    
    # CAPA 1: Ingesta (Scraper)
    hubo_cambio = actualizar_gtfs_si_es_necesario(URL_GTFS)
    
    # CAPA 2: Procesamiento
    # Si hubo cambio O si el archivo procesado no existe, procesamos.
    if hubo_cambio or not os.path.exists("data/processed/rutas_santiago.geojson"):
        print("⚙️ Generando nuevas geometrías para el mapa...")
        procesar_shapes_a_geojson()
    else:
        print("🆗 Las rutas ya están procesadas y actualizadas.")

    print("🚀 Listo para la siguiente etapa: Visualización o Tiempo Real.")

if __name__ == "__main__":
    main()