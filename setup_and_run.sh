#!/bin/bash

# Load environment variables from .env file
set -a
[ -f .env ] && . .env
set +a

# Check if the config file path is set
if [ -z "$CONFIG_FILE_PATH" ]; then
    echo "Config file path is not set in the .env file."
    exit 1
fi

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install --upgrade pip
pip install requests pyyaml python-dotenv

# Run the Python script
echo "Running the Python script..."
python update_traefik_and_pihole.py $CONFIG_FILE_PATH

# Deactivate the virtual environment
deactivate

echo "Done."
