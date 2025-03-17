import pandas as pd
import numpy as np
import re  # Para usar re.sub
import time
from etl.logger import logger

# Lista con los nombres de columnas que deben mantenerse con letras y otros símbolos
ALPHANUMERIC_CODES = ["customer_id_old", "rating"]

# Diccionario que indica las columnas de fechas para cada hoja
DATE_COLUMNS = {
    "film": ["last_update"],
    "inventory": ["last_update"],
    "rental": ["rental_date", "return_date", "last_update"],
    "customer": ["create_date", "last_update"],
    "store": ["last_update"]
}

def impute_categorical_proportionally(df, col):
    """
    Imputa valores nulos de la columna 'col' usando la distribución
    de categorías existentes (frecuencias relativas) en los datos no nulos.
    """
    serie = df[col]
    value_counts = serie.value_counts(dropna=True)
    total = value_counts.sum()

    if total == 0:
        logger.info(f"    ⚠️ Columna '{col}' está totalmente vacía, no se puede imputar proporcionalmente.")
        return df

    distribution = value_counts / total
    categorias = distribution.index
    probabilidades = distribution.values

    def random_impute(x):
        if pd.isna(x):
            return np.random.choice(categorias, p=probabilidades)
        else:
            return x

    # Aplicar la función
    df[col] = serie.apply(random_impute)
    return df


