# dhsc_data_tools package

The goal of DHSCdatatools is to provide a suite of tools for using data hosted on the DHSC analytical cloud (DAC) platform. 
[For detailed developer documentation click here.](https://github.com/DataS-DHSC/dhsc-data-tools/tree/main/docs/dhsc_data_tools)

**In development - not ready for use**

This repository contains tools to work with the DAC from local Python installation.

## Pre-requisites

A new conda environment is recommended for the package. In Git Bash:

```
conda create -n <your_environment_name> pip python-dotenv
```

## To install the dhsc_data_tools package

In Git Bash, with your relevant environment activated:

```
pip install git+https://github.com/DataS-DHSC/dhsc-data-tools.git
```

## .env and config files

A .env file containing tenant name and key vault name is required for `dhsc_data_tools.dac_odbc.connect()` and `dhsc_data_tools.keyvault.kvConnection()`.

**IMPORTANT**

**Ensure in each project your `.gitignore` file excludes `.env` and `.config` files.**
If you do accidentally commit these files (or any other sensitive data) please get in touch with the [Data Science Hub](mailto:datascience@dhsc.gov.uk) to discuss how best to mitigate the breach.

## Example use scripts

### Connecting to the DAC data using an SQL endpoint

```python
from dhsc_data_tools import dac_odbc
from dotenv import load_dotenv
load_dotenv(".env")

#create client
conn = dac_odbc.connect()

# Run a SQL query by using the preceding connection.
cursor = conn.cursor()
cursor.execute("SELECT * FROM samples.nyctaxi.trips LIMIT 10")

# Print the rows retrieved from the query.
for row in cursor.fetchall():
    print(row)
```

## Code of Conduct

Please note that the DHSCdatatools project is released with a [Contributor Code of Conduct](https://contributor-covenant.org/version/2/1/CODE_OF_CONDUCT.html).
By contributing to this project, you agree to abide by its terms.

## Licence

Unless stated otherwise, the codebase is released under the MIT License. This covers both the codebase and any sample code in the documentation.

All other content is [© Crown copyright](http://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/uk-government-licensing-framework/crown-copyright/)
and available under the terms of the [Open Government 3.0 licence](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/), except where otherwise stated.