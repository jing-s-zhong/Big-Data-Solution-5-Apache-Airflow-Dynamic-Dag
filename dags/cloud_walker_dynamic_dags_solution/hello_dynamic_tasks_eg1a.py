# Filename: hello_dynamic_tasks_eg1.py
# https://www.cloudwalker.io/2020/12/21/airflow-dynamic-tasks/
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

# Step 1 - Define the default arguments for DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 12, 18),
    'email': ['vipin.chadha@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Step 2 - Declare a DAG with default arguments
dag = DAG('hello_dynamic_tasks_eg1',
          schedule_interval='0 8 * * *',
          default_args=default_args,
          catchup=False
          )

# Step 3 - Declare dummy start and stop tasks
start_task = DummyOperator(task_id='start', dag=dag)
end_task = DummyOperator(task_id='end', dag=dag)

# Steo 4 - Create dynamic tasks for a range of numbers
for i in range(1, 4):
    # Step 4a - Declare the task
    t1 = BashOperator(
        task_id='task_t' + str(i),
        bash_command='echo hello from task:'+str(i),
        dag=dag
    )
    # Step 4b - Define the sequence of execution of tasks
    start_task >> t1  >> end_task