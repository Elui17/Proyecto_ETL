import time
from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data
from etl.logger import logger

def main():
    #ruta del archivo xlxs
    input_file = "C:/Users/User/Documents/Prueba_tecnica_Ing_Datos/data/Films_2.xlsx"
    #ruta de la carpeta donde se guardaran los archivos csv
    output_path = "C:/Users/User/Documents/Prueba_tecnica_Ing_Datos/outputs/processed_films"
    
    cloud_provider = "gcp"
    #nombre del bucket destino
    bucket_name = "etl-films-storage" 

    logger.info("🚀 Iniciando el proceso ETL...")
    total_start_time = time.time()

    data = extract_data(input_file)
    if data:
        transformed_data = transform_data(data)
        if transformed_data:
            load_data(transformed_data, output_path, cloud_provider, bucket_name)

    total_duration = time.time() - total_start_time
    logger.info(f"✅ Proceso ETL finalizado en {total_duration:.2f} segundos.")

if __name__ == "__main__":
    main()
