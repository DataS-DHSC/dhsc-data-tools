Module dhsc_data_tools.dac_odbc
===============================

Functions
---------

    
`connect(environment: str = 'prod')`
:   Allows to connect to data within the DAC, and query it using SQL queries.
    
    Parameters: an environment argument, which defaults to "prod". Must be one of "dev", "qa", "test", "prod".
    
    Requires: 
    TENANT_NAME environment variable. 
    Simba Spark ODBC Driver is required. Request the latter through IT portal, install through company portal.
    
    Returns: connection object.