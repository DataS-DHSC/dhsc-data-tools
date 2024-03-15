Module dhsc_data_tools.remote_compute
=====================================

Functions
---------

    
`connect_cluster(profile: str = 'DEFAULT', file: str = '.config', cluster_uid: str = '')`
:   Establishes a connection with a databricks compute cluster.
    
    Requires:
    It relies on a `.config` file in the working directory, containing HOST, TOKEN, CLUSTER_ID:
    [<profile-name>]
    HOST=xxx
    TOKEN=xxx
    CLUSTER_ID=xxx
    
    You can also pass a cluster_id parameter manually, which will override the config file parameter.
    
    Parameters: 
    profile (config profile name defaults to "DEFAULT"),  
    file ()
    
    Returns: a spark instance.