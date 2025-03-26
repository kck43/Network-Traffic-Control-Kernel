#!/bin/bash

set -ex -o pipefail

INTERFACE=$(ip -j link show | jq -r '.[] | select(.operstate == "UP") | .ifname' | head -n1)
if [[ -z "$INTERFACE" ]]; then
    echo "couldn't find an interface which is UP"
    exit 1
fi

DIR=$(mktemp -d)
python3 -m venv $DIR/venv
source $DIR/venv/bin/activate
pip install -r requirements.txt
gcc -o $DIR/sendeth -O2 sendeth.c

bpftrace time_send_xmit.bt | tee output.txt &
BPFPID=$!
sleep 5
$DIR/sendeth $INTERFACE 1000 &
SENDETHPID=$!
sleep 5

kill $SENDER $SENDETHPID
wait -fn $SENDER $SENDETHPID

python3 plot_results.py output.txt
