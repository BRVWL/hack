#!/usr/bin/env python

import scapy.all as scapy

# Use ARP protocol 
def scan(ip):
  scapy.arping(ip)

scapy("192.168.0.1/24")
 
