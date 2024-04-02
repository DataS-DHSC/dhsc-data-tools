Module dhsc_data_tools.keyvault
===============================
Module to interact with Azure Keyvaults

Classes
-------

`kvConnection(environment: str = 'prod')`
:   Key vault connection object.
    
    Parameters:
    Takes an environment name parameter, which must be one of
    "dev", "test", "qa" or "prod". Defaults to "prod". (Not case sensitive.)
    It will look for a corresponding key vault name in environment variables.
    
    Requires: KEY_VAULT_NAME and DAC_TENANT environment variables.
    
    Returns: Azure Keyvault Connection object.

    ### Methods

    `get_secret(self, secret_name: str)`
    :   Returns the *value* of the secret.
        
        Parameters:
        `get_secret()` method requires the name of the sought secret to be passed as an argument.
        
        Please note:
        User might have to set HTTP/HTTPS proxy as PAC context explicitly
        before running kvconnection.get_secret().