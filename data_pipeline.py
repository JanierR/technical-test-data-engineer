import requests
import csv
import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

# Configuración de logging
logging.basicConfig(
    filename="data_pipeline.log",  # Archivo donde se guardarán los logs
    level=logging.INFO,  # Nivel de logging (INFO, ERROR, etc.)
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# URLs de los endpoints
BASE_URL = "http://127.0.0.1:8000"
ENDPOINTS = {
    "tracks": f"{BASE_URL}/tracks",
    "users": f"{BASE_URL}/users",
    "listen_history": f"{BASE_URL}/listen_history"
}

# Directorio de salida
OUTPUT_DIR = "output_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_data(endpoint):
    """
    Descarga datos desde un endpoint dado.
    Maneja errores de red y responde con una lista vacía en caso de fallos.
    """
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        data = response.json()
        logging.info(f"Datos obtenidos correctamente desde {endpoint}.")
        return data.get("items", [])
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error al acceder a {endpoint}: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f"Error de conexión al acceder a {endpoint}: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        logging.error(f"Timeout al acceder a {endpoint}: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Error inesperado al acceder a {endpoint}: {req_err}")
    return []

def save_to_csv(data, filename):
    """
    Guarda una lista de diccionarios en un archivo CSV.
    Maneja errores al guardar los datos.
    """
    if not data:
        logging.warning(f"No hay datos para guardar en {filename}.")
        return

    filepath = os.path.join(OUTPUT_DIR, filename)
    try:
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            keys = data[0].keys()
            with open(filepath, mode="w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)
            logging.info(f"Datos guardados correctamente en {filepath}.")
        else:
            logging.error(f"Formato de datos incorrecto para {filename}.")
    except Exception as e:
        logging.error(f"Error al guardar los datos en {filename}: {e}")

def run_pipeline():
    """
    Ejecuta el pipeline completo.
    """
    logging.info("Iniciando el pipeline de datos...")
    for name, endpoint in ENDPOINTS.items():
        logging.info(f"Descargando datos desde {endpoint}...")
        data = fetch_data(endpoint)
        save_to_csv(data, f"{name}.csv")
    logging.info("Pipeline completado.")

if __name__ == "__main__":
    # Configurar el programador
    scheduler = BlockingScheduler()

    # Programar el pipeline para que se ejecute todos los días a las 00:00 (medianoche)
    scheduler.add_job(run_pipeline, 'cron', hour=0, minute=0)
    # scheduler.add_job(run_pipeline, 'interval', minutes=1)

    logging.info("Programador iniciado. El pipeline se ejecutará todos los días a las 00:00.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Programador detenido.")
