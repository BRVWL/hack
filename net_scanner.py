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
    clients_list = []
    for item in answered:
        # print(item[1].show())
        answered_ip_address = item[1].psrc
        answered_mac_address = item[1].hwsrc
        current_client = {
          "ip": answered_ip_address,
          "mac": answered_mac_address
        }
        clients_list.append(current_client)
    return clients_list


def output_scanned_network(answered_list):
    print("IP\t\t\t\tMAC\n__________________________________________________")
    for client in answered_list:
        print(client["ip"] + "\t\t\t" + client["mac"])


list = scan("10.0.2.1/24")

output_scanned_network(list)
