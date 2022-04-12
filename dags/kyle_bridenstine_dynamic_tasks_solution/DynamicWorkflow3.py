import airflow
from airflow.operators.python_operator import PythonOperator
from airflow.utils.task_group import TaskGroup
from airflow.models import Variable
# from airflow import configuration as conf
# from airflow.models import DagBag, TaskInstance
from airflow import DAG, settings
# from airflow.operators.bash_operator import BashOperator
import logging
import os

main_dag_id = 'DynamicWorkflow3'

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
    'provide_context': True
}

dag = DAG(
    main_dag_id,
    schedule_interval="@once",
    tags=['dynamic', 'example'],
    default_args=args)

def start(*args, **kwargs):
    value = Variable.get("DynamicWorkflow_Group1")
    logging.info("Current DynamicWorkflow_Group1 value is " + str(value))

def bridge1(*args, **kwargs):
    # You can set this value dynamically e.g., from a database or a calculation
    dynamicValue = 4
    Variable.set("DynamicWorkflow_Group2", dynamicValue)
    variableValue = Variable.get("DynamicWorkflow_Group2")
    logging.info("Current DynamicWorkflow_Group2 value is " + str(variableValue))

def bridge2(*args, **kwargs):
    # You can set this value dynamically e.g., from a database or a calculation
    dynamicValue = 3
    Variable.set("DynamicWorkflow_Group3", dynamicValue)
    variableValue = Variable.get("DynamicWorkflow_Group3")
    logging.info("Current DynamicWorkflow_Group3 value is " + str(variableValue))

def end(*args, **kwargs):
    logging.info("Ending")

def doSomeWork(name, index, *args, **kwargs):
    # Do whatever work you need to do
    # Here I will just create a new file
    os.system('touch /home/ec2-user/airflow/' + str(name) + str(index) + '.txt')

starting_task = PythonOperator(
    task_id='start',
    dag=dag,
    provide_context=True,
    python_callable=start,
    op_args=[])

# Used to connect the stream in the event that the range is zero
bridge1_task = PythonOperator(
    task_id='bridge1',
    dag=dag,
    provide_context=True,
    python_callable=bridge1,
    op_args=[])

#with TaskGroup("dynamic_group1", tooltip="Transform and stage data") as dynamic_group1:
DynamicWorkflow_Group1 = Variable.get("DynamicWorkflow_Group1")
logging.info("The current DynamicWorkflow_Group1 value is " + str(DynamicWorkflow_Group1))

for index in range(int(DynamicWorkflow_Group1)):
    dynamicTask = PythonOperator(
        task_id='firstGroup_' + str(index),
        dag=dag,
        provide_context=True,
        python_callable=doSomeWork,
        op_args=['firstGroup', index])
    starting_task >> dynamicTask
    dynamicTask >> bridge1_task

# Used to connect the stream in the event that the range is zero
bridge2_task = PythonOperator(
    task_id='bridge2',
    dag=dag,
    provide_context=True,
    python_callable=bridge2,
    op_args=[])

#with TaskGroup("dynamic_group2", tooltip="Transform and stage data") as dynamic_group2:
DynamicWorkflow_Group2 = Variable.get("DynamicWorkflow_Group2")
logging.info("The current DynamicWorkflow value is " + str(DynamicWorkflow_Group2))

for index in range(int(DynamicWorkflow_Group2)):
    dynamicTask = PythonOperator(
        task_id='secondGroup_' + str(index),
        dag=dag,
        provide_context=True,
        python_callable=doSomeWork,
        op_args=['secondGroup', index])
    bridge1_task >> dynamicTask
    dynamicTask >> bridge2_task

ending_task = PythonOperator(
    task_id='end',
    dag=dag,
    provide_context=True,
    python_callable=end,
    op_args=[])

#with TaskGroup("dynamic_group3", tooltip="Transform and stage data") as dynamic_group3:
DynamicWorkflow_Group3 = Variable.get("DynamicWorkflow_Group3")
logging.info("The current DynamicWorkflow value is " + str(DynamicWorkflow_Group3))

for index in range(int(DynamicWorkflow_Group3)):
    dynamicTask = PythonOperator(
        task_id='thirdGroup_' + str(index),
        dag=dag,
        provide_context=True,
        python_callable=doSomeWork,
        op_args=['thirdGroup', index])
    bridge2_task >> dynamicTask
    dynamicTask >> ending_task

# If you do not connect these then in the event that your range is ever zero you will have a disconnection between your stream
# and your tasks will run simultaneously instead of in your desired stream order.
starting_task >> bridge1_task
bridge1_task >> bridge2_task
bridge2_task >> ending_task
