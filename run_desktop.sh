#!/bin/bash

# Create a virtual environment and install the base dependencies using poetry
poetry install

# Install the specific desktop dependencies from the requirements.txt file
poetry run pip install -r desktop/requirements.txt

# Run the PySide6 desktop application
poetry run python desktop/main.py
