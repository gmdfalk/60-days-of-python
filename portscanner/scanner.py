#!/usr/bin/env python2

import socket
import subprocess
import sys
from datetime import datetime

# Clears the terminal screen.
subprocess.call("clear", shell=True)

server = sys.argv[1]
serverip = socket.gethostbyname(server)
print "-"*60
print "Scanning {} ({}), please wait.".format(serverip, server)
print "-"*60

before = datetime.now()

try:
    for port in range(1, 136):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((serverip, port))
        print result
        if not result:
            print "Port open:", port
        sock.close()
except socket.gaierror:
    print "Hostname could not be resolved. Exiting."
    sys.exit()
except socket.error:
    print "Could not connect to server."
    sys.exit()

after = datetime.now()
duration = after - before

print "Scanning completed in:", duration
