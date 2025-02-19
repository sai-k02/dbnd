# © Copyright Databand.ai, an IBM Company 2022

import datetime

import pytest

from airflow import DAG
from airflow.models import TaskInstance
from airflow.operators.python_operator import PythonOperator

from dbnd import config
from dbnd._vendor.pendulum import tz, utcnow
from dbnd_airflow import track_task


DATA_INTERVAL_START = datetime.datetime(2021, 9, 13).replace(tzinfo=tz.UTC)

TEST_DAG_ID = "my_custom_operator_dag"
TEST_TASK_ID = "my_custom_operator_task"


def python_operator_function():
    actual = config.get("tracking_spark", "agent_path")
    assert actual == "__FAKE__"


@pytest.fixture()
def dag():
    with DAG(
        dag_id=TEST_DAG_ID,
        schedule_interval="@daily",
        default_args={"start_date": DATA_INTERVAL_START},
    ) as dag:
        PythonOperator(python_callable=python_operator_function, task_id=TEST_TASK_ID)
    return dag


def test_dbnd_config_on_operator_is_effective(dag):
    operator = dag.get_task(TEST_TASK_ID)

    # Arrange
    operator.dbnd_config = {"tracking_spark": {"agent_path": "__FAKE__"}}

    # This line will replace operator.execute method with our custom new_execute
    track_task(operator)

    ti = TaskInstance(operator, utcnow())
    ti.run(ignore_depends_on_past=True, ignore_ti_state=True)
