"""Module to interact with Azure Keyvaults"""

import os
from azure.keyvault.secrets import SecretClient
from azure.identity import InteractiveBrowserCredential
from azure.identity import TokenCachePersistenceOptions
from azure.identity import SharedTokenCacheCredential


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
    
    print("User warning: Expect an authentication pop-up window.")
    print("You will only be asked to authenticate once the first time.")

    def __init__(self, environment: str = "prod"):

        if environment.upper() in ["DEV", "TEST", "QA", "PROD"]:
            temp_vault_name = os.getenv("KEY_VAULT_NAME")
            if temp_vault_name:
                # KEY_VAULT_NAME must include {env} for .format method
                self.vault_name = temp_vault_name.format(env=environment.lower())
            else:
                raise KeyError(
                    "KEY_VAULT_NAME environment variable not found."
                )
            if self.vault_name:
                self.kv_uri = f"https://{self.vault_name}.vault.azure.net"
            else:
                raise KeyError(
                    "KEY_VAULT_NAME environment variable not found."
                    )
        else:
            raise ValueError(
                "Environment name argument must be one of 'dev', 'test', 'qa', 'prod'."
            )

        # Do not change the value of the scope parameter. It represents the programmatic ID 
        # for Azure Databricks (2ff814a6-3304-4ab8-85cb-cd0e6f879c1d) along with the default 
        # scope (/.default, URL-encoded as %2f.default).
        scope = "2ff814a6-3304-4ab8-85cb-cd0e6f879c1d/.default"
        
        # Do not add/modify `allow_unencrypted_storage` parameter,
        # this defaults to False as intended.
        cache_options = TokenCachePersistenceOptions()

        # Establish client
        try:
            self.credential = SharedTokenCacheCredential(cache_persistence_options=cache_options)
            token = self.credential.get_token(scope)
        except Exception as e:   
            self.credential = InteractiveBrowserCredential(
                client_id="04b07795-8ddb-461a-bbee-02f9e1bf7b46",
                cache_persistence_options = cache_options,
                additionally_allowed_tenants=['*']
            )
            token = self.credential.get_token(scope) 

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
