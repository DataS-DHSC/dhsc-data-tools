Module dhsc_data_tools.dac_odbc
===============================
Module dac_odbc allows to interact with DAC SQL endpoints.

Functions
---------

    
`connect(environment: str = 'prod')`
:   Allows to connect to data within the DAC, and query it using SQL queries.
    
    Parameters: an environment argument, which defaults to "prod".
    Must be one of "dev", "qa", "test" or "prod".
    
    Requires:
    KEY_VAULT_NAME and DAC_TENANT environment variables.
    Simba Spark ODBC Driver is required.
    Request the latter through IT portal, install through company portal.
    
    Returns: connection object.