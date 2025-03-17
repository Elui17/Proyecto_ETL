# load.py CORRECTO y DEFINITIVO para CSV
import os
import time
import pandas as pd
from etl.logger import logger

def load_data(data, output_path, cloud_provider=None, bucket_name=None):
    start_time = time.time()
    logger.info("💾 Guardando datos en archivos CSV separados...")

    try:
        os.makedirs(output_path, exist_ok=True)

        for sheet_name, df in data.items():
            output_file = os.path.join(output_path, f"{sheet_name}.csv")
            df.to_csv(output_file, index=False)
            logger.info(f"📑 Archivo '{sheet_name}.csv' guardado exitosamente.")

            if cloud_provider == "gcp":
                from etl.cloud_storage import upload_to_gcp
                gcs_key = f"processed/{sheet_name}.csv"
                logger.info(f"🚀 Subiendo '{sheet_name}.csv' a Google Cloud Storage: {gcs_key}")
                upload_to_gcp(output_file, bucket_name, gcs_key)

        duration = time.time() - start_time
        logger.info(f"✅ Proceso de guardado en CSV completado en {duration:.2f} segundos.")

    except Exception as e:
        logger.error(f"❌ Error guardando datos en CSV: {e}")
