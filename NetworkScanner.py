import argparse
from scapy.all import ICMP, IP, sr1

def network_scanner(network):
    print(f"Scanning network: {network}")

    for i in range(1, 5):
        ip = f"{network}.{i}"
        packet = IP(dst=ip)/ICMP()
        
        response = sr1(packet, timeout=1, verbose=0)
        
        if response:
            print(f"Host {ip} is up")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Network Scanner")
    parser.add_argument("network", help="Network segment to scan (e.g., 192.168.1)")

    args = parser.parse_args()
    network_segment = args.network
    network_scanner(network_segment)
