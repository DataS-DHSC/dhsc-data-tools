#!/usr/bin/env bash

sphinx-apidoc -o docs/source dhsc_data_tools\
    && sphinx-build -M markdown docs/source/ docs/build/
