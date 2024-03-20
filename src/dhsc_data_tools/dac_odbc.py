"""Module dac_odbc allows to interact with DAC SQL endpoints."""

import os
from msal import PublicClientApplication
import pyodbc
from pypac import pac_context_for_url
from dhsc_data_tools.keyvault import kvConnection


def connect(environment: str = "prod"):
    """Allows to connect to data within the DAC, and query it using SQL queries.

    Parameters: an environment argument, which defaults to "prod".
    Must be one of "dev", "qa", "test", "prod".

    Requires:
    TENANT_NAME environment variable.
    Simba Spark ODBC Driver is required.
    Request the latter through IT portal, install through company portal.

    Returns: connection object.
    """

    print("User warning: Expect two authentication pop-up windows.")
    print(
        "These may ask you to authenticate and then confirm 'Authentication complete.'"
    )

    # Using Azure CLI app ID
    client_id = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"
    try:
        tenant_name = os.environ["DAC_TENANT"]
    except KeyError as exc:
        raise KeyError("DAC_TENANT environment variable not found.") from exc

    # Do not modify this variable. It represents the programmatic ID for
    # Azure Databricks along with the default scope of '/.default'.
    scope = ["2ff814a6-3304-4ab8-85cb-cd0e6f879c1d/.default"]

    # create client
    app = PublicClientApplication(
        client_id=client_id,
        authority="https://login.microsoftonline.com/" + tenant_name,
    )

    # acquire token
    with pac_context_for_url("https://www.google.co.uk/"):
        token = app.acquire_token_interactive(scopes=scope)

    # establish keyvault connection
    kvc = kvConnection(environment)

    # retrieve relevant key vault secrets
    with pac_context_for_url(kvc.kv_uri):
        host_name = kvc.get_secret("dac-db-host")
        ep_path = kvc.get_secret("dac-sql-endpoint-http-path")

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
        + f"Auth_AccessToken={token['access_token']}",
        autocommit=True,
    )

    return conn
