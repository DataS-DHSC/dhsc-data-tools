Module dhsc_data_tools.dataconnect
==================================

Functions
---------

    
`db_connect(environment='prod')`
:   This function allows to connect to data within the DAC,
    and query it using SQL queries.
    
    Simba Spark ODBC Driver is required.
    
    Expects environment variables for tenant name,