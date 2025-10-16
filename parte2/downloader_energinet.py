
import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

class EnerginetAPIClient:
    """Descarga registros del dataset Elspotprices de Energinet."""
    BASE_URL = "https://api.energidataservice.dk/dataset/Elspotprices"

    def fetch_prices(self, start: str, end: str, limit: int = 100):
        """Devuelve la lista de records JSON entre start y end (YYYY-MM-DD)."""
        params = {"start": start, "end": end, "limit": limit}
        r = requests.get(self.BASE_URL, params=params, timeout=20)
        r.raise_for_status()
        js = r.json()
        records = js.get("records", [])
        return records

    def records_to_df(self, records):
        """Normaliza los records en un DataFrame (limpieza mínima)."""
        if not records:
            return pd.DataFrame()
        df = pd.json_normalize(records)
        if "HourUTC" in df.columns:
            df["HourUTC"] = pd.to_datetime(df["HourUTC"])
        for col in ["SpotPriceDKK", "SpotPriceEUR"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        df["ingest_timestamp"] = pd.Timestamp.utcnow()
        return df

class BigQueryUploader:
    """Sube DataFrame a BigQuery, crea dataset/tabla si hace falta."""
    def __init__(self, project_id: str, dataset_id: str, location: str = "US"):
        self.project = project_id
        self.dataset = dataset_id
        self.location = location
        self.client = bigquery.Client(project=self.project)

    def ensure_dataset(self):
        dataset_id = f"{self.project}.{self.dataset}"
        try:
            self.client.get_dataset(dataset_id)
            print(f"Dataset {dataset_id} ya existe.")
        except NotFound:
            ds = bigquery.Dataset(dataset_id)
            ds.location = self.location
            self.client.create_dataset(ds)
            print(f"Dataset {dataset_id} creado.")

    def upload_dataframe(self, df: pd.DataFrame, table_name: str, write_disposition="WRITE_APPEND"):
        if df.empty:
            print("DataFrame vacío — nada que subir.")
            return
        table_id = f"{self.project}.{self.dataset}.{table_name}"
        job_config = bigquery.LoadJobConfig()
        job_config.write_disposition = write_disposition
        job = self.client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()
        print(f"Subidas {len(df)} filas a {table_id} (disposition={write_disposition}).")

# Parámetros - Cambiar PROJECT_ID por tu proyecto en GCP
PROJECT_ID = os.environ.get("GCP_PROJECT") or "core-veld-475310-u0"
DATASET_ID = "SANDBOX_apidata"
TABLE_NAME = "elspot_prices"

# Fechas del año 2024 para asegurar datos.
start_date = "2024-01-01"
end_date   = "2024-01-02"

# Descargar datos
client = EnerginetAPIClient()
records = client.fetch_prices(start=str(start_date), end=str(end_date), limit=100)
print(f"Registros descargados: {len(records)}")

df = client.records_to_df(records)
print(df.head())

# Subir a BigQuery
uploader = BigQueryUploader(project_id=PROJECT_ID, dataset_id=DATASET_ID)
uploader.ensure_dataset()
uploader.upload_dataframe(df, TABLE_NAME)

