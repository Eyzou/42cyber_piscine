import argparse
import re


def validate_ipv4(ip):
    pattern = re.compile(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')
    match = pattern.match(ip)

    if not match:
        return False

    return all(0 <= int(octet) <= 255 for octet in match.groups())

def validate_mac(mac):
    pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]?){5}([0-9A-Fa-f]{2})$')
    return pattern.match(mac) is not None

def parse_args():
    parser = argparse.ArgumentParser(prog="Inquisitor",
                                     description="ARP spoofing or ARP poisoning program",
                                     epilog="./inquisitor <src_ip> <src_mac> <target_ip> <target_mac>")
    parser.add_argument("IP-src", help= "source IP address")
    parser.add_argument("MAC-src", help = "source MAC address (format AA:BB:DD:EE:FF)")
    parser.add_argument("IP-target", help= "target IP address")
    parser.add_argument("MAC-target", help = "target MAC address (format AA:BB:DD:EE:FF)")
    parser.add_argument("-v","--verbose", action="store_true")
    args = parser.parse_args()
    return args

def main():
    args = parse_args()

if __name__ == '__main__':
   main()