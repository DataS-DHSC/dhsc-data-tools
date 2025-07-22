# dhsc_data_tools package

## Submodules

## dhsc_data_tools.dac_odbc module

Module allows to interact with DAC SQL endpoints.

### dhsc_data_tools.dac_odbc.connect(environment: str = 'prod', refresh_token: bool = False) → Connection

Allows to connect to data within the DAC, and use SQL queries.

Requires:
: KEY_VAULT_NAME and DAC_TENANT environment variables.
  Simba Spark ODBC Driver is required.
  Request the latter through IT portal, install through company portal.

* **Parameters:**
  * **environment** (*str*) – DAC environment. Defaults to “prod”.
    Must be one of “dev”, “qa”, “test” or “prod”.
  * **refresh_token** (*bool*) – When True, will trigger re-authentication
    instead of using cached credentials. Defaults to fault.
* **Returns:**
  pyodbc.Connection

## dhsc_data_tools.keyvault module

Module to interact with Azure Keyvaults

### *class* dhsc_data_tools.keyvault.KVConnection(environment: str = 'prod', refresh_token: bool = False)

Bases: `object`

Key vault connection object.

Requires:
: KEY_VAULT_NAME and DAC_TENANT environment variables.

* **Parameters:**
  * **environment** (*str*) – DAC environment. Defaults to “prod”.
    Must be one of “dev”, “qa”, “test” or “prod”.
  * **refresh_token** (*bool*) – When True, will trigger re-authentication
    instead of using cached credentials. Defaults to fault.
* **Raises:**
  * **ValueError** – invalid environment.
  * **KeyError** – environment variables not found.

#### get_secret(secret_name: str) → str

Returns the *value* of the secret.

Args:
secret_name (str): name of the sought secret.

#### WARNING
User might have to set HTTP/HTTPS proxy as PAC context explicitly
before running kvconnection.get_secret().

## dhsc_data_tools.remote_compute module

Module allows to run code on Azure Databricks clusters.

### dhsc_data_tools.remote_compute.connect_cluster(profile: str = 'DEFAULT', file: str = 'config_yaml', cluster_uid: str | None = None) → DatabricksSession

Establishes a connection with a databricks compute cluster.

Requires:
: It relies on a yaml configuration file in the working directory,
  which by default reads config.yaml, containing profile entries
  such as:
  <br/>
  your-profile-name:
  : host=xxx
    token=xxx
    cluster_id=xxx
  <br/>
  You can also pass a cluster_id parameter manually, which will
  override the config file parameter.

* **Parameters:**
  * **profile** (*str*) – config profile name defaults to “DEFAULT”.
  * **file** (*str*) – the config file’s name or path.
  * **[****Optional****]** (*cluster_uid*) – specify cluster to run code on.
    Connects to default shared if not specified.
* **Returns:**
  DatabricksSession

## dhsc_data_tools.tools module

Tooling to work with DAC data.

### dhsc_data_tools.tools.df_from_dataflow(dataflow: str, connection: Connection = None) → DataFrame

Get data into a pandas DataFrame. Either custom SQL query, or full dataflow path.

* **Parameters:**
  * **dataflow** (*str*) – full dataflow path. (Pass either dataflow or sql.)
  * **[****Optional****]** (*connection*) – ODBC connection object.
    Defaults to None, in which case creates own connection.
* **Returns:**
  pd.DataFrame

### dhsc_data_tools.tools.df_from_sql(sql: str, connection: Connection = None) → DataFrame

Get data into a pandas DataFrame. Either custom SQL query, or full dataflow path.

* **Parameters:**
  * **sql** (*str*) – sql query.
  * **[****Optional****]** (*connection*) – ODBC connection object.
    Defaults to None, in which case creates own connection.
* **Returns:**
  pd.DataFrame

### dhsc_data_tools.tools.get_catalogs(connection: Connection = None) → DataFrame

Gets catalogs on the DAC.

* **Parameters:**
  **[****Optional****]** (*connection*) – ODBC connection object.
  Defaults to None, in which case creates own connection.
* **Returns:**
  pd.DataFrame

### dhsc_data_tools.tools.get_schemas(catalog: str, connection: Connection = None) → DataFrame

Gets all schemas within the catalog.

* **Parameters:**
  * **catalog** (*str*) – catalog name.
  * **[****Optional****]** (*connection*) – ODBC connection object.
    Defaults to None, in which case creates own connection.
* **Returns:**
  pd.DataFrame

### dhsc_data_tools.tools.get_table_info(catalog: str, schema: str, table: str, connection: Connection = None) → DataFrame

Gets table description of a given table.

* **Parameters:**
  * **catalog** (*str*) – catalog name.
  * **schema** (*str*) – schema name.
  * **table** (*str*) – table name.
  * **[****Optional****]** (*connection*) – ODBC connection object.
    Defaults to None, in which case creates own connection.
* **Returns:**
  pd.DataFrame

### dhsc_data_tools.tools.get_tables(catalog: str, schema: str, connection: Connection = None) → DataFrame

Gets all tables within a given schema.

* **Parameters:**
  * **catalog** (*str*) – catalog name.
  * **schema** (*str*) – schema name.
  * **[****Optional****]** (*connection*) – ODBC connection object.
    Defaults to None, in which case creates own connection.
* **Returns:**
  pd.DataFrame

## Module contents

This module allows users to interact with the DAC.
