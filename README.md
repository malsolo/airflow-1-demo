# Airflow version 1 DEMO

## Steps

Create a virtualenv, we'll use python 3.6

```
$ virtualenv -p python3.6 venv

$ source venv/bin/activate
```

Deactivate at any moment by typing:
```
$ deactivate
```

## Install airflow

Follow instructions at https://airflow.readthedocs.io/en/1.10.14/installation.html

```
$ export AIRFLOW_VERSION=1.10.14
$ export PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
# For example: 3.6
$ export CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example: https://raw.githubusercontent.com/apache/airflow/constraints-1.10.14/constraints-3.6.txt
$ pip install "apache-airflow[postgres]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

## Create a DAG

invoices_dag.py

## Verify

```
$ docker ps
CONTAINER ID   IMAGE              COMMAND                  CREATED              STATUS                        PORTS                                                           NAMES
3c7ed3a0d601   malsolo/airflow    "/entrypoint.sh ./st…"   About a minute ago   Up About a minute (healthy)   5555/tcp, 8793/tcp, 0.0.0.0:8080->8080/tcp, :::8080->8080/tcp   airflow-airflow
e635b329df5a   malsolo/postgres   "docker-entrypoint.s…"   2 minutes ago        Up About a minute (healthy)   0.0.0.0:32769->5432/tcp, :::32769->5432/tcp                     airflow-postgres

$ docker exec -it airflow-postgres /bin/bash
root@e635b329df5a:/# psql malsolo airflow
psql (12.6 (Debian 12.6-1.pgdg100+1))
Type "help" for help.

malsolo=# \l
                               List of databases
   Name    |  Owner  | Encoding |  Collate   |   Ctype    |  Access privileges  
-----------+---------+----------+------------+------------+---------------------
 airflow   | airflow | UTF8     | en_US.utf8 | en_US.utf8 | 
 malsolo   | airflow | UTF8     | en_US.utf8 | en_US.utf8 | =Tc/airflow        +
           |         |          |            |            | airflow=CTc/airflow
 postgres  | airflow | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0 | airflow | UTF8     | en_US.utf8 | en_US.utf8 | =c/airflow         +
           |         |          |            |            | airflow=CTc/airflow
 template1 | airflow | UTF8     | en_US.utf8 | en_US.utf8 | =c/airflow         +
           |         |          |            |            | airflow=CTc/airflow
(5 rows)

malsolo=# \c malsolo
You are now connected to database "malsolo" as user "airflow".
malsolo= select count(*) from invoices; 
 count 
-------
 32118
(1 row)

malsolo=# select * from invoices limit 3; 
 stockcode | quantity | invoicedate | unitprice | customerid |    country     
-----------+----------+-------------+-----------+------------+----------------
 85123A    |        6 | 2010-12-01  |      2.55 |      17850 | United Kingdom
 71053     |        6 | 2010-12-01  |      3.39 |      17850 | United Kingdom
 84406B    |        8 | 2010-12-01  |      2.75 |      17850 | United Kingdom
(3 rows)

malsolo=# exit
root@e635b329df5a:/# exit
exit
(venv) $




```
