##📌 1. Arquitectura completa de datos

La aplicacion sigue un proceso ETL que se compone de tres fases principales:

### 🟢 Extracción (extract.py)
 Fuente: Archivo Excel (Films_2.xlsx) con múltiples hojas.
Uso de Pandas para cargar cada hoja en un diccionario de DataFrames.
Limpieza básica inicial (ajuste nombres de columnas).

### 🟡 Transformación (transform.py)
Aquí se realizan operaciones más profundas:

Limpieza inicial:

Reemplazo de valores 'NULL' por NaN.
Eliminación de columnas innecesarias (original_language_id).
Transformaciones específicas por tipo:

Conversión de columnas con fechas (DATE_COLUMNS) usando pd.to_datetime con relleno forward (método ffill).
Conversión de columnas de texto con valores numéricos sucios (extracción numérica con regex, conversión a tipo numérico).
Imputación de datos faltantes:
Columnas numéricas: imputación usando media.
Columnas categóricas: imputación proporcional o usando la moda según porcentaje de nulos (>20% proporcional, ≤20% moda).
Identificación y reporte de valores atípicos (IQR).

Manejo adicional de fechas en columnas que contienen "fecha"/"date" no especificadas en DATE_COLUMNS.

Este módulo asegura calidad, coherencia y consistencia de los datos antes de cargarlos.

### 🔵 Carga (load.py)
Almacenamiento de cada DataFrame transformado en CSV.
Guardado local en una estructura ordenada (outputs/processed_films).
Subida opcional a Google Cloud Storage (GCS).

### 🌐 Almacenamiento en la nube (cloud_storage.py)
Manejo explícito de credenciales desde variables de entorno.
Subida y confirmación de archivos en Google Cloud Storage.

## 📑 2. Estructura física (archivos/carpetas)


```bash
Prueba_tecnica_Ing_Datos/
│── data/                  # Carpeta con el archivo Films_2.xlsx
│── etl/                   # Módulos del proceso ETL
│   ├── __init__.py        # Indica que es un paquete
│   ├── extract.py         # Módulo de extracción
│   ├── transform.py       # Módulo de transformación
│   ├── load.py            # Módulo de carga
│   ├── cloud_storage.py   # Funciones para subir archivos a GCP
│   ├── logger.py          # Configuración del logging
│── outputs/               # Carpeta donde se guardarán los archivos CSV
│── pics/                  # Carpeta donde se guardan imágenes y gráficos
│── AED.py                 # Realiza un análisis exploratorio de los datos
│── main.py                # Script principal
│── info.md                # Markdown con el informe de presentación
│── requirements.txt       # Dependencias necesarias
│── mi-clave.json          # Clave de servicio GCP (NO se sube a Git)
│── README.md              # Documentación del proyecto
```

## 🧩 3. Arquetipo de la aplicación (Pipeline Modular ETL)
La aplicación sigue un arquetipo popular para procesamiento de datos:

Patrón ETL (Extract-Transform-Load) modular:
Modularidad: Código dividido en módulos especializados (extracción, transformación, carga y almacenamiento cloud).
Orientación a scripts: Scripts independientes pero interconectados, coordinados desde un script principal (main.py).
Logging robusto: El módulo logger.py centraliza y detalla el registro de acciones para seguimiento y depuración eficiente.
Integración con herramientas y estándares populares:
Python/Pandas para manipulación y análisis de datos.
Google Cloud Storage para almacenamiento escalable en la nube.
Análisis exploratorio posterior mediante Jupyter (AED.ipynb) y visualización con Power BI (Analisis_Expl_datos.pbix).

## 🧐 4. Analisis exploratorio de los datos

### 📝 Introducción

*Objetivo del análisis:* En este analisis se gusta enocntrar y explicar la relacion que existen entre las distintas tablas de datos junto a la inforamcion contenida en cada tabla.

*Contexto de los datos:* Los archivos contiene informacion de rentas de films y datos de clientes pertencientes a una videoclub con dos cedes durante el periodo de mayo de 2005 a agosto de 2005. 

