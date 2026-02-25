"""Module allows to interact with DAC SQL endpoints."""

import warnings

import pyodbc
from pypac import pac_context_for_url

from dhsc_data_tools import _auth_utils, _constants
from dhsc_data_tools.keyvault import KVConnection


def connect(
    environment: str = "prod",
    refresh_token: bool = False,
) -> pyodbc.Connection:
    """Return connection object to the DAC.

    Use connect the connection object returned to read data within the DAC,
    and use SQL queries.

    Requires:
        KEY_VAULT_NAME and DAC_TENANT environment variables.
        Simba Spark ODBC Driver is required.
        Request the latter through IT portal, install through company portal.

    Args:
        environment (str): DAC environment. Defaults to "prod".
            Must be one of "dev", "qa", "test" or "prod".
        refresh_token (bool): When True, will trigger re-authentication
            instead of using cached credentials. Defaults to False.

    Returns:
        pyodbc.Connection

    """
    # Set PAC context
    with pac_context_for_url(f"https://{_constants._AUTHORITY}/"):
        # Define Azure Identity Credential
        credential = _auth_utils._return_credential(refresh_token)
        # establish keyvault connection
        kvc = KVConnection(
            environment=environment,
            refresh_token=refresh_token,
            credential=credential,
        )
        # Get token
        token = credential.get_token(_constants._SCOPE)
        # retrieve relevant key vault secrets
        host_name = kvc.get_secret("dac-db-host")
        ep_path = kvc.get_secret("dac-sql-endpoint-http-path")

    # User warning
    warnings.warn(
        (
            "Creating connection. "
            "This may take some time if cluster needs starting."
        ),
        stacklevel=2,
    )

    # establish connection and return object
    return pyodbc.connect(
        (
            "Driver=Simba Spark ODBC Driver;"
            f"Host={host_name};"  # from keyvaults
            "Port=443;"
            f"HTTPPath={ep_path};"  # from keyvaults
            "SSL=1;"
            "ThriftTransport=2;"
            "AuthMech=11;"
            "Auth_Flow=0;"
            f"Auth_AccessToken={token.token}"  # from credential
        ),
        autocommit=True,
    )
