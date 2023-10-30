import socket
import argparse
import pyfiglet
import concurrent.futures
from datetime import datetime

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"Port {port} is open")
        sock.close()
    except (socket.timeout, ConnectionRefusedError, OSError):
        pass

def scan_ports(target):
    print("-" * 50)
    print(f"Scanning target: {target}")
    print(f"Started scanning at: {str(datetime.now())}")
    print("-" * 50)

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scan_port, target, port) for port in range(1, 65535)]

        for future in concurrent.futures.as_completed(futures):
            pass

def main():
    parser = argparse.ArgumentParser(description="Python Port Scanner")
    parser.add_argument("target", help="The target hostname or IP address to scan")
    args = parser.parse_args()

    ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
    print(ascii_banner)

    target = socket.gethostbyname(args.target)
    scan_ports(target)

if __name__ == "__main__":
    main()
