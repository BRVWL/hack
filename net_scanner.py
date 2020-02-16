#!/usr/bin/env python

import scapy.all as scapy


# def scan(ip):
#     scapy.arping(ip)


# Use ARP protocol
def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    brod_cast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_brodcast_request = brod_cast / arp_request
    # answered this is who use this network
    answered = scapy.srp(arp_brodcast_request, timeout=1, verbose=False)[0]
    return answered


def output_scanned_network(answered_list):
    print("IP\t\t\t\tMAC\n__________________________________________________")
    for item in answered_list:
        # print(item[1].show())
        answered_ip_address = item[1].psrc
        answered_mac_address = item[1].hwsrc
        print(answered_ip_address + "\t\t\t" + answered_mac_address)


list = scan("10.0.2.1/24")

output_scanned_network(list)
