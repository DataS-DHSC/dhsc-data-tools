"""Module dac_odbc allows to interact with DAC SQL endpoints."""

import os
import pyodbc
from pypac import pac_context_for_url
from azure.identity import SharedTokenCacheCredential, TokenCachePersistenceOptions
from dhsc_data_tools.keyvault import kvConnection


def connect(environment: str = "prod"):
    """Allows to connect to data within the DAC, and query it using SQL queries.

    Parameters: an environment argument, which defaults to "prod".
    Must be one of "dev", "qa", "test", "prod".

    Requires:
    DAC_TENANT environment variable to be loaded.
    Simba Spark ODBC Driver is required.
    Request the latter through IT portal, install through company portal.

    Returns: connection object.
    """

    print("User warning: Expect an authentication pop-up window.")
    print("You will only be asked to authenticate once the first time.")

    # Using Azure CLI app ID
    client_id = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"
    tenant_name = os.getenv("DAC_TENANT")
    if tenant_name:
        pass
    else:
        raise KeyError("DAC_TENANT environment variable not found.")

    # establish keyvault connection
    kvc = kvConnection(environment)

    # retrieve relevant key vault secrets
    with pac_context_for_url(kvc.kv_uri):
        host_name = kvc.get_secret("dac-db-host")
        ep_path = kvc.get_secret("dac-sql-endpoint-http-path")

    # Do not change the value of the scope parameter. It represents the programmatic ID 
    # for Azure Databricks (2ff814a6-3304-4ab8-85cb-cd0e6f879c1d) along with the default 
    # scope (/.default, URL-encoded as %2f.default).
    scope = "2ff814a6-3304-4ab8-85cb-cd0e6f879c1d/.default"
    
    # Do not modify `allow_unencrypted_storage` parameter - which defaults to False
    cache_options = TokenCachePersistenceOptions()

    # Get auth token
    credential = SharedTokenCacheCredential(cache_persistence_options=cache_options)
    token = credential.get_token(scope)

    # establish connection
    conn = pyodbc.connect(
        "Driver=Simba Spark ODBC Driver;"
        + f"Host={host_name};"
        + "Port=443;"  # from keyvaults
        + f"HTTPPath={ep_path};"
        + "SSL=1;"  # from keyvaults
        + "ThriftTransport=2;"
        + "AuthMech=11;"
        + "Auth_Flow=0;"
        + f"Auth_AccessToken={token.token}",
        autocommit=True,
    )

    return conn
