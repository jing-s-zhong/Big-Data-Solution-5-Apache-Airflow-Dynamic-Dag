# Big-Data-Solution-5-Apache-Airflow-Dynamic-Dag

### Starting Airflow Docker Container

```
docker-compose up -d
```

stop the Airflow container
```
docker-copose down
```

restart the Airefoe container
```
docker-compose restart
```

### Enter The Airflow Admin Web UI

```
https://localhost:8080

username: airflow
password: airflow
```

### Customize Airflow Image by Adding Packages

(1) Add the package names to the requirements.txt file. Each package one line.
```
apache-airflow-providers-snowflake
apache-airflow-providers-microsoft-mssql
pandas
```

(2) Customize the docker image by creating a Dockerfile with attached config
```
FROM apache/airflow:2.2.5
COPY requirements.txt .
RUN pip install -r requirements.txt
```

(3) Build the customized docker image
```
docker-compose build
```
or drectly starting the containers with 'build' option
```
docker-compose up -d --build
```

### Check Snowflake Package Available

(1) Admin->Providers

check following item in the list
```
apache-airflow-providers-snowflake
```

(2) Admin->Connections-><Add a new connection>

check existing the "Snowflake" option in connection_type drop_down list 
