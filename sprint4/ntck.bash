#!/bin/bash

set -ex -o pipefail

# Get the first active network interface for later.
INTERFACE=${INTERFACE:-$(ip -j link show | jq -r '.[] | select(.operstate == "UP") | .ifname' | head -n1)}
if [[ -z "$INTERFACE" ]]; then
    echo "couldn't find an interface which is UP"
    exit 1
fi
# Check that bpftrace can run.
bpftrace -e 'BEGIN { exit() }' >/dev/null

# Create a temporary directory for artifacts and outputs.
NTCK_DIR=${NTCK_DIR:-$(mktemp -d)}
gcc -o $NTCK_DIR/sendeth -O2 sendeth.c

# Check that a Python virtual env is active.
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "setting up temporary venv"
    python3 -m venv $NTCK_DIR/venv
    source $NTCK_DIR/venv/bin/activate
    pip install -r requirements.txt
fi

# Start collecting metrics.
bpftrace time_send_xmit.bt > $NTCK_DIR/output.txt &
BPFPID=$!
sleep 5

# Dump packets to make sure something is metricked.
$NTCK_DIR/sendeth $INTERFACE 1000

# End the background job.
kill $BPFPID
wait -fn $BPFPID

# Produce the plots.
python3 plot_results.py $NTCK_DIR/output.txt
