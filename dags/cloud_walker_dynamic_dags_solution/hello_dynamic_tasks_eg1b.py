# Filename: hello_dynamic_tasks_eg1.py
# https://www.cloudwalker.io/2020/12/21/airflow-dynamic-tasks/
from airflow import DAG
from airflow.models import Variable
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
dag = DAG('hello_dynamic_tasks_eg2',
          schedule_interval='0 8 * * *',
          default_args=default_args,
          catchup=False
          )

# Step 3 - Declare dummy start and stop tasks
start_task = DummyOperator(task_id='start', dag=dag)
end_task = DummyOperator(task_id='end', dag=dag)

# Step 4 - Read the list of elements from the airflow variable
v_list = Variable.get("v_list", deserialize_json=True)

# Step 5 - Create dynamic tasks for each element of the list
for element in v_list:
    # Step 5a - Declare the task
    t1 = BashOperator(
        task_id='task_t' + str(element),
        bash_command='echo hello from task:' + str(element),
        dag=dag
    )
    # Step 5b - Define the sequence of execution of task
    start_task >> t1 >> end_task
