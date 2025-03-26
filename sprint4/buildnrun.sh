#!/bin/sh

docker build -t ntck .
docker run --privileged --net=host --pid=host -it \
    -v /usr/src:/usr/src:ro \
    -v /lib/modules:/lib/modules:ro \
    -v /sys/kernel/debug:/sys/kernel/debug:rw \
    -v /sys/kernel/btf/vmlinux:/sys/kernel/btf/vmlinux:ro \
    -v /usr/src/linux-headers-$(uname -r):/usr/src/linux-headers-$(uname -r):ro \
    ntck
