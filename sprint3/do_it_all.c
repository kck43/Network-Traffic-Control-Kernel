#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>

int main(int argc, char* argv[]) {
    char *num_packets = argv[1];

    pid_t bpftrace_pid, send_raw_eth_pid;

    // Start bpftrace command with output redirection
    bpftrace_pid = fork();
    if (bpftrace_pid == 0) {
        // Open output.txt for writing
        int fd = open("output.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
        if (fd < 0) {
            perror("open output.txt");
            exit(EXIT_FAILURE);
        }

        // Redirect stdout to output.txt
        dup2(fd, STDOUT_FILENO);
        close(fd);

        execlp("bpftrace", "bpftrace", "time_send_xmit.bt", (char *)NULL);
        perror("execlp bpftrace");
        exit(EXIT_FAILURE);
    }

    // Wait for 10 seconds
    sleep(10);

    // Start send_raw_eth_2 command
    send_raw_eth_pid = fork();
    if (send_raw_eth_pid == 0) {
        execlp("./send_raw_eth_2", "./send_raw_eth_2", num_packets, (char *)NULL);
        perror("execlp send_raw_eth_2");
        exit(EXIT_FAILURE);
    }

    // Wait for send_raw_eth_2 to finish
    waitpid(send_raw_eth_pid, NULL, 0);

    // Send SIGINT to bpftrace process
    kill(bpftrace_pid, SIGINT);

    // Wait for bpftrace to terminate
    waitpid(bpftrace_pid, NULL, 0);

    // Run python3 plot_results.py
    if (fork() == 0) {
        execlp("python3", "python3", "plot_results.py", (char *)NULL);
        perror("execlp python3");
        exit(EXIT_FAILURE);
    }

    return 0;
}
