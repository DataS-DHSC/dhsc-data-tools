"""Module allows to run code on Azure Databricks clusters."""

import configparser
from databricks.connect import DatabricksSession


def connect_cluster(
    profile: str = "DEFAULT", file: str = r".config", cluster_uid: str = ""
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
    config = configparser.ConfigParser()
    config.read(file, encoding="utf8")

    keys = {
        "host_url": config.get(profile, "HOST"),
        "token": config.get(profile, "TOKEN"),
        "cluster_id": config.get(profile, "CLUSTER_ID"),
    }

    # Connect to cluster; if cluster_uid argument was given,
    # override config file.
    if cluster_uid == "":
        spark = DatabricksSession.builder.remote(
            host=keys["host_url"], token=keys["token"], cluster_id=keys["cluster_id"]
        ).getOrCreate()
    else:
        spark = DatabricksSession.builder.remote(
            host=keys["host_url"], token=keys["token"], cluster_id=cluster_uid
        ).getOrCreate()

    # Return a spark instance
    return spark
