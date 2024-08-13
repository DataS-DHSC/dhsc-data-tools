Module dhsc_data_tools.dac_odbc
===============================
Module dac_odbc allows to interact with DAC SQL endpoints.

Functions
---------

    
`connect(environment: str = 'prod', refresh_token: bool = False)`
:   Allows to connect to data within the DAC, and use SQL queries.
    
    Parameters:
    an `environment` argument, which defaults to "prod".
    Must be one of "dev", "qa", "test" or "prod".
    
    `refresh_token`: when True, will trigger re-authentication
    instead of using cached credentials. False by default.
    
    Requires:
    KEY_VAULT_NAME and DAC_TENANT environment variables.
    Simba Spark ODBC Driver is required.
    Request the latter through IT portal, install through company portal.
    
    Returns: connection object.