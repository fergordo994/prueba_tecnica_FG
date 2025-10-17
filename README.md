# Prueba Técnica FG: Pipeline de Datos
## Descripción

Este repositorio cuenta con varios apartados de un ejercicio practico que busca descargar datos de precios de electricidad de la API pública de Energinet, los sube a BigQuery en un dataset sandbox, y luego realiza una transformación idempotente para integrar los datos en la tabla final.

Además, la parte 3 cuenta con un DAG de Airflow para orquestacion de tareas.

# Estructura del repositorio

- Python_BQ/downloader_energinet.py - Apartado 1 del Ejercicio 2.

- BQ_Dataset/elspot_prices.csv - Apartado 2 del Ejercicio 2.

- sql/transform.sql - Apartado 3 del ejercicio 2.

- Parte3_Airflow/airflow_dag.py - Todos los apartados del Ejercicio 3. Contiene el achivo py y el pdf donde se explica cada paso con pantallazos comprobando que funciona correctamente. Además, un pantallazo donde se muestra como hemos lanzado la UI version y lo podemos ver desde la pagina web en local.

## Requisitos

- Python 3.9+

- Librerías: requests, pandas, google-cloud-bigquery

- Cuenta de Google Cloud Platform con permisos para BigQuery:

    - BigQuery Data Editor

    - BigQuery Job User

- Configuración de credenciales:

    - Crear una Service Account en GCP con los permisos mencionados.

    - Descargar la clave JSON.

    - Configurar las variables de entorno antes de ejecutar el script:

        export GOOGLE_APPLICATION_CREDENTIALS="/ruta/a/tu/clave.json"

        export GCP_PROJECT="tu-project-id"

⚠️ Nunca subas tu JSON de credenciales al repositorio.

## Ejecución

- Descargar y subir datos a BigQuery:

- python Python_BQ/downloader_energinet.py

- Esto creará el dataset SANDBOX_apidata si no existe y subirá los datos descargados.

Ejecutar la transformación SQL:

Abre BigQuery, copia el contenido de sql/transform.sql en una nuecva query y ejecútalo.
La tabla final será INTEGRATION.integration_prueba_tecnica.
La transformación es idempotente: puedes ejecutarla varias veces sin generar duplicados.


Qué hace

- Crea la tabla final si no existe (INTEGRATION.integration_prueba_tecnica).

- Convierte HourUTC de DATETIME a TIMESTAMP para que el MERGE funcione sin errores.

- Elimina duplicados usando ROW_NUMBER() por PriceArea y HourUTC.

- Mantiene idempotencia, puedes ejecutar varias veces sin duplicar datos.

- Añade transform_date para registrar cuándo se hizo la transformación.


# Parte 3: Airflow DAG

Hemos definido un DAG llamado test que se ejecuta cada día a las 3:00 UTC.

Argumentos por defecto:

from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(1900, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}


## Tareas incluidas:

start y end (DummyOperator)

Lista de tareas task_n donde las tareas pares dependen de todas las impares.

Operador TimeDiff que recibe una fecha (diff_date) y muestra la diferencia con la fecha actual.

## Para probarlo localmente:

### Listar DAGs

airflow dags list

### Ver grafo de un DAG
airflow dags show test

### Ejecutar la tarea de la diferencia horaria
airflow tasks test test time_diff_task 2025-10-17

## Requisitos de Airflow:

pip install apache-airflow
pip install graphviz  # Para visualizar DAGs

# Notas

El proyecto está preparado para ser reproducible: solo se necesita configurar la cuenta de servicio y las variables de entorno.

Mantener limpio el repositorio y no subir archivos de credenciales asegura seguridad y facilidad de revisión.

La SQL y el DAG son idempotentes y seguros para re-ejecuciones.