def transform_data(data):
    """
    Aplica un pipeline de transformaciones a un diccionario de DataFrames.
    Cada clave del diccionario se asume como nombre de hoja (sheet) y su valor un DataFrame.
    """

    logger.info("🔄 Iniciando transformación avanzada de los datos...")
    start_time = time.time()

    try:
        for sheet_name, df in data.items():
            initial_count = len(df)
            logger.info(f"🔹 Transformando hoja: {sheet_name} (registros iniciales: {initial_count})")

            # -----------------------------------------------------------------
            # PASO 1: Reemplazar 'NULL' con NaN, revisar estadísticas y eliminar filas vacías
            # -----------------------------------------------------------------
            df.replace(r'(?i)^\s*NULL\s*$', np.nan, regex=True, inplace=True)

            for columna in df.columns:
                nulos = df[columna].isnull().sum()
                tipos_frecuentes = df[columna].map(type).mode()
                tipo_mas_comun = tipos_frecuentes[0].__name__ if not tipos_frecuentes.empty else 'Desconocido'
                valores_diferentes_tipo = df[columna].map(lambda x: type(x).__name__ != tipo_mas_comun).sum()

                logger.info(
                    f"  🔸 Columna '{columna}': "
                    f"Nulos = {nulos}, "
                    f"Tipo más común = {tipo_mas_comun}, "
                    f"Valores distintos al tipo común = {valores_diferentes_tipo}"
                )

            

            # Eliminar filas completamente vacías
            # Asegurar que los nombres de las columnas no tengan espacios ocultos
            df.columns = df.columns.str.strip()

            # Eliminar la columna "original_language_id" en la hoja "film"
            df.drop(columns=["original_language_id"], inplace=True, errors="ignore")

            # -----------------------------------------------------------------
            # PASO 2: Convertir a fecha las columnas indicadas en DATE_COLUMNS (Forward Fill si hay nulos)
            # -----------------------------------------------------------------
            if sheet_name in DATE_COLUMNS:
                for date_col in DATE_COLUMNS[sheet_name]:
                    if date_col in df.columns:
                        # Limpiar string y quitar espacios
                        df[date_col] = df[date_col].astype(str).str.strip()

                        # Intentar convertir al formato "YYYY-MM-DD HH:MM:SS"
                        df[date_col] = pd.to_datetime(
                            df[date_col],
                            format="%Y-%m-%d %H:%M:%S",
                            errors='coerce'
                        )

                        # Si existen valores nulos, se rellenan con la fila anterior
                        df[date_col].fillna(method='ffill', inplace=True)

                        # Si las primeras filas o la columna entera siguen nulas, usar 1900-01-01
                        df[date_col].fillna(pd.to_datetime('1900-01-01'), inplace=True)

                        # Reemplazar solo los valores nulos en 'return_date' con los de 'last_update'
                        if sheet_name == "rental" and "return_date" in df.columns and "last_update" in df.columns:
                           df.loc[df["return_date"].isna(), "return_date"] = df["last_update"]
                           logger.info(f"🔄 Valores nulos en 'return_date' reemplazados con 'last_update' en la hoja '{sheet_name}'.")


                        logger.info(f"📅 Columna '{date_col}' en hoja '{sheet_name}' convertida a datetime (Forward Fill).")

            # -----------------------------------------------------------------
            # PASO 3: Identificar y convertir a numéricas las columnas 'object' 
            #         (saltando las que estén en ALPHANUMERIC_CODES).
            # -----------------------------------------------------------------
            object_cols = df.select_dtypes(include=['object']).columns
            for col in object_cols:
                if col in ALPHANUMERIC_CODES:
                    logger.info(f"🔍 Saltando limpieza de '{col}' (columna alfanumérica).")
                    continue

                # Si hay dígitos, podría ser numérica sucia
                if df[col].dropna().astype(str).str.contains(r'\d', regex=True).any():
                    logger.info(f"🧹 Columna '{col}' parece numérica sucia (contiene dígitos). Limpiándola...")

                    # Eliminar caracteres no numéricos (excepto '.')
                    df[col] = df[col].apply(
                        lambda x: re.sub(r'[^0-9.]', '', x) if isinstance(x, str) else x
                    )

                    # Convertir a numérico
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    logger.info(f"🧹 Columna '{col}' convertida a tipo numérico.")

            # -----------------------------------------------------------------
            # PASO 4: Imputar columnas numéricas (con la media)
            # -----------------------------------------------------------------
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                media_valor = df[col].mean()
                df[col].fillna(media_valor, inplace=True)
                logger.info(f"   🔄 Imputando nulos en '{col}' con la media = {media_valor}.")

            # -----------------------------------------------------------------
            # PASO 5: Imputar columnas categóricas
            #         - Si la proporción de nulos > 20%, usar imputación proporcional
            #         - De lo contrario, usar la moda
            # -----------------------------------------------------------------
            object_cols = df.select_dtypes(include=['object']).columns
            for col in object_cols:
                num_nulls = df[col].isnull().sum()
                num_non_nulls = df[col].notnull().sum()
                total_vals = num_nulls + num_non_nulls

                if total_vals == 0:
                    logger.info(f"    ⚠️ Columna '{col}' está totalmente vacía, se omite.")
                    continue

                null_ratio = num_nulls / total_vals
                logger.info(
                    f"    → Columna '{col}': nulos={num_nulls}, total={total_vals}, ratio={null_ratio:.1%}"
                )

                if null_ratio > 0.2:
                    logger.info(f"      🔄 Imputando '{col}' proporcionalmente (tiene {null_ratio:.1%} de nulos).")
                    df = impute_categorical_proportionally(df, col)
                else:
                    if df[col].notnull().sum() > 0:
                        moda = df[col].mode(dropna=True)[0]
                        df[col].fillna(moda, inplace=True)
                        logger.info(f"      🔄 Imputando '{col}' con la moda = '{moda}'.")
                    else:
                        logger.info(f"      ⚠️ Columna '{col}' está 100% vacía, sin imputación.")

            # -----------------------------------------------------------------
            # PASO 6: Corrección de fechas que no estén en DATE_COLUMNS
            #         (para otras columnas con 'fecha'/'date' en su nombre)
            # -----------------------------------------------------------------
            other_date_cols = [c for c in df.columns if ('fecha' in c.lower() or 'date' in c.lower()) 
                               and c not in DATE_COLUMNS.get(sheet_name, [])]

            for date_col in other_date_cols:
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                if df[date_col].isnull().any():
                    if df[date_col].dropna().empty:
                        default_date = pd.to_datetime('1900-01-01')
                        df[date_col].fillna(default_date, inplace=True)
                    else:
                        most_common_date = df[date_col].mode()[0]
                        df[date_col].fillna(most_common_date, inplace=True)
                logger.info(f"↪️ Columna '{date_col}' (fecha extra) procesada con fallback.")

            # -----------------------------------------------------------------
            # PASO 7: Detección (solo reporte) de valores atípicos con IQR
            # -----------------------------------------------------------------
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            outlier_report = {}
            for col in numeric_cols:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
                outlier_report[col] = len(outliers)

            for col, count in outlier_report.items():
                if count > 0:
                    logger.info(f"⚠️ Columna '{col}' tiene {count} valores atípicos (IQR).")

            # -----------------------------------------------------------------
            # PASO 8: Resumen final de la hoja
            # -----------------------------------------------------------------
            final_count = len(df)
            logger.info(f"🔄 Hoja '{sheet_name}' transformada.")
            logger.info(f"   Registros antes: {initial_count}, después: {final_count}")

            data[sheet_name] = df

        end_time = time.time()
        elapsed_time = round(end_time - start_time, 2)
        logger.info(f"✅ Transformación avanzada completa. Tiempo total: {elapsed_time} segundos.")
        return data

    except Exception as e:
        logger.error(f"❌ Error durante la transformación: {e}")
        return None
