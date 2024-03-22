"""Module allows to run code on Azure Databricks clusters."""

import yaml
from databricks.connect import DatabricksSession


def connect_cluster(
    profile: str = "DEFAULT", file: str = r"config_yaml", cluster_uid: str = None
):
    """Establishes a connection with a databricks compute cluster.

    Requires:
    It relies on a `.config` file in the working directory, containing:
    [<profile-name>]
    HOST=xxx
    TOKEN=xxx
    CLUSTER_ID=xxx

    NB: You can also pass a cluster_id parameter manually,
        which will override the config file parameter.

    Parameters:
    profile (config profile name defaults to "DEFAULT"),
    file ()

    Returns: a spark instance.
    """

    # Get configuration
    with open(file, "r") as file:
        cfg = yaml.safe_load(file)

    # Connect to cluster; if cluster_uid argument was given,
    # override config file.
    if cluster_uid:
        spark = DatabricksSession.builder.remote(
            host=cfg[profile]["host"],
            token=cfg[profile]["token"],
            cluster_id=cluster_uid,
        ).getOrCreate()
    else:
        spark = DatabricksSession.builder.remote(
            host=cfg[profile]["host"],
            token=cfg[profile]["token"],
            cluster_id=cfg[profile]["cluster_id"],
        ).getOrCreate()

    # Return a spark instance
    return spark
