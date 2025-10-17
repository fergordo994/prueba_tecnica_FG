# parte3/airflow_dag.py

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

# Argumentos por defecto del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(1900, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

# Definición del DAG
with DAG(
    'test',
    default_args=default_args,
    description='DAG de prueba técnica FG',
    schedule_interval='0 3 * * *',  # cada día a las 3:00 UTC
    catchup=False
) as dag:

    # Tareas start y end
    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    # Tareas dummy intermedias
    N = 4
    tasks = []

    for i in range(1, N + 1):
        task = DummyOperator(task_id=f'task_{i}')
        tasks.append(task)

    # Definir dependencias: pares dependen de impares
    odd_tasks = [t for t in tasks if int(t.task_id.split('_')[1]) % 2 != 0]
    even_tasks = [t for t in tasks if int(t.task_id.split('_')[1]) % 2 == 0]

    for even in even_tasks:
        for odd in odd_tasks:
            odd >> even

    # Operador personalizado: TimeDiff
    class TimeDiffOperator(BaseOperator):

        @apply_defaults
        def __init__(self, diff_date, *args, **kwargs):
            super(TimeDiffOperator, self).__init__(*args, **kwargs)
            self.diff_date = diff_date

        def execute(self, context):
            now = datetime.utcnow()
            diff = now - self.diff_date
            print(f"La diferencia de tiempo es: {diff}")
            return diff

    time_diff_task = TimeDiffOperator(
        task_id='time_diff_task',
        diff_date=datetime(2024, 1, 1)
    )

    # Flujo del DAG
    start >> tasks >> time_diff_task >> end

# Un Hook en Airflow es una clase que permite conectarse a sistemas externos (APIs, bases de datos, etc.)
# y realizar operaciones con ellos. Ej: BigQueryHook, S3Hook.
# Una conexión (Connection) es solo la configuración (usuario, contraseña, host...) que el Hook usa para autenticarse.
