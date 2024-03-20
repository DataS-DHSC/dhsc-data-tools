"""Module to interact with Azure Keyvaults"""

import os
from azure.keyvault.secrets import SecretClient
from azure.identity import InteractiveBrowserCredential


class kvConnection:
    """
    Key vault connection object.

    Parameters:
    Takes an environment name parameter, which must be one of
    "dev", "test", "qa", "prod". Defaults to "prod". (Not case sensitive.)
    It will look for a corresponding key vault name in environment variables.

    Requires: KEY_VAULT_NAME environment variable.

    Returns: Azure Keyvault Connection object.
    """

    def __init__(self, environment: str = "prod"):
        if environment.upper() in ["DEV", "TEST", "QA", "PROD"]:
            temp_vault_name = os.getenv("KEY_VAULT_NAME")
            try:
                self.vault_name = temp_vault_name.format(env=environment.lower())
            except AttributeError as exc:
                raise AttributeError(
                    "KEY_VAULT_NAME environment variable not found."
                ) from exc
            if self.vault_name:
                self.kv_uri = f"https://{self.vault_name}.vault.azure.net"
            else:
                raise KeyError("KEY_VAULT_NAME environment variable not found.")
        else:
            raise ValueError(
                "Environment name argument must be one of 'dev', 'test', 'qa', 'prod'."
            )

        self.credential = InteractiveBrowserCredential(
            client_id="04b07795-8ddb-461a-bbee-02f9e1bf7b46",
            additionally_allowed_tenants="*",
        )

        self.client = SecretClient(vault_url=self.kv_uri, credential=self.credential)

    def get_secret(self, secret_name: str):
        """Returns the *value* of the secret.

        Parameters:
        `get_secret()` method requires the name of the sought secret to be passed as an argument.

        Please note:
        User might have to set HTTP/HTTPS proxy as PAC context explicitly
        before running kvconnection.get_secret().
        """
        return self.client.get_secret(secret_name).value
