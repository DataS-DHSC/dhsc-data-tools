# Getting started

## dhsc_data_tools package

**Stable branch: main**

The goal of DHSCdatatools is to provide a suite of tools for using data hosted on the DHSC analytical cloud (DAC) platform.
[For detailed documentation click here.](./docs/build/markdown/index.md)

### Getting started

#### Pre-requisites

1. Local installation of Simba Spark ODBC Driver 32-bit and Simba Spark ODBC Driver 64-bit. Request these through the IT portal.
2. Activate conda environment. To create a new env, in Git Bash:

```default
conda create -n <your_environment_name> python==3.12 pip
```

> Some of the dependencies of this package are not currently compatible with the latest Python 3.13. Use any python version from and including 3.8 and below 3.13. E.g. above `python==3.12` is specified.
1. Though not strictly a package dependency, we recommend you install python-dotenv to work with environment variables.

In Git Bash, **\*with the relevant environment activated\***:

```default
pip install python-dotenv
```

#### Install the dhsc_data_tools package

In Git Bash, **\*with the relevant environment activated\***, to install **dhsc_data_tools**:

```default
pip install git+https://github.com/DataS-DHSC/dhsc-data-tools.git
```

### .env and config files

A .env file containing tenant name and key vault name is required for `dhsc_data_tools.dac_odbc.connect()` and `dhsc_data_tools.keyvault.KVConnection()`.
Please find the .env file in the [Data Science Teams space DAC channel](https://teams.microsoft.com/l/channel/19%3ad94b5e4692d043249285162a04b35d12%40thread.tacv2/DAC%2520(DHSC%2520analytical%2520cloud)?groupId=88d91456-9588-4bed-a713-fde91b11a227&tenantId=61278c30-91a8-4c31-8c1f-ef4de8973a1c).

Place this file in your working directory.

**IMPORTANT**

**Ensure in each project your \`\`.gitignore\`\` file excludes config, \`\`.env\`\`, and relevant yaml files.**
If you do accidentally commit these files (or any other sensitive data) please get in touch with the [Data Science Hub](mailto:datascience@dhsc.gov.uk) to discuss how best to mitigate the breach.

#### Example use scripts

##### Connecting to the DAC data using an SQL endpoint

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

# For help, you can run
help(dac_odbc.connect) # or with any other module
```

### QA Status

Everything in the main branch has been through QA.

### Code of Conduct

Please note that the DHSCdatatools project is released with a [Contributor Code of Conduct](https://contributor-covenant.org/version/2/1/CODE_OF_CONDUCT.html).
By contributing to this project, you agree to abide by its terms.

### Contributing

Contributions are welcome.

#### Dev setup

Clone this repository.

Install requirements from `pyproject.toml`, including development and documentation dependencies.

```default
pip install . .[dev] .[docs] dotenv
```

#### Build package

Build dists.

```default
build .
```

#### Update docs

This will update the docs.

```default
sphinx-apidoc -o docs/source src/dhsc_data_tools && sphinx-build -M markdown docs/source/ docs/build/
```

### Licence

Unless stated otherwise, the codebase is released under the MIT License. This covers both the codebase and any sample code in the documentation.

All other content is [© Crown copyright](http://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/uk-government-licensing-framework/crown-copyright/)
and available under the terms of the [Open Government 3.0 licence](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/), except where otherwise stated.
