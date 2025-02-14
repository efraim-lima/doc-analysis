#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Upgrade pip
pip install --upgrade pip

echo "Development environment setup complete!"
echo "To activate the virtual environment, run: source venv/bin/activate" 