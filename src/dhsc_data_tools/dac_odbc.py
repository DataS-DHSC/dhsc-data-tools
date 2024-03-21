"""Module dac_odbc allows to interact with DAC SQL endpoints."""

import os
import atexit
import pyodbc
from pypac import pac_context_for_url
from msal import PublicClientApplication
from msal import SerializableTokenCache
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
    
    #Define home path
    user_home = os.path.expanduser('~')

    # Using Azure CLI app ID
    client_id = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"
    
    # Find DAC_TENANT (tenant name) environment var
    tenant_name = os.getenv("DAC_TENANT")
    if tenant_name:
        pass
    else:
        raise KeyError("DAC_TENANT environment variable not found.")

    # Do not modify this variable. It represents the programmatic ID for
    # Azure Databricks along with the default scope of '/.default'.
    scope = ["2ff814a6-3304-4ab8-85cb-cd0e6f879c1d/.default"]

    # Define cache
    cache = SerializableTokenCache()
    cache_path = f"{user_home}\\my_cache.bin"

    if os.path.exists(cache_path):
        cache.deserialize(open(cache_path, "r").read())
    
    # atexit.register(lambda:
    #     open(cache_path, "w").write(cache.serialize())
    #     # Hint: The following optional line persists only when state changed
    #     if cache.has_state_changed else None
    #     )

    # Create client
    app = PublicClientApplication(
        client_id=client_id,
        authority="https://login.microsoftonline.com/" + tenant_name,
        token_cache = cache
    )
    
    # Get accounts for .acquire_token_silent method
    accounts = app.get_accounts()

    if accounts:
        if len(accounts) == 1:
            token = app.acquire_token_silent(scopes=scope, account=accounts[0])
        else:
            for i in accounts:
                app.remove_account(i)
            # acquire token
            with pac_context_for_url("https://www.google.co.uk/"):
                token = app.acquire_token_interactive(scopes=scope)
    else:
        # acquire token
        with pac_context_for_url("https://www.google.co.uk/"):
            token = app.acquire_token_interactive(scopes=scope)

    if cache.has_state_changed:
        open(cache_path, "w").write(cache.serialize())

    # establish keyvault connection
    kvc = kvConnection(environment)

    # retrieve relevant key vault secrets
    with pac_context_for_url(kvc.kv_uri):
        host_name = kvc.get_secret("dac-db-host")
        ep_path = kvc.get_secret("dac-sql-endpoint-http-path")

    # establish connection
    conn = pyodbc.connect(
        "Driver=Simba Spark ODBC Driver;"
        + f"Host={host_name};"  # from keyvaults
        + "Port=443;"
        + f"HTTPPath={ep_path};"  # from keyvaults
        + "SSL=1;"  
        + "ThriftTransport=2;"
        + "AuthMech=11;"
        + "Auth_Flow=0;"
        + f"Auth_AccessToken={token['access_token']}",  # from MSAL
        autocommit=True,
    )

    return conn
