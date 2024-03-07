import os
from azure.keyvault.secrets import SecretClient
from azure.identity import InteractiveBrowserCredential

class kvConnection:
    '''
    Key vault connection object.
    
    Class takes an environment name argument, which must be one of 
    "dev", "test", "qa", "prod". Defaults to "prod". (Not case sensitive.)
    It will look for a corresponding key vault name in environment variables.

    get_secret() method requires the name of the sought secret to be passed 
    as an argument, and it returns the *value* of the secret.

    User might have to set HTTP/HTTPS proxy as PAC context explicitly 
    before running kvconnection.get_secret().
    '''

    def __init__(self, environment="prod"):
        
        if environment.upper() in ["DEV", "TEST", "QA", "PROD"]:
            vault_name = os.getenv('KEY_VAULT_'+environment.upper())
            if vault_name:
                self.KVUri = f"https://{vault_name}.vault.azure.net"
            else:
                raise KeyError(f"No environment variable corresponding to KEY_VAULT_{environment.upper()}")
        else:
            raise ValueError("Environment name argument must be one of 'dev', 'test', 'qa', 'prod'.")

        self.credential = InteractiveBrowserCredential(client_id="04b07795-8ddb-461a-bbee-02f9e1bf7b46",
                                                       additionally_allowed_tenants="*"
                                                       )
        
        self.client = SecretClient(vault_url=self.KVUri, credential=self.credential)

    def get_secret(self, secret_name):
        #get and return key
        return self.client.get_secret(secret_name).value