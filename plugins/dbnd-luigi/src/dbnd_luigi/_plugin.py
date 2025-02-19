# © Copyright Databand.ai, an IBM Company 2022

import dbnd


@dbnd.hookimpl
def dbnd_setup_plugin():
    from dbnd_luigi.luigi_tracking import register_luigi_tracking

    register_luigi_tracking()
