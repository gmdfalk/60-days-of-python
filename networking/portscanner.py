from __future__ import print_function

# Threading seems to work better on Windows while multiprocessing is faster on
# Unix, because subprocesses are a lot less expensive here.
from multiprocessing import Pool
import socket
import sys


def host_to_ip(host):
    print("[+] Resolving", host)
    return socket.gethostbyname(host)


def scan(target):
    target_ip, port = target

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)

    try:
        sock.connect((target_ip, port))
        sock.close()

        return port, True
    except (socket.timeout, socket.error):
        return port, False

if __name__ == '__main__':
    if not len(sys.argv):
        print("Usage: scanner.py <target> <maxport>")
    if len(sys.argv) == 3:
        maxport = int(sys.argv[2])
    else:
        maxport = 1025

    target = sys.argv[1]

    # Resolve Host to IP, if necessary.
    if not target.replace(".", "").isdigit():
        target = host_to_ip(target)
    print("[+] Scanning", target)

    ports = range(1, maxport + 1)
    scanlist = [(target, port) for port in ports]

    # Use 512 workers. Not sure how insane that is but it seems to work fine.
    pool = Pool(512)

    for port, status in pool.imap_unordered(scan, scanlist):
        if status:
            print("[!]", port, "is open")
    print("[+] Finished scanning", target)
