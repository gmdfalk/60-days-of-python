import socket

from multiprocessing import Pool

def dns_to_ip(dns):
    if dns.replace(".", "").isdigit():
        return dns
    print "Resolving", dns
    return socket.gethostbyname(dns)


def scan(target_port):
    target_ip, port = target_port

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)

    try:
        sock.connect((target_ip, port))
        sock.close()

        return port, True
    except (socket.timeout, socket.error):
        return port, False

if __name__ == '__main__':
    target = raw_input('Target IP: ')
    target_ip = dns_to_ip(target)
    print "Scanning", target_ip

    ports = xrange(1, 1025)
    scanlist = [(target_ip, port) for port in ports]

    # Use 512 workers. Not sure how insane that is but it seems to work fine.
    pool = Pool(512)

    for port, status in pool.imap_unordered(scan, scanlist):
        if status:
            print port, "is open"
    print "Finished scanning", target_ip
