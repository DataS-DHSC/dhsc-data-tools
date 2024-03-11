# dhsc_data_tools package

**In development - not ready for use**

This repository contains tools to work with the DAC from local Python installation.

## Pre-requisites

To create a new conda environment, in Git Bash:

```
conda create -n <your_environment>
```

(Optional) To load .env files, the `python-dotenv` package can be used. First activate the environment just created:

```
conda activate <your-environment>
```

Then install dotenv:

```
conda install conda-forge::python-dotenv
```

## To install the dhsc_data_tools package

In Git Bash, with your relevant environment activated:

```
conda install git+https://github.com/DataS-DHSC/dhsc-data-tools.git
```