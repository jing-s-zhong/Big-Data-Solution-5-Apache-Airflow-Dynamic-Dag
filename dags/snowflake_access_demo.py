# https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/_modules/airflow/providers/snowflake/example_dags/example_snowflake.html
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
Example use of Snowflake related operators.
"""
from datetime import datetime

from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

SNOWFLAKE_CONN_ID = 'snow_jingsheng'
SNOWFLAKE_SCHEMA = '_metadata'
SNOWFLAKE_WAREHOUSE = 'compute_wh'
SNOWFLAKE_DATABASE = 'int'
SNOWFLAKE_ROLE = 'sysadmin'
SNOWFLAKE_SAMPLE_TABLE = 'CTRL_TASK_SCHEDULE'

# SQL commands
QUERY_TABLE_SQL_STRING = (
    f"SELECT * FROM {SNOWFLAKE_SAMPLE_TABLE} ;"
)

# [START howto_operator_snowflake]

dag = DAG(
    'example_snowflake',
    start_date=datetime(2021, 1, 1),
    default_args={'snowflake_conn_id': SNOWFLAKE_CONN_ID},
    tags=['snowflake', 'example'],
    catchup=False,
)


snowflake_op_sql_str = SnowflakeOperator(
    task_id='snowflake_op_sql_str',
    dag=dag,
    sql=QUERY_TABLE_SQL_STRING,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA,
    role=SNOWFLAKE_ROLE,
)

# [END howto_operator_snowflake]

# [START howto_operator_s3_to_snowflake]

# [END howto_operator_s3_to_snowflake]

# [START howto_operator_snowflake_to_slack]

# [END howto_operator_snowflake_to_slack]

(
    snowflake_op_sql_str
)
