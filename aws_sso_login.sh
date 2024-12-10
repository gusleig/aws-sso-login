#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Load environment variables from .env file
if [ -f "$SCRIPT_DIR/.env" ]; then
    source "$SCRIPT_DIR/.env"
else
    echo "Error: .env file not found in $SCRIPT_DIR"
    exit 1
fi

# Verify that PYTHON_SCRIPT_PATH is set
if [ -z "$PYTHON_SCRIPT_PATH" ]; then
    echo "Error: PYTHON_SCRIPT_PATH is not set in .env file"
    exit 1
fi

# Verify that the Python script exists
if [ ! -f "$PYTHON_SCRIPT_PATH" ]; then
    echo "Error: Python script not found at $PYTHON_SCRIPT_PATH"
    exit 1
fi

# Expand the AWS_ENV_FILE path
AWS_ENV_FILE="${AWS_ENV_FILE/#\~/$HOME}"
AWS_ENV_FILE="${AWS_ENV_FILE/#\$HOME/$HOME}"

# Run the Python script and source the credentials if successful
python3 "$PYTHON_SCRIPT_PATH" && {
    if [ -f "$AWS_ENV_FILE" ]; then
        source "$AWS_ENV_FILE"
        echo "Successfully loaded AWS credentials"
    else
        echo "Error: Credentials file not found at $AWS_ENV_FILE"
        exit 1
    fi
}