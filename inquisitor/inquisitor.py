import argparse
import re
import logging
import sys


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
    parser.add_argument("src_ip", metavar="IP-src", help= "source IP address")
    parser.add_argument("src_mac", metavar="MAC-src", help= "source MAC address (format AA:BB:DD:EE:FF)")
    parser.add_argument("target_ip", metavar="IP-target", help= "target IP address")
    parser.add_argument("target_mac", metavar="MAC-target", help= "target MAC address (format AA:BB:DD:EE:FF)")
    parser.add_argument("-v","--verbose", action="store_true", help="Verbose mode - show all FTP traffic including")
    args = parser.parse_args()
    if not validate_ipv4(args.src_ip) or not validate_ipv4(args.target_ip):
        parser.error("Invalid IP address format")
    if not validate_mac(args.src_mac) or not validate_mac(args.target_mac):
        parser.error("Invalid MAC format")
    logging.info("Source (spoofed) IP: {args.src_ip} MAC: {args.src_mac}")
    logging.info("Victim IP: {args.target_ip} MAC: {args.target_mac}")
    return args


def main():
    if len(sys.argv) < 5:
        logging.info("You need at least 4 parameters, ./inquisitor.py -h for more information")
        sys.exit(1)
    try:
        args = parse_args()

    
    except KeyboardInterrupt:
        logging.info("Interrupted by user CTRL+C")
        sys.exit(0)
        
    except Exception as e:
        logging.error("Error {e}")
        sys.exit(1)

if __name__ == '__main__':
   main()