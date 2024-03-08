Module dhsc_data_tools.remote_compute
=====================================

Functions
---------

    
`connect_cluster(profile, file='.config', cluster_uid='')`
:   Function: remote_connect(profile, file=r'.config', cluster_uid="")
    
    This function establishes a connection with a databricks compute cluster.
    
    It relies on environment a config file containing HOST, TOKEN, CLUSTER_ID.
    
    You can also pass a cluster_id manually.
    
    Returns a spark instance.

    
`parse_cfg(profile, file='.config')`
:   Returns a dictionary of configuration values.
    
    Takes a config profile name and a file argument. 
    The latter defaults to .config in the same  working dir.
    
    Requires the config file in the following way:
    [<profile-name>]
    HOST=xxx
    TOKEN=xxx
    CLUSTER_ID=xxx