import logging
import requests
import pyodbc

# Configuración de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def connect_to_db():
    """Conecta a la base de datos SQL Server."""
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost;'
            'DATABASE=data_testing;'
            'Trusted_Connection=yes;'
        )
        logging.info("Conexión a la base de datos exitosa.")
        return conn
    except Exception as e:
        logging.error(f"Error al conectar a la base de datos: {e}")
        raise


def fetch_data_from_api(endpoint):
    """Obtiene datos desde el endpoint API."""
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        logging.info(f"Datos extraídos correctamente desde {endpoint}.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al obtener datos desde la API: {e}")
        raise


def get_table_columns(cursor, table_name):
    """Obtiene las columnas de una tabla desde la base de datos."""
    try:
        cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
        columns = [row[0] for row in cursor.fetchall()]
        return columns
    except Exception as e:
        logging.error(f"Error al obtener columnas de la tabla {table_name}: {e}")
        raise


def insert_data_to_db(cursor, table_name, data):
    """Inserta datos en la tabla especificada."""
    if not data:
        logging.warning(f"No hay datos para insertar en {table_name}.")
        return

    try:
        # Obtener las columnas válidas de la tabla
        table_columns = get_table_columns(cursor, table_name)
        logging.info(f"Columnas detectadas en la tabla '{table_name}': {table_columns}")

        for row in data:
            # Validar que las claves del registro coincidan con las columnas de la tabla
            valid_keys = [key for key in row if key in table_columns]
            if not valid_keys:
                logging.warning(f"El registro no contiene claves válidas para la tabla {table_name}: {row}")
                continue

            placeholders = ", ".join(["?" for _ in valid_keys])
            columns = ", ".join(valid_keys)
            values = [row[key] for key in valid_keys]

            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            logging.debug(f"Consulta SQL generada: {query} con valores {values}")

            cursor.execute(query, values)
        logging.info(f"Datos insertados correctamente en la tabla {table_name}.")
    except Exception as e:
        logging.error(f"Error al insertar datos en la tabla {table_name}: {e}")
        raise


def main():
    """Función principal para ejecutar el pipeline."""
    db_connection = None
    try:
        # Conectar a la base de datos
        db_connection = connect_to_db()
        cursor = db_connection.cursor()

        # Endpoints de la API
        endpoints = {
            "users": "http://127.0.0.1:8000/users",
            "songs": "http://127.0.0.1:8000/songs",
            "listening_history": "http://127.0.0.1:8000/listening_history"
        }

        # Procesar cada tabla
        for table_name, endpoint in endpoints.items():
            logging.info(f"Procesando la tabla {table_name}...")
            data = fetch_data_from_api(endpoint)
            insert_data_to_db(cursor, table_name, data)

        # Confirmar transacciones
        db_connection.commit()
        logging.info("Pipeline completado exitosamente.")
    except Exception as e:
        logging.error(f"Error en el proceso principal: {e}")
    finally:
        if db_connection:
            db_connection.close()
            logging.info("Conexión a la base de datos cerrada.")


if __name__ == "__main__":
    main()
