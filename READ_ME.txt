# 📌 ETL Films2 - Proceso ETL con Python y Google Cloud Storage
Este proyecto implementa un **ETL** (Extracción, Transformación y Carga) 

---

## 🎯 1. Estructura del Proyecto

```
Proyecto_ETL/
│── data/                  # Carpeta con el archivo Films_2.xlsx
│── etl/                   # Módulos del proceso ETL
│   ├── __init__.py        # Indica que es un paquete
│   ├── extract.py         # Módulo de extracción
│   ├── transform.py       # Módulo de transformación
│   ├── load.py            # Módulo de carga
│   ├── cloud_storage.py   # Funciones para subir archivos a GCP
│   ├── logger.py          # Configuración del logging
│── outputs/               # Carpeta donde se guardarán los archivos CSV
│── main.py                # Script principal
│── AED.py                 # Realiza un analisis exploratorio de los datos
│── requirements.txt       # Dependencias necesarias
│── mi-clave.json          # Clave de servicio GCP (NO subir a GitHub)
│── README.md              # Documentación del proyecto
```

---


## ⚡ 2. Requisitos
Antes de ejecutar el código, asegúrate de tener instaladas las siguientes dependencias:

### 📌 **Instalar dependencias**
Ejecuta el siguiente comando en la terminal dentro de tu entorno virtual:

```bash
pip install -r requirements.txt
```
Si no tienes un archivo `requirements.txt`, instala las librerías manualmente:

```bash
pip install pandas google-cloud-storage openpyxl boto3
```


---

## ⚙️ 3. Configurar Google Cloud Storage
Este proyecto almacena los archivos procesados en un **bucket de Google Cloud Storage**.

### 📌 **1️⃣ Crear un bucket en Google Cloud**
1. Ir a [Google Cloud Storage](https://console.cloud.google.com/storage/browser)
2. Hacer clic en **Crear Bucket**
3. **Asignar un nombre único**, ejemplo: `etl-films-storage`
4. Seleccionar la ubicación: `us-central1` (o la más cercana a ti)
5. Clase de almacenamiento: `Standard`
6. Control de acceso: `Uniforme`
7. **Crear el bucket**

### 📌 **2️⃣ Generar credenciales JSON**
1. Ir a [Cuentas de servicio](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. Seleccionar el **proyecto correcto** (`pb-ing-datos-luis-suarez`)
3. Ir a la cuenta de servicio `etl-storage-service`
4. Ir a la pestaña **Claves** → **Agregar clave** → **Crear clave JSON**
5. Se descargará un archivo `.json`. **Mueve este archivo a la carpeta del proyecto.**
6. Renómbralo a `mi-clave.json`

### 📌 **3️⃣ Configurar la variable de entorno**
Ejecuta este comando en **PowerShell** para que Python pueda usar las credenciales:

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="{direccion a su archivo json}"
```

Si quieres configurarlo de forma permanente, usa este comando:

```powershell
[System.Environment]::SetEnvironmentVariable("GOOGLE_APPLICATION_CREDENTIALS", "{direccion a su archivo json}", "Machine")
```

Reinicia VS Code o la terminal después de hacer esto.

---

## 🚀 4. Ejecutar la ETL
Una vez configurado todo, ejecuta:

```powershell
python main.py
```

Esto hará lo siguiente:
1. **Extrae los datos** desde `Films_2.xlsx`
2. **Transforma los datos** eliminando nulos y duplicados, sutituyendo los datos nulos aleatoriamente por uno de los valores
     no nulos en la columna teniendo en cuenta que la frecuencia con la que aparece el valor en el total de los valores no nulos.
3. **Guarda los archivos en CSV** en `outputs/processed_films`
4. **Sube los archivos procesados a Google Cloud Storage** en `{ruta a cua carpeta de la nube de google}`

---

## ✅ 5. Verificar la subida en Google Cloud
Después de ejecutar la ETL, revisa los archivos en Google Cloud Storage:

1. **Ir a [Google Cloud Storage](https://console.cloud.google.com/storage/browser)**
2. **Abrir el bucket donde establecio que se guaradaran los archivos**
3. **Verificar que los archivos `.csv` están en la carpeta destino**

Si todo salió bien, verás logs como este en la terminal:

```
✅ Archivo film.csv subido a GCP Storage en {ruta a cua carpeta de la nube de google}
✅ Archivo inventory.csv subido a GCP Storage en {ruta a cua carpeta de la nube de google}
✅ Proceso ETL finalizado en {tiempo que demoro la ejecucion} segundos.
```

---

## 🔧 6. Solución de errores comunes

### ❌ `google.auth.exceptions.DefaultCredentialsError`
👉 **Solución:** Asegúrate de que la variable de entorno `GOOGLE_APPLICATION_CREDENTIALS` está configurada correctamente:

```powershell
echo $env:GOOGLE_APPLICATION_CREDENTIALS
```
Si no devuelve la ruta del JSON, vuelve a configurarlo.

### ❌ `google.cloud.exceptions.Forbidden`
👉 **Solución:** Verifica que la **cuenta de servicio** tiene permisos de "Administrador de almacenamiento" en Google Cloud.

### ❌ `FileNotFoundError: No such file or directory` para `Films_2.xlsx`
👉 **Solución:** Asegúrate de que el archivo está en la carpeta `data/`.

---

## 🎉 7. ¡Listo para usar!
Si seguiste todos los pasos, tu ETL ya debería estar funcionando correctamente y subiendo los archivos procesados a **Google Cloud Storage**. 🚀

📌 **Si tienes dudas, revisa los logs en la terminal o en `logger.py`.**
