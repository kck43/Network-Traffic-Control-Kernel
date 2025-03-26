#!/bin/bash

set -ex -o pipefail

INTERFACE=$(ip -j link show | jq -r '.[] | select(.operstate == "UP") | .ifname' | head -n1)
if [[ -z "$INTERFACE" ]]; then
    echo "couldn't find an interface which is UP"
    exit 1
fi

NTCK_DIR=${NTCK_DIR:-$(mktemp -d)}
gcc -o $NTCK_DIR/sendeth -O2 sendeth.c

if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "setting up temporary venv"
    python3 -m venv $NTCK_DIR/venv
    source $NTCK_DIR/venv/bin/activate
    pip install -r requirements.txt
fi

bpftrace time_send_xmit.bt | tee $NTCK_DIR/output.txt &
BPFPID=$!
sleep 5
$NTCK_DIR/sendeth $INTERFACE 1000 &
SENDETHPID=$!
sleep 5

kill $SENDER $SENDETHPID
wait -fn $SENDER $SENDETHPID

python3 plot_results.py $NTCK_DIR/output.txt
