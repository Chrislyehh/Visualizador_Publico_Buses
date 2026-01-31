import requests
import os
import zipfile

def actualizar_gtfs_si_es_necesario(url, folder="data/gtfs"):
    """
    Esta función es el 'Portero'. Solo descarga si hay algo nuevo.
    Retorna True si hubo descarga, False si ya estábamos al día.
    """
    log_file = os.path.join(folder, "last_check.txt")
    
    # 1. Pedir cabeceras
    response = requests.head(url, allow_redirects=True)
    remote_date = response.headers.get('Last-Modified')

    # 2. Verificar si cambió
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            if f.read().strip() == remote_date:
                return False # No hay cambios

    # 3. Descargar si es nuevo
    print("Detectada nueva versión del GTFS...")
    os.makedirs(folder, exist_ok=True)
    r = requests.get(url)
    zip_path = os.path.join(folder, "gtfs.zip")
    
    with open(zip_path, 'wb') as f:
        f.write(r.content)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(folder)
        
    with open(log_file, 'w') as f:
        f.write(remote_date)
        
    return True