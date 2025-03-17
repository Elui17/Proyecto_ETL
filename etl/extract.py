import pandas as pd
import time
from .logger import logger

def extract_data(input_file):
    start_time = time.time()
    logger.info("Extrayendo datos desde el archivo Excel con Pandas...")
    
    try:
        # 1) Cargamos los DataFrames en un diccionario
        sheets = ["film", "inventory", "rental", "customer", "store"]
        data = {sheet: pd.read_excel(input_file, sheet_name=sheet) for sheet in sheets}
        
        # 2) Limpiamos los espacios en las columnas de cada DataFrame individual
        for sheet, df in data.items():
            df.columns = [col.strip() for col in df.columns]
            data[sheet] = df
        
        duration = time.time() - start_time
        logger.info(f"✅ Datos extraídos correctamente en {duration:.2f} segundos.")
        return data

    except Exception as e:
        logger.error(f"❌ Error en la extracción de datos: {e}")
        return None
