FROM debian:latest

RUN apt-get update
RUN apt-get install -y \
    bpftrace \
    jq \
    build-essential \
    python3-pip \
    python3-venv \
    iproute2

COPY ntck.bash plot_results.py requirements.txt sendeth.c time_send_xmit.bt /
RUN chmod +x /ntck.bash /plot_results.py

VOLUME ["/usr/src", "/lib/modules", "/sys/kernel/debug"]

ENTRYPOINT ["/ntck.bash"]
