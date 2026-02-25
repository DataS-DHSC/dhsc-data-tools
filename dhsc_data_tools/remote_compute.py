"""Module allows to run code on Azure Databricks clusters."""

from pathlib import Path

import yaml
from databricks.connect import DatabricksSession
from pyspark.sql.session import SparkSession


def connect_cluster(
    profile: str = "DEFAULT",
    config_path: Path = Path("config.yaml"),
    cluster_uid: str | None = None,
) -> SparkSession:
    """Establish a connection with a databricks compute cluster.

    Requires:
        It relies on a yaml configuration file in the working directory,
        which by default reads `config.yaml`, containing profile entries
        such as:

        your-profile-name:
            host=xxx
            token=xxx
            cluster_id=xxx

        You can also pass a cluster_id parameter manually, which will
        override the config file parameter.

    Args:
        profile (str): config profile name defaults to "DEFAULT".
        config_path (Path): the config file's path.
        cluster_uid (str): Optional. Cluster to run code on.
            Connects to default shared if not specified.

    Returns:
        DatabricksSession

    """
    # Get configuration
    with config_path.open(encoding="utf-8") as infile:
        cfg = yaml.safe_load(infile)

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

    return spark
