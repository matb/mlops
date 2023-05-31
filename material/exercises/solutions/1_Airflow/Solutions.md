# Solutions 

1. The error is a simple syntax error in the first bashoperator. 
To solve this all we need to do is add the `,`back 
Inital Code: 
```python 
with DAG(
    "simple_dag",
    default_args=default_args,
    schedule_interval="0 12 * * *",
    )  as dag:
    t1 = BashOperator(
        task_id = "print_runtime"
        bash_command='echo "Starting Run {{dag}} {{ds}}" > /tmp/{{run_id}}.log',
        dag=dag)
```
Solution:
```python 
with DAG(
    "simple_dag",
    default_args=default_args,
    schedule_interval="0 12 * * *",
    )  as dag:
    t1 = BashOperator(
        task_id = "print_runtime", # Comma was missing here 
        bash_command='echo "Starting Run {{dag}} {{ds}}" > /tmp/{{run_id}}.log',
        dag=dag)
```

2. While both code-bases will trigger-able - only one will actually be executed. This is due the 
`default_args - "start_date": datetime(2023, 4, 2),`. Since the `start_date` is the future airflow will not execute anything now.
Changing it to any date in the past will work fine.


Note: In case that you do not want your DAG to catch up with the "missed" executions you can give it one more argument `catchup=False,`
  