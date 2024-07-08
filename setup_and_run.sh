#!/bin/bash

# Check if the file_to_convert.py exists in the current directory
if [ ! -f "file_to_convert.py" ]; then
    echo "file_to_convert.py not found in the current directory."
    exit 1
fi

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install required packages
echo "Installing required packages..."
pip install python-docx

# Run the file_to_convert.py script
echo "Running the file_to_convert.py script..."
python file_to_convert.py

# Deactivate the virtual environment
deactivate

echo "Done."
