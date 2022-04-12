import time
from datetime import datetime
from airflow.models.dag import DAG
from airflow.decorators import task
from airflow.utils.task_group import TaskGroup
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.hooks.base_hook import BaseHook
from airflow.models import Variable
from airflow.models import XCom
import pandas as pd
from sqlalchemy import create_engine

SNOWFLAKE_CONN_ID = 'snow_jingsheng'
SNOWFLAKE_SCHEMA = '_metadata'
SNOWFLAKE_WAREHOUSE = 'compute_wh'
SNOWFLAKE_DATABASE = 'int'
SNOWFLAKE_ROLE = 'sysadmin'
SNOWFLAKE_SAMPLE_TABLE = 'CTRL_TASK_SCHEDULE'

#extract tasks
@task()
def get_schema_syncers():
    hook = SnowflakeHook(snowflake_conn_id="snow_jingsheng")
    sql = """ SELECT * FROM INT._METADATA.CTRL_SCHEMA_UPDATE """
    df = hook.get_pandas_df(sql)
    print(df)
    task_dict = df.to_dict('records')
    return task_dict
#
@task()
def pop_schema_syncers(task_dict: dict):
    all_loaders = []
    start_time = time.time()
    #access the table_name element in dictionaries
    for k, v in task_dict.items():
        #print(v)
        all_loaders.append(v['metadata_update'])
        sql = f'{v}'
        hook = SnowflakeHook(snowflake_conn_id="snow_jingsheng")
        df = hook.get_pandas_df(sql)
        print(f'Done. {str(round(time.time() - start_time, 2))} total seconds elapsed')
    print("Db Schema Synced")
    return all_loaders
    
#extract tasks
@task()
def get_data_loaders():
    hook = SnowflakeHook(snowflake_conn_id="snow_jingsheng")
    sql = """ SELECT * FROM INT._METADATA.CTRL_TASK_SCHEDULE """
    df = hook.get_pandas_df(sql)
    print(df)
    task_dict = df.to_dict('dict')
    return task_dict
#
@task()
def pop_data_loaders(task_dict: dict):
    all_loaders = []
    start_time = time.time()
    #access the table_name element in dictionaries
    for k, v in task_dict['data_loader'].items():
        #print(v)
        all_loaders.append(v)
        sql = f'{v}'
        hook = SnowflakeHook(snowflake_conn_id="snow_jingsheng")
        df = hook.get_pandas_df(sql)
        print(f'Done. {str(round(time.time() - start_time, 2))} total seconds elapsed')
    print("Data loader executed")
    return all_loaders

def my_func():
    print('Hello from my_func')

# [START how_to_task_group]
with DAG(
    dag_id="dynamic_tasks_dag",
    default_args={'snowflake_conn_id': SNOWFLAKE_CONN_ID},
    schedule_interval="0 9 * * *", 
    start_date=datetime(2022, 3, 5),
    catchup=False,  
    tags=["dynamic", "example"]
    ) as dag:

    with TaskGroup("schema_sync_group", tooltip="Extract and load source data") as schema_sync_group:
        schema_syncers = get_schema_syncers()
        # python_task = PythonOperator(task_id='python_task', python_callable=my_func, dag=dag)
        # syncer_runners = pop_schema_syncers(schema_syncers)
        syncer_runners = []
        for k, v in schema_syncers.xcom_pull('schema_syncers'):
            #print(v)
            snowflake_op = SnowflakeOperator(
                #task_id=f'{v["data_schema"]}:{v["data_schema"]}',
                #sql=f'{v["data_loader"]}',
                task_id=f'task_{k}',
                sql=f'{v["data_loader"]}',
                warehouse=SNOWFLAKE_WAREHOUSE,
                database=SNOWFLAKE_DATABASE,
                schema=SNOWFLAKE_SCHEMA,
                role=SNOWFLAKE_ROLE,
                dag=dag,
            )
            syncer_runners.append(snowflake_op)
        #define order
        schema_syncers >> syncer_runners

    # [START howto_task_group_section_2]
    with TaskGroup("data_load_group", tooltip="Transform and stage data") as data_load_group:
        data_loaders = get_data_loaders()
        loader_runners = pop_data_loaders(data_loaders)
        #define order
        data_loaders >> loader_runners

    with TaskGroup("metadata_sync_group", tooltip="Final Product model") as metadata_sync_group:
        metadata_syncer = DummyOperator(task_id='metadata_syncer', dag=dag)
        #define order
        metadata_syncer

    schema_sync_group >> metadata_sync_group >> data_load_group
