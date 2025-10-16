# Prueba Técnica FG: Pipeline de Datos

## Descripción
Este proyecto descarga datos de precios de electricidad de la API pública de Energinet, los sube a BigQuery en un dataset sandbox, y luego realiza una transformación idempotente para integrar los datos en la tabla final.

---

## Estructura del repositorio

prueba_tecnica_FG/
├─ parte2/
│ └─ downloader_energinet.py # Script Python para descargar y subir datos a BigQuery
├─ sql/
│ └─ transform.sql # Transformación SQL idempotente
├─ README.md # Este archivo
└─ .gitignore # Ignora JSON de credenciales y pycache

yaml
Copiar código

---

## Requisitos

- Python 3.9+  
- Librerías:
  - `requests`
  - `pandas`
  - `google-cloud-bigquery`  
- Cuenta de Google Cloud Platform con permisos para BigQuery:
  - `BigQuery Data Editor`
  - `BigQuery Job User`

---

## Configuración de credenciales

1. Crear una Service Account en GCP con los permisos mencionados.  
2. Descargar la clave JSON.  
3. Configurar las variables de entorno antes de ejecutar el script:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/ruta/a/tu/clave.json"
export GCP_PROJECT="tu-project-id"
⚠️ Nunca subas tu JSON de credenciales al repositorio.

Ejecución
1. Descargar y subir datos a BigQuery
bash
Copiar código
python parte2/downloader_energinet.py
Esto creará el dataset SANDBOX_apidata si no existe y subirá los datos descargados.

2. Ejecutar la transformación SQL
Abre BigQuery, copia el contenido de sql/transform.sql y ejecútalo.
La tabla final será INTEGRATION.integration_prueba_tecnica.
La transformación es idempotente: puedes ejecutarla varias veces sin generar duplicados.

Notas
El proyecto está preparado para ser reproducible: solo se necesita configurar la cuenta de servicio y las variables de entorno.

La SQL está diseñada para eliminar duplicados por PriceArea y HourUTC, tomando siempre el registro más reciente.

Mantener limpio el repositorio y no subir archivos de credenciales asegura seguridad y facilidad de revisión.# prueba_tecnica_FG
