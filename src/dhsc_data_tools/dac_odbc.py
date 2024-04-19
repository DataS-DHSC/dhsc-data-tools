"""Module dac_odbc allows to interact with DAC SQL endpoints."""

import pyodbc
from pypac import pac_context_for_url
from dhsc_data_tools.keyvault import KVConnection
from dhsc_data_tools import _utils
from dhsc_data_tools import _constants


def connect(environment: str = "prod"):
    """Allows to connect to data within the DAC, and query it using SQL queries.

    Parameters: an environment argument, which defaults to "prod".
    Must be one of "dev", "qa", "test" or "prod".

    Requires:
    KEY_VAULT_NAME and DAC_TENANT environment variables.
    Simba Spark ODBC Driver is required.
    Request the latter through IT portal, install through company portal.

    Returns: connection object.
    """

    # establish keyvault connection
    kvc = KVConnection(environment)

    # Set PAC context
    with pac_context_for_url(kvc.kv_uri):
        # Define Azure Identity Credential
        credential = _utils.return_credential(
            _utils._return_tenant_id()
            )
        # Get token
        token = credential.get_token(_constants._scope)
        # retrieve relevant key vault secrets
        host_name = kvc.get_secret("dac-db-host")
        ep_path = kvc.get_secret("dac-sql-endpoint-http-path")

    # User warning
    print(
        "Creating connection.", 
        "This may take some time if cluster needs starting."
        )

    # establish connection and return object
    conn = pyodbc.connect(
        "Driver=Simba Spark ODBC Driver;"
        + f"Host={host_name};"  # from keyvaults
        + "Port=443;"
        + f"HTTPPath={ep_path};"  # from keyvaults
        + "SSL=1;"
        + "ThriftTransport=2;"
        + "AuthMech=11;"
        + "Auth_Flow=0;"
        + f"Auth_AccessToken={token.token}",  # from azure identity credential
        autocommit=True,
    )

    return conn
