Module dhsc_data_tools.remote_compute
=====================================
Module allows to run code on Azure Databricks clusters.

Functions
---------

    
`connect_cluster(profile: str = 'DEFAULT', file: str = 'config_yaml', cluster_uid: str | None = None)`
:   Establishes a connection with a databricks compute cluster.
    
    Requires:
    It relies on a yaml configuration file in the working directory,
    which by default reads `config.yaml`, containing profile entries
    such as:
    
    your-profile-name:
        host=xxx
        token=xxx
        cluster_id=xxx
    
    NB: You can also pass a cluster_id parameter manually,
        which will override the config file parameter.
    
    Parameters:
    profile (config profile name defaults to "DEFAULT"),
    file (the config file's name, you can pass a file path also),
    cluster_uid (optional).
    
    Returns: a spark instance.