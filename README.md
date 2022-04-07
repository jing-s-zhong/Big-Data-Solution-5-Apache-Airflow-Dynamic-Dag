# Big-Data-Solution-5-Apache-Airflow-Dynamic-Dag

### Starting Airflow Docker Container

```
docker-compose up -d
```

### Enter Airflow Web UI

```
https://localhost:8080

username: airflow
password: airflow
```

### Check Snowflake Package

(1) Admin->Providers

check following item in the list
```
apache-airflow-providers-snowflake
```

(2) Admin->Connections-><Add a new connection>

check existing the "Snowflake" option in connection_type drop_down list 
