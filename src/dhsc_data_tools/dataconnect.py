import os
from msal import PublicClientApplication
import pyodbc
from pypac import pac_context_for_url
from dhsc_data_tools.keyvault import kvConnection

def db_connect(environment="prod"):

    '''
    This function allows to connect to data within the DAC,
    and query it using SQL queries.

    Simba Spark ODBC Driver is required.

    Expects environment variables for tenant name, 
    '''

    print("User warning: Expect two authentication pop-up windows,\nwhich may ask you to authenticate and then \n confirm 'Authentication complete.'")
    
    # Using Azure CLI app ID
    client_id = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"
    tenant_name = os.environ["TENANT_NAME"]

    # Do not modify this variable. It represents the programmatic ID for
    # Azure Databricks along with the default scope of '/.default'.
    scope = [ '2ff814a6-3304-4ab8-85cb-cd0e6f879c1d/.default' ]

    # create client
    app = PublicClientApplication(
        client_id = client_id,
        authority = "https://login.microsoftonline.com/" + tenant_name
        )

    # acquire token
    with pac_context_for_url("https://www.google.co.uk/"):
        token = app.acquire_token_interactive(
            scopes = scope
        )

    # establish keyvault connection
    KVC = kvConnection(environment)

    # retrieve relevant key vault secrets
    with pac_context_for_url(KVC.KVUri):
        host_name = KVC.get_secret("dac-sql-endpoint-hostname")
        ep_path = KVC.get_secret("dac-sql-endpoint-http-path")

    # establish connection
    conn = pyodbc.connect(
        "Driver=Simba Spark ODBC Driver;" +
        f"Host={host_name};" + # from keyvaults
        "Port=443;" +
        f"HTTPPath={ep_path};" + # from keyvaults 
        "SSL=1;" +
        "ThriftTransport=2;" +
        "AuthMech=11;" +
        "Auth_Flow=0;" +
        f"Auth_AccessToken={token['access_token']}",
        autocommit = True
    )

    return conn