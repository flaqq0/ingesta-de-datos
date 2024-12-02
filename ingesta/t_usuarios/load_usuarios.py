import os
import boto3
from botocore.exceptions import NoCredentialsError
from loguru import logger
from datetime import datetime

# Configuración de logger con milisegundos
LOG_FILE_PATH = "./logs/load_usuarios.log"
logger.add(LOG_FILE_PATH, format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}", level="INFO", rotation="10 MB")

# Variables globales
BASE_DIRECTORY = "./fakeData"  # Directorio base donde se encuentran los archivos locales
BUCKETS = "aproyecto-dev"

# Conexión a S3 usando las credenciales configuradas en ~/.aws/credentials
s3 = boto3.client('s3')

# Función para subir un archivo a S3
def upload_to_s3(file_path, bucket, s3_file_path):
    try:
        s3.upload_file(file_path, bucket, s3_file_path)
        logger.info(f"Archivo '{file_path}' subido exitosamente a '{s3_file_path}' en el bucket '{bucket}'")
    except FileNotFoundError:
        logger.error(f"El archivo '{file_path}' no fue encontrado.")
    except NoCredentialsError:
        logger.critical("Credenciales de AWS no disponibles.")
    except Exception as e:
        logger.error(f"Error desconocido al subir el archivo '{file_path}': {str(e)}")

# Función para realizar la ingesta de archivos de usuarios
def ingest():
    logger.info(f"Iniciando ingesta al bucket '{BUCKET_NAME}'.")
    start_time = datetime.now()
    processed_files = 0

    for root, dirs, files in os.walk(BASE_DIRECTORY):
        for file in files:
            if file.endswith(".json"):  # Trabajaremos con archivos JSON
                s3_file_path = f"usuarios/{file}"  # Ruta en el bucket S3
                file_path = os.path.join(root, file)
                
                # Subir archivo al bucket S3
                try:
                    logger.info(f"Procesando archivo: {file_path}")
                    upload_to_s3(file_path, BUCKET_NAME, s3_file_path)
                    processed_files += 1
                except Exception as e:
                    logger.error(f"Error al procesar el archivo '{file_path}': {str(e)}")
    
    end_time = datetime.now()
    logger.success(f"Ingesta completada. Tiempo total: {end_time - start_time}. Archivos procesados: {processed_files}")

# Llamada a la función para realizar la ingesta
ingest()