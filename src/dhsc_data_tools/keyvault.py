"""Module to interact with Azure Keyvaults"""

import os
from azure.keyvault.secrets import SecretClient
from azure.identity import TokenCachePersistenceOptions
from dhsc_data_tools import auth_utils


class kvConnection:
    """
    Key vault connection object.

    Parameters:
    Takes an environment name parameter, which must be one of
    "dev", "test", "qa" or "prod". Defaults to "prod". (Not case sensitive.)
    It will look for a corresponding key vault name in environment variables.

    Requires: KEY_VAULT_NAME and DAC_TENANT environment variables.

    Returns: Azure Keyvault Connection object.
    """

    def __init__(self, environment: str = "prod"):
        # Check issues with the env name parameter input by user
        if environment.upper() in ["DEV", "TEST", "QA", "PROD"]:
            temp_vault_name = os.getenv("KEY_VAULT_NAME")
            if temp_vault_name:
                # KEY_VAULT_NAME must include {env} for .format method
                self.vault_name = temp_vault_name.format(env=environment.lower())
            else:
                raise KeyError("KEY_VAULT_NAME environment variable not found.")
            if self.vault_name:
                self.kv_uri = f"https://{self.vault_name}.vault.azure.net"
            else:
                raise KeyError("KEY_VAULT_NAME environment variable not found.")
        else:
            raise KeyError(
                "Environment name argument must be one of 'dev', 'test', 'qa', 'prod'."
            )

        # Do not change the value of the scope parameter.
        # It represents the programmatic ID for Azure Databricks
        # (2ff814a6-3304-4ab8-85cb-cd0e6f879c1d) along with the
        # default scope (/.default, URL-encoded as %2f.default).
        scope = "2ff814a6-3304-4ab8-85cb-cd0e6f879c1d/.default"

        # Fixed
        client_id = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"

        # Find DAC_TENANT (tenant name) environment var
        # to define tenant_id
        tenant_id = os.getenv("DAC_TENANT")
        if tenant_id is None:
            raise KeyError("DAC_TENANT environment variable not found.")

        # Define cache options for credential object
        cache_options = TokenCachePersistenceOptions()

        # Authentication process, attempts cached authentication first
        authentication_record_path = auth_utils.get_authentication_record_path(
            authority="login.microsoftonline.com",
            clientId=client_id,
            tenantId=tenant_id,
        )

        authentication_record = auth_utils.read_authentication_record(
            authentication_record_path
        )

        # Define Azure Identity Credential
        self.credential = auth_utils.return_credential(
            client_id, tenant_id, cache_options, authentication_record
        )

        # if there is no cached auth record, reauthenticate
        auth_utils.check_auth_record(
            self.credential, authentication_record, authentication_record_path, scope
        )

        # InteractiveBrowserCredential and AuthenticationRecord
        # lazy load, here they are forced to run, although the
        # token will not be used by the code further.
        token = self.credential.get_token(scope)

        # Establish Azure Keyvault SecretClient
        self.client = SecretClient(vault_url=self.kv_uri, credential=self.credential)

    def get_secret(self, secret_name: str):
        """Returns the *value* of the secret.

        Parameters:
        `get_secret()` method requires the name of the sought secret to be passed as an argument.

        Please note:
        User might have to set HTTP/HTTPS proxy as PAC context explicitly
        before running kvconnection.get_secret().
        """

        print("Getting secret...")

        return self.client.get_secret(secret_name).value
