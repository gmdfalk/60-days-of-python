import socket

from multiprocessing import Pool

def host_to_ip(host):
    print "[+] Resolving", host
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
    target = raw_input('Target Host/IP: ')
    if not target.replace(".", "").isdigit():
        target = host_to_ip(target)
    print "[+] Scanning", target

    ports = xrange(1, 1025)
    scanlist = [(target, port) for port in ports]

    # Use 512 workers. Not sure how insane that is but it seems to work fine.
    pool = Pool(512)

    for port, status in pool.imap_unordered(scan, scanlist):
        if status:
            print "[!]", port, "is open"
    print "[+] Finished scanning", target
