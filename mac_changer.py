#!/usr/bin/env python

import subprocess
import optparse
import re

# Define function for getting args
# Example
# python <name>.py -i wlan0 -m 00:11:22:33:44:66
# python <name>.py --interface wlan0 --mac 00:11:22:33:44:66
def get_args():
  parser = optparse.OptionParser()
  parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address")
  parser.add_option("-m", "--mac", dest="mac_address", help="New MAC address")
  (options, agruments) = parser.parse_args()
  if not options.interface:
    parser.error("[-] Please specify an interface, use --help for more info")
  elif not options.mac_address:
    parser.error("[-] Please specify a new mac address, use --help for more info")
  return options

# Define function for getting MAC address
def get_mac_address(interface):
  # Save data from ifconfig command
  ifconfig_result = subprocess.check_output(["ifconfig", interface])
  # Search MAC address by regexp
  finded_mac_address = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
  if finded_mac_address:
    mac_addres = finded_mac_address.group(0)
    return mac_addres
  else:
    print("[-] Could not find MAC address ")

# Define change mac function
def change_mac(interface, mac_address):
  subprocess.call(["ifconfig", interface, "down"], shell=True)
  subprocess.call(["ifconfig", interface, "hw", "ether", mac_address], shell=True)
  subprocess.call(["ifconfig", interface, "up"], shell=True)


# RUN 

# Get values from args 
options = get_args()

# Get the mac address
current_mac_address = get_mac_address(options.interface)
print("Current MAC address is - " + str(current_mac_address))

# Changing MAC address
change_mac(options.interface, options.mac_address)

# Recheck chenged mac addres
current_mac_address = get_mac_address(options.interface)
if current_mac_address == options.mac_address:
  print("[+] MAC address was changed")
else:
  print("[-] MAC address was'not change")