### 📂 Fuente de los datos

## Fuentes de Datos

| Nombre del Archivo | Tipo de Archivo |
|---------------------|----------------|
| customer            | csv            | 
| film                | csv            | 
| inventory           | csv            | 
| rental              | csv            | 
| store               | csv            | 


### 🔍 Descripción general de los datos

*Tabla: customer*

*Cantidad total de registros*
- 1392 filas

*Número de columnas*
- 11 columnas

*Columnas y tipos de datos*
| Nombre de la columna  | Tipo de dato       |
|------------------------|--------------------|
| customer_id           | Entero (int)      |
| store_id              | Entero (int)      |
| first_name            | Cadena (string)   |
| last_name             | Cadena (string)   |
| email                 | Cadena (string)   |
| address_id            | Entero (int)      |
| active                | Entero (int)      |
| create_date           | Fecha/Hora (datetime) |
| last_update           | Fecha/Hora (datetime) |
| customer_id_old       | Cadena (string)   |
| segment               | Cadena (string)   |

*Tabla: film*

*Cantidad total de registros*
- 1000 filas

*Número de columnas*
- 13 columnas

*Columnas y tipos de datos*
| Nombre de la columna  | Tipo de dato        |
|------------------------|---------------------|
| film_id               | Entero (int)       |
| title                 | Cadena (string)    |
| description           | Cadena (string)    |
| release_year          | Entero (int)       |
| language_id           | Entero (int)       |
| rental_duration       | Entero (int)       |
| rental_rate           | Decimal (float)    |
| length                | Entero (int)       |
| replacement_cost      | Decimal (float)    |
| num_voted_users       | Entero (int)       |
| rating                | Cadena (string)    |
| special_features      | Cadena (string)    |
| last_update           | Fecha/Hora (datetime) |

*Tabla: inventory*

*Cantidad total de registros*
- 4581 filas

*Número de columnas*
- 4 columnas

*Columnas y tipos de datos*
| Nombre de la columna  | Tipo de dato       |
|------------------------|--------------------|
| inventory_id          | Entero (int)       |
| film_id              | Entero (int)       |
| store_id             | Entero (int)       |
| last_update          | Texto (string)     |

*Tabla: rental*

*Cantidad total de registros*
- 16044 filas

*Número de columnas*
- 7 columnas

*Columnas y tipos de datos*
| Nombre de la columna  | Tipo de dato       |
|------------------------|--------------------|
| rental_id            | Entero (int)       |
| rental_date         | Texto (string)     |
| inventory_id        | Entero (int)       |
| customer_id         | Entero (int)       |
| return_date        | Texto (string)     |
| staff_id            | Entero (int)       |
| last_update        | Texto (string)     |


*Tabla: store*

*Cantidad total de registros*
- 2 filas

*Número de columnas*
- 4 columnas

*Columnas y tipos de datos*
| Nombre de la columna  | Tipo de dato       |
|------------------------|--------------------|
| store_id              | Entero (int)      |
| manager_staff_id      | Entero (int)      |
| address_id            | Entero (int)      |
| last_update           | Fecha/Hora (datetime) |

### 📊 Distribuciones y visualizaciones clave

![Grafico de pastel que muestra el porcentaje de tipos de clientes por segmento](C:\Users\User\Documents\Prueba_tecnica_Ing_Datos\pics\image.png)

![Grafico de pastel que muestra el porcentaje de rentas por rating](C:\Users\User\Documents\Prueba_tecnica_Ing_Datos\pics\image2.png)

![Grafico de tablas dobles que muestra la cantidad de rentas por mes y tienda](C:\Users\User\Documents\Prueba_tecnica_Ing_Datos\pics\image3.png)

![Grafico de tablas dobles que muestra la cantidad de clientes por mes y tienda](C:\Users\User\Documents\Prueba_tecnica_Ing_Datos\pics\image4.png)

![Grafico de lineas que muestra el total de ingresos por mes](C:\Users\User\Documents\Prueba_tecnica_Ing_Datos\pics\image5.png)

