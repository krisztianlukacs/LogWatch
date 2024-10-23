#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to display usage information
usage() {
    echo "Usage: $0 <PARAMETERONEFILE> [FILTER]"
    exit 1
}

# Check if exactly one argument is provided
#if [ "$#" -ne 1 ]; then
#    echo "Error: Exactly one parameter is required."
#    usage
#fi

# Assign the first argument to a variable
PARAMETERONEFILE="$1"

# Check if the second argument is provided
if [ "$#" -eq 2 ]; then
    FILTER="$2"
else
    FILTER=""
fi

# Define the paths
LOGWATCH_SCRIPT="/home/lukacsk/bin/logwatch/LogWatch.py"
CONFIG_FILE="/home/lukacsk/bin/logwatch/colorconfig.json"

# Check if LogWatch.py exists and is executable
if [ ! -f "$LOGWATCH_SCRIPT" ]; then
    echo "Error: LogWatch.py not found at $LOGWATCH_SCRIPT."
    exit 1
fi

if [ ! -x "$LOGWATCH_SCRIPT" ]; then
    echo "LogWatch.py is not executable. Attempting to set executable permission."
    chmod +x "$LOGWATCH_SCRIPT"
fi

# Check if config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Configuration file not found at $CONFIG_FILE."
    exit 1
fi

# Execute the Python script with the provided parameter and config file
"$LOGWATCH_SCRIPT" "$PARAMETERONEFILE" "$CONFIG_FILE" "$FILTER"

