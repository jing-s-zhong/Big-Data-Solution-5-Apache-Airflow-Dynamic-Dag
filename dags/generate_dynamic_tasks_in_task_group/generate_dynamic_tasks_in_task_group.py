import airflow
from airflow.models.dag import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.task_group import TaskGroup
from airflow.models import Variable
# from airflow import configuration as conf
# from airflow.models import DagBag, TaskInstance
# from airflow import DAG, settings
# from airflow.operators.bash_operator import BashOperator
import logging
import os

def values_function():
        return [1,3,5,7] #values

def group(number, **kwargs):
        #load the values if needed in the command you plan to execute
        dyn_value = "{{ task_instance.xcom_pull(task_ids='push_func') }}"
        return BashOperator(
                task_id='JOB_NAME_{}'.format(number),
                bash_command='echo {} {}'.format(dyn_value, number)
        )

dag = DAG(
        dag_id="dynamic_dag_tasks", 
        tags=['dynamic', 'example'],
        start_date=airflow.utils.dates.days_ago(2)
)

with TaskGroup("dynamic_group1", tooltip="Transform and stage data", dag=dag) as dynamic_group1:
        for i in values_function():
                group(i)

push_func = PythonOperator(
        task_id='push_func',
        provide_context=True,
        python_callable=values_function,
        dag=dag)

complete = DummyOperator(
        task_id='All_jobs_completed',
        dag=dag)

push_func >> dynamic_group1 >> complete