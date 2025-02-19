# © Copyright Databand.ai, an IBM Company 2022

from __future__ import absolute_import

import pandas as pd

import dbnd

from dbnd import Config, data, output, parameter, pipeline, task
from dbnd._core.current import current_task_run
from dbnd.tasks import PipelineTask, PythonTask


class TTask(PythonTask):
    t_param = parameter.value("1")
    t_output = output.data

    def run(self):
        self.t_output.write("%s" % self.t_param)


class TTaskWithInput(TTask):
    t_input = data


class TTaskThatFails(TTask):
    msg = parameter.value("This is a drill")

    def run(self):
        raise ValueError(self.msg)


class CaseSensitiveParameterTask(PythonTask):
    TParam = parameter.value(1)

    def run(self):
        return self.TParam**2


class RequiredConfig(dbnd.Config):
    required_test_param = parameter[str]


class TaskThatRequiresConfig(PipelineTask):
    some_output = output

    def band(self):
        if RequiredConfig.try_instance().required_test_param == "A":
            self.some_output = SubTaskThatFails(simple_parameter="A")
        else:
            self.some_output = TTask()


class SubTaskThatFails(TTask):
    def complete(self):
        return False

    def run(self):
        raise Exception()


class TTaskWithMetrics(TTask):
    def run(self):
        self.log_metric("metric_int", 1)
        self.log_metric("metric_bigint", 1234567890123456)
        self.log_metric("metric_float", 3.14)
        self.log_metric("metric_str", "str")

        current_task_run().set_external_resource_urls({"someurl": "http://localhost"})

        super(TTaskWithMetrics, self).run()


class TPipelineWithMetrics(PipelineTask):
    def band(self):
        TTaskWithMetrics()


class TTaskWithMetricsAndInput(TTaskWithMetrics):
    param_str = parameter.value(default="boo")[str]

    def run(self):
        super(TTaskWithMetricsAndInput, self).run()


class FooBaseTask(TTask):
    """
    used by all command line checkers
    """


class FooConfig(Config):
    bar = parameter(default="from_constr")[str]
    quz = parameter(default="from_constr")[str]


class TConfig(Config):
    _conf__task_family = "tconfig"
    config_value_s1 = parameter[str]
    config_value_s2 = parameter[str]


@task
def ttask_simple(tparam="1"):
    # type:(str)->str
    return "result %s"


@task
def ttask_dataframe(tparam=1):
    # type:(int)->pd.DataFrame
    return pd.DataFrame(data=[[tparam, tparam]], columns=["c1", "c2"])


@pipeline
def tpipeline_simple(param="1"):
    return ttask_simple(param)


@pipeline
def tpipeline_two_tasks(param1=1, param2="2"):
    data_df = ttask_dataframe(param1)
    data_str = ttask_simple(str(data_df))
    return data_str
