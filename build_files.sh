#!/bin/bash
# Install Python and pip if they are not available
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed. Installing Python..."
    apt-get update && apt-get install -y python3 python3-pip
fi

if ! command -v pip3 &> /dev/null
then
    echo "pip3 is not installed. Installing pip3..."
    apt-get install -y python3-pip
fi

# Run pip to install dependencies
pip3 install -r requirements.txt
