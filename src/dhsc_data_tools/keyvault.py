"""Module to interact with Azure Keyvaults"""

import os

from azure.keyvault.secrets import SecretClient

from src.dhsc_data_tools import _auth_utils


class KVConnection:
    """Key vault connection object.

    Args:
    environment (str): DAC environment. Defaults to "prod".
        Must be one of "dev", "qa", "test" or "prod".

    refresh_token (bool): When True, will trigger re-authentication
        instead of using cached credentials. Defaults to fault.

    Requires:
        KEY_VAULT_NAME and DAC_TENANT environment variables.

    Raises:
        ValueError: invalid environment.
        KeyError: environment variables not found.
    """

    def __init__(self, environment: str = "prod", refresh_token: bool = False):
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
        self.credential = _auth_utils._return_credential(
            tenant_id=_auth_utils._return_tenant_id(), refresh_token=refresh_token
        )

        # Establish Azure Keyvault SecretClient
        self.client = SecretClient(vault_url=self.kv_uri, credential=self.credential)

    def get_secret(self, secret_name: str) -> str:
        """Returns the *value* of the secret.

        Args:
        secret_name (str): name of the sought secret.

        Warning:
            User might have to set HTTP/HTTPS proxy as PAC context explicitly
            before running kvconnection.get_secret().
        """

        print("Getting secret...")

        return self.client.get_secret(secret_name).value
