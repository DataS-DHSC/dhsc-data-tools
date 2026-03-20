#!/usr/bin/env bash

set -euo pipefail
IFS=$'\n\t'

uv init

if [ -f requirements.txt ]; then
    uv add -r requirements.txt
elif [ -f pyproject.toml ]; then
    uv sync --all-extras
else
    echo "No dependencies file found."
    exit 1
fi
