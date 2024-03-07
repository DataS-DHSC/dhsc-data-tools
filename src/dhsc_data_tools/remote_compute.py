import os
import configparser
from databricks.connect import DatabricksSession

def parse_cfg(profile, file=r'.config'):
    '''
    Returns a dictionary of configuration values.

    Takes a config profile name and a file argument. 
    The latter defaults to .config in the same  working dir.
    
    Requires the config file in the following way:
    [<profile-name>]
    HOST=xxx
    TOKEN=xxx
    CLUSTER_ID=xxx
    '''
    config = configparser.ConfigParser()
    config.read_file(open(file))

    return {"host_url":config.get(profile, 'HOST'), 
            "token":config.get(profile, 'TOKEN'), 
            "cluster_id":config.get(profile, 'CLUSTER_ID')}

def connect_cluster(profile, file=r'.config', cluster_uid=""):
    '''
    Function: remote_connect(profile, file=r'.config', cluster_uid="")
    
    This function establishes a connection with a databricks compute cluster.
    
    It relies on environment a config file containing HOST, TOKEN, CLUSTER_ID.

    You can also pass a cluster_id manually.

    Returns a spark instance.
    '''
    
    keys = parse_cfg(profile, file)
    
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

    return spark