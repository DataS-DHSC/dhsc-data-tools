Module dhsc_data_tools.keyvault
===============================

Classes
-------

`kvConnection(environment='prod')`
:   Key vault connection object.
    
    Class takes an environment name argument, which must be one of 
    "dev", "test", "qa", "prod". Defaults to "prod". (Not case sensitive.)
    It will look for a corresponding key vault name in environment variables.

    ### Methods

    `get_secret(self, secret_name)`
    :   Returns the *value* of the secret.
        
        `get_secret()` method requires the name of the sought secret to be passed as an argument.
        
        User might have to set HTTP/HTTPS proxy as PAC context explicitly 
        before running kvconnection.get_secret().