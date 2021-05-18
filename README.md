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
