# Josh's sprint 2 script
## Overview
Simulates network egress and captures tracepoint timestamps for analysis.
The python file currently only compiles a dataframe, can do more with this like visualization going forward.

### trace_net.bt 
* attaches 5 tracepoints
### send_raw_eth.c
* sends NUM_PACKETS raw ethernet packets 
### tabulate results.py
* compiles output of bpftrace into a pandas DataFrame

## Setup 
1. create a python virtual environment with ```python3 -m venv venv```
2. activate the venv with ```source venv/bin/activate```
3. install necessary dependencies with pip install -r requirements.txt

## Compilation
1. compile the send_raw_eth_2.c file with ```gcc -o send_raw_eth_2 send_raw_eth_2.c```

## Running the program
1. start the bpftrace script in one terminal with ```bpftrace trace_net.bt > output.txt```
2. run the send_raw_eth program
3. tabulate the results with ```python tabulate_results.py```

## Changing number of packets sent by send_raw_eth_2:
* Open the send_raw_eth_2.c file
* Edit the ```NUM_PACKETS``` definition to your desired number of packets
* Recompile and run the program

## Output
THe program is supposed to output two jpgs of graphs, and a csv of the aggregated timestamps & latencies. THe graph that gets saved to
```timeline_plot.jph``` comes out looking wrong, but the data is also saved to a csv so generating graphs with Sheets or Excel may be preferred.

