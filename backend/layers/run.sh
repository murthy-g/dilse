#!/bin/bash

# Set constants
PYTHON_VERSION="3.8"
LAYER_DIR="layers/python/lib/python3.8/site-packages"
ZIP_NAME="layers.zip"

# Function to create and activate virtual environment
create_virtual_env() {
    echo "Creating virtual environment with Python $PYTHON_VERSION..."
    python${PYTHON_VERSION} -m venv venv
    source venv/bin/activate
}

# Function to upgrade pip and install required packages
install_packages() {
    echo "Upgrading pip and installing required packages..."
    pip cache purge
    pip install --upgrade pip
    mkdir -p ${LAYER_DIR}
    pip install -r requirements.txt -t ${LAYER_DIR}
}

# Function to zip the installed packages and models for AWS Lambda Layer
zip_layer() {
    echo "Zipping installed packages and models..."
    
    # Add models to the layers directory
    cp -r ../models/*.py ${LAYER_DIR}

    cd ${LAYER_DIR}
    zip -r9 ${ZIP_NAME} .
    mv ${ZIP_NAME} ../../../..   # Move zip file back to the root directory
}

# Function to deactivate and clean up virtual environment
cleanup() {
    echo "Cleaning up..."
    deactivate
    rm -r venv
}

# Main script execution
create_virtual_env
install_packages
zip_layer
cleanup

echo "Done!"
