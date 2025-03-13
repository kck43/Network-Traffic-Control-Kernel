#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/ether.h>
#include <netpacket/packet.h>
#include <net/if.h>
#include <sys/ioctl.h>

#define ETH_P_CUSTOM 0x88B5 // Custom EtherType for filtering
#define IFACE "enp0s3"        // Change this to your network interface
#define NUM_PACKETS 10

int main() {
    int sockfd;
    struct ifreq ifr;
    struct sockaddr_ll sa;
    unsigned char packet[1024];

    // Create a raw socket
    sockfd = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_CUSTOM));
    if (sockfd < 0) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    // Get interface index
    memset(&ifr, 0, sizeof(ifr));
    strncpy(ifr.ifr_name, IFACE, IFNAMSIZ - 1);
    if (ioctl(sockfd, SIOCGIFINDEX, &ifr) < 0) {
        perror("ioctl");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    // Set up sockaddr_ll
    memset(&sa, 0, sizeof(sa));
    sa.sll_ifindex = ifr.ifr_ifindex;
    sa.sll_halen = ETH_ALEN;
    memset(sa.sll_addr, 0xFF, ETH_ALEN); // Broadcast or set a custom MAC

    // Build Ethernet frame
    struct ethhdr *eth = (struct ethhdr *)packet;
    memset(eth->h_dest, 0xAA, ETH_ALEN); // Dummy destination MAC (AA:AA:AA:AA:AA:AA)
    memset(eth->h_source, 0xBB, ETH_ALEN); // Dummy source MAC (BB:BB:BB:BB:BB:BB)
    eth->h_proto = htons(ETH_P_CUSTOM); // Custom EtherType

    unsigned short packetIdentifier = 0;
    // Fill payload with a simple pattern
    memset(packet + sizeof(struct ethhdr), 0x42, sizeof(packet) - sizeof(struct ethhdr));

    // Send packet
    for(int i = 0; i < NUM_PACKETS; i++) {
        if (sendto(sockfd, packet, sizeof(packet), 0, (struct sockaddr *)&sa, sizeof(sa)) < 0) {
            perror("sendto");
            close(sockfd);
            exit(EXIT_FAILURE);
        }
    }

    printf("Dummy packet sent.\n");

    close(sockfd);
    return 0;
}
