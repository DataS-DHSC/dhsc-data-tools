"""Module dac_odbc allows to interact with DAC SQL endpoints."""

import os
import hashlib
import json
import pyodbc
from pathlib import Path
import platformdirs
from azure.identity import AuthenticationRecord, InteractiveBrowserCredential, TokenCachePersistenceOptions
from azure.keyvault.secrets import SecretClient
from pypac import pac_context_for_url
from dhsc_data_tools.keyvault import kvConnection
from dhsc_data_tools import auth_utils


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

    print("User warning: Expect an authentication pop-up window.")
    print("You will only be asked to authenticate on the first run.")

    # Find DAC_TENANT (tenant name) environment var
    # to define tenant_id
    tenant_id = os.getenv("DAC_TENANT")
    if tenant_id is None:
        raise KeyError("DAC_TENANT environment variable not found.")

    # Do not change the value of the scope parameter.
    # It represents the programmatic ID for Azure Databricks
    # (2ff814a6-3304-4ab8-85cb-cd0e6f879c1d) along with the
    # default scope (/.default, URL-encoded as %2f.default).
    scope = "2ff814a6-3304-4ab8-85cb-cd0e6f879c1d/.default"

    # Using Azure CLI app ID
    client_id = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"

    # Authentication process, attempts cached authentication first
    authentication_record_path = auth_utils.get_authentication_record_path(
        authority="login.microsoftonline.com",
        clientId=client_id,
        tenantId=tenant_id
    )

    authentication_record = auth_utils.read_authentication_record(
        authentication_record_path
        )
    
    # Set HTTP/HTTPS proxy explicitly as PAC context
    with pac_context_for_url("https://www.google.co.uk/"):
        http_proxy = os.environ["HTTP_PROXY"]
        https_proxy = os.environ["HTTPS_PROXY"]

    os.environ["HTTP_PROXY"] = http_proxy
    os.environ["HTTPS_PROXY"] = https_proxy

    # Define Azure Identity Credential
    credential = InteractiveBrowserCredential(
        client_id=client_id,
        cache_persistence_options=TokenCachePersistenceOptions(),
        additionally_allowed_tenants = ["*"],
        tenant_id = tenant_id,
        authentication_record=authentication_record
    )

    # if there is no cached auth record, reauthenticate
    if authentication_record is None:
        auth_utils.write_authentication_record(
            authentication_record_path, 
            credential.authenticate(scopes=[scope])
        )

    # Get token
    token = credential.get_token(scope)

    # establish keyvault connection
    kvc = kvConnection(environment)

    # retrieve relevant key vault secrets
    with pac_context_for_url(kvc.kv_uri):
        host_name = kvc.get_secret("dac-db-host")
        ep_path = kvc.get_secret("dac-sql-endpoint-http-path")

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
        + f"Auth_AccessToken={token.token}", # from azure identity credential
        autocommit=True,
    )

    return conn
