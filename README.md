# Prueba Técnica FG: Pipeline de Datos
## Descripción

Este repositorio cuenta con varios apartados de un ejercicio practico que busca descargar datos de precios de electricidad de la API pública de Energinet, los sube a BigQuery en un dataset sandbox, y luego realiza una transformación idempotente para integrar los datos en la tabla final.

Además, la parte 3 cuenta con un DAG de Airflow para orquestacion de tareas.

- Estructura del repositorio

Python_BQ/downloader_energinet.py - 1) Tienes que crear un script de Python que se conecte a una API y se descargue los datos (con 100 registros más que suficiente). 
Tiene que haber una clase para descargar de la API y otra para subirla a BigQuery. Haz un commit con esta parte y súbelo al repositorio como “parte2” (puedes hacer los commits que quieras pero indicando cada parte) 

BQ_Dataset/elspot_prices.csv - 2) Los resultados de la conexión a la API los tienes que cargar en un DATASET que te crees en Bigquery. 
a) El Dataset que reciba los datos de la API debe seguir esta nomenclatura: SANDBOX_<nombre de tu aplicación> 
Para esta parte, cuando lo tengas, puedes adjuntar captura de pantalla y subir el fichero que genera la tabla al repositorio. 

sql/transform.sql
    integration_prueba_tecnica.csv - 3) Vas a transformar los datos del sandbox. Dentro del repositorio, debe haber una carpeta sql/ con al menos un archivo: 
1. transform.sql: Este archivo debe contener una única consulta SQL que: ○ Lea los datos de la tabla almacenada en SANDBOX_<nombre de tu aplicación> 
  ○  Realice alguna transformación simple. Por ejemplo: eliminar posibles duplicados del día, añadir una columna con la fecha en que se 
  ejecuta la transformación… 
  ○  Inserte el resultado transformado en la tabla 
  INTEGRATION.integration_prueba_tecnica. 
  ○ Requisito clave: La consulta debe ser idempotente. Es decir, si se ejecuta varias veces sobre los mismos datos crudos del día, el 
  resultado en la tabla final debe ser el mismo (no debe generar 
  duplicados).

Parte3_Airflow/airflow_dag.py - Contiene el achivo py y el pdf donde se explica cada paso con pantallazos comprobando que funciona correctamente.

## Requisitos

- Python 3.9+

- Librerías: requests, pandas, google-cloud-bigquery

- Cuenta de Google Cloud Platform con permisos para BigQuery:

- BigQuery Data Editor

- BigQuery Job User

- Configuración de credenciales

- Crear una Service Account en GCP con los permisos mencionados.

- Descargar la clave JSON.

- Configurar las variables de entorno antes de ejecutar el script:

export GOOGLE_APPLICATION_CREDENTIALS="/ruta/a/tu/clave.json"
<<<<<<< HEAD

=======
>>>>>>> 113f7a1 (Todos)
export GCP_PROJECT="tu-project-id"

⚠️ Nunca subas tu JSON de credenciales al repositorio.

## Ejecución

- Descargar y subir datos a BigQuery:

- python parte2/prueba_tecnica.ipynb

- Esto creará el dataset SANDBOX_apidata si no existe y subirá los datos descargados.

Ejecutar la transformación SQL:

Abre BigQuery, copia el contenido de sql/transform.sql y ejecútalo.
La tabla final será INTEGRATION.integration_prueba_tecnica.
La transformación es idempotente: puedes ejecutarla varias veces sin generar duplicados.

<<<<<<< HEAD
Qué hace

- Crea la tabla final si no existe (INTEGRATION.integration_prueba_tecnica).

- Convierte HourUTC de DATETIME a TIMESTAMP para que el MERGE funcione sin errores.

- Elimina duplicados usando ROW_NUMBER() por PriceArea y HourUTC.

- Mantiene idempotencia, puedes ejecutar varias veces sin duplicar datos.

- Añade transform_date para registrar cuándo se hizo la transformación.
=======
Notas

El proyecto está preparado para ser reproducible: solo se necesita configurar la cuenta de servicio y las variables de entorno.

La SQL está diseñada para eliminar duplicados por PriceArea y HourUTC, tomando siempre el registro más reciente.

Mantener limpio el repositorio y no subir archivos de credenciales asegura seguridad y facilidad de revisión.
>>>>>>> 113f7a1 (Todos)
