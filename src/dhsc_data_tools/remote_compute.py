import os
import configparser
from databricks.connect import DatabricksSession

def connect_cluster(profile, file=r'.config', cluster_uid=""):
    '''Establishes a connection with a databricks compute cluster.
    
    It relies on a `.config` file in the working directory, containing HOST, TOKEN, CLUSTER_ID:
    [<profile-name>]
    HOST=xxx
    TOKEN=xxx
    CLUSTER_ID=xxx
    
    You can also pass a cluster_id parameter manually, which will override the config file parameter.

    Returns a spark instance.
    '''

    #Get configuration
    config = configparser.ConfigParser()
    config.read_file(open(file))
    
    keys = {"host_url":config.get(profile, 'HOST'), 
            "token":config.get(profile, 'TOKEN'), 
            "cluster_id":config.get(profile, 'CLUSTER_ID')}
    
    #Connect to cluster; if cluster_uid argument was given,
    # override config file.
    if cluster_uid=="":
        spark = DatabricksSession.builder.remote(
        host       = keys['host_url'], 
        token      = keys['token'], 
        cluster_id = keys['cluster_id'] 
        ).getOrCreate()
    else:
        spark = DatabricksSession.builder.remote(
        host       = keys['host_url'], 
        token      = keys['token'], 
        cluster_id = cluster_uid
        ).getOrCreate()

    # Return a spark instance
    return spark