import os

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.python import PythonVirtualenvOperator

OUTPUT_ONE_PATH = "/tmp/output_one.txt"
OUTPUT_TWO_PATH = "/tmp/output_one.txt"


default_args = {
    "owner": "uta",
    "depends_on_past": False,
    "start_date": datetime(2023, 4, 2),
    "email": ["matthias.baumann@ultratendency.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
}

def decorate_file(input_path, output_path):
    with open(input_path, "r") as in_file:
        line = in_file.read()

    with open(output_path, "w") as out_file:
        out_file.write("My "+line)

        
with DAG(
    "simple_dag",
    default_args=default_args,
    schedule_interval="0 12 * * *",
    )  as dag:
    t1 = BashOperator(
        task_id = "print_runtime",
        bash_command='echo "Starting Run {{dag}} {{ds}}" > /tmp/{{run_id}}.log',
        dag=dag)

    t2 = BashOperator(
        task_id="print_file",
        bash_command='echo "pipeline" > {}'.format(OUTPUT_ONE_PATH),
        dag=dag)

    t3 = PythonOperator(
        task_id="decorate_file",
        python_callable=decorate_file,
        op_kwargs={"input_path": OUTPUT_ONE_PATH, "output_path": OUTPUT_TWO_PATH},
        dag=dag)


t1 >> t2 >> t3
