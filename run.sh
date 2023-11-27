#!/bin/bash

# Function to clean up and terminate the second process
cleanup() {
    echo "Cleaning up and terminating the second process"
    # Replace 'second_process' with the actual name or command of your second process
    pkill -TERM -f 'python'
    exit 0
}

# Set up a trap to call the cleanup function when the script receives the EXIT signal
trap cleanup EXIT

# Start the first process
# Replace 'first_process' with the actual name or command of your first process
./.venv/bin/python -m http.server &

# Start the second process
# Replace 'second_process' with the actual name or command of your second process
./.venv/bin/python ./resume_combinator.py &

wait

