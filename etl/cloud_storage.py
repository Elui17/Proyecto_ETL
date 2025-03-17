from google.cloud import storage
from etl.logger import logger

def upload_to_gcp(file_path, bucket_name, destination_blob_name):
    """Sube un archivo a Google Cloud Storage."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    try:
        blob.upload_from_filename(file_path)
        logger.info(f"✅ Archivo {file_path} subido a GCP Storage en gs://{bucket_name}/{destination_blob_name}")
    except Exception as e:
        logger.error(f"❌ Error al subir a GCP Storage: {e}")
