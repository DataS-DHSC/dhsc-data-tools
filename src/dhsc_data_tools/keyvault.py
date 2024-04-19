"""Module to interact with Azure Keyvaults"""

import os
from azure.keyvault.secrets import SecretClient
from dhsc_data_tools import _utils


class KVConnection:
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
        if environment.upper() not in ["DEV", "TEST", "QA", "PROD"]:
            raise ValueError(
                "Environment name argument must be one of 'dev', 'test', 'qa', 'prod'."
            )

        temp_vault_name = os.getenv("KEY_VAULT_NAME")

        if temp_vault_name:
            # KEY_VAULT_NAME must include {env} for .format method
            self.vault_name = temp_vault_name.format(env=environment.lower())
        else:
            raise KeyError(
                """
                KEY_VAULT_NAME environment variable not found.
                Make sure KEY_VAULT_NAME is in your .env file
                and .env file is loaded.
                """
                )
        
        self.kv_uri = f"https://{self.vault_name}.vault.azure.net"

        # Define Azure Identity Credential
        self.credential = _utils._return_credential(
            _utils._return_tenant_id()
            )

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