![Grafico de barras que muestra el promedio de taza de renta por categoria rating](C:\Users\User\Documents\Prueba_tecnica_Ing_Datos\pics\image6.png)

### ⚠️Valores atípicos detectados:
tabla: inventory
- Columna 'store_id' tiene 4 valores atípicos (IQR)
tabla: customer
- Columna 'active' tiene 15 valores atípicos (IQR)
General
- Se encuentran datos atipicos en algunas columnas de fechas que presentan valores (añor 2006, mes 2) distintos al periodo donde se encuntran la mayoria de los datos en los archivos.
Se recomienda revisar estos valores manualmente para validar o eliminar según el contexto.

### 🔖 Insights principales encontrados
- Mas de la mitad de los clientes son de tipo consumer.
- El numero de rentas con respecto a las rentas totales, teniendo en cuenta la categoria de rating son muy similares entre si, mostrando porecentajes alrededores del 20% de representacion en las rentas totales para cada una de las categorias.
- Los meses con mayores rentas son los meses de julio y agosto, siendo muy similares las rentas entre las dos sedes para todo el periodo.
- La cantidad de clientes unicos por mes es similar para ambas sedes, teniendo un mayo numero de clientes en los meses de julio y agosto.
- El mes de mayores ingresos fue el mes de Julio, alcanzando los 20000 (tipo de moneda) durate el mes.

### Próximos pasos sugeridos:
- Análisis predictivo del comportamiento del cliente (modelo de retención).
- Segmentación de películas según la rentabilidad.
- Creación de dashboards interactivos (Power BI) para seguimiento continuo.

## ⁉ Preguntas :
### 🚩 Pregunta 1:
¿Cuáles son las categorias de películas más rentables según su frecuencia de alquiler (cantidad de alquileres) y tarifa promedio?
Las categorias de pleiculas mas rentables segun la frecuencia de alquiler y la tarifa promedio de alquiler son las clasificadas como PG-13 y NC-17, representando el 22% y 20% de las rentas, respectivamente, con un promedio de tarifa de renta, igual para ambdas categorias, de 3.1 (moneda).

### 🚩 Pregunta 2:
¿Cuál clientes son más activos en alquileres de películas (frecuencia y gasto promedio)?
Los clientes mas activos son los identificados con id_customer: 148 y 526, con un gastoo promedio por pelicula de 3.2 (moneda) y 3(moneda), y una fecuencia de renta de 46 y 45 rentas, respecivamente.

### 🚩 Pregunta 3:
¿Qué categorías de películas presentan valores mas altos en su costo de reposición (replacement_cost)?
Las peliculas que alcanzan mayores costos de reposicion con las que estan en la clasificacion PG 13, superando los 20 (moneda) en algunos valores.

### 🚩 Pregunta 4:
¿Existen tendencias o patrones claros en el tiempo respecto a la frecuencia de alquileres? 
Para el periodo existe un claro aumento en el numero de rentas hasta el mes de julio, en el mes de agosto disminuyen las el numero de rentas

### 🚩 Pregunta 5:
¿Hay diferencias significativas en patrones de alquiler por tienda?
No hay difrencias significativas entre los patrones de alquileres por tienda

## 📌 Conclusiones

1️⃣ Se identificaron valores atípicos en la base de datos, principalmente en store_id, active y algunas fechas fuera del rango esperado. 

2️⃣ Las películas más rentables son las clasificadas como PG-13 y NC-17, representando el 22% y 20% de las rentas, con una tarifa promedio de 3.1 (moneda).

3️⃣ El mes más rentable fue julio, con ingresos que alcanzaron 20,000 (moneda). Sin embargo, en agosto hubo una caída en las rentas, lo que sugiere un patrón estacional en la demanda.

4️⃣ No hay diferencias significativas entre las tiendas en términos de frecuencia de alquiler y clientes únicos, lo que indica una distribución homogénea de la demanda.

5️⃣ Se recomienda optimizar el inventario, aplicar promociones estratégicas en agosto y desarrollar modelos de predicción de comportamiento del cliente para mejorar la retención y rentabilidad. 