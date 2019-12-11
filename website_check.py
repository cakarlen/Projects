#!/usr/bin/env python
import subprocess
import nmap
import sys
import socket
import os
from urllib import request
from datetime import datetime


# SocketScan class
class SocketScan:
    def __init__(self, socket_server, socket_port):
        self.socket_server = socket_server
        self.socket_port = socket_port

    # Function: socket scanner
    def scanner(self):

        print("\nRunning initial scanning...")

        # Take ports input, delete '-', take remaining to two different variables
        self.socket_port = self.socket_port.replace("-", " ")
        min_port, max_port = self.socket_port.split(' ', 1)
        if min_port == max_port:
            min_port = max_port

        # Get IP address from hostname
        remote_ip = socket.gethostbyname(self.socket_server)

        # Using the range function to specify ports (here it will scans all ports between 1 and 65535)
        try:
            for scan_port in range(int(min_port), int(max_port)):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((remote_ip, scan_port))
                if result == 0:
                    with open('socket_{}'.format(self.socket_server), 'w') as file:
                        file.write(("Port {}: 	 Open".format(scan_port)))
                    ports_open = [scan_port]
                    # Convert list to string
                    ports_open = str(ports_open)
                sock.close()

        # Error handling
        except KeyboardInterrupt:
            print("You pressed Ctrl+C")
            sys.exit()

        except socket.gaierror:
            print('Hostname could not be resolved. Exiting')
            sys.exit()

        except socket.error:
            print("Couldn't connect to server")
            sys.exit()

        # Printing the information to screen
        print("Initial scan has completed!")


# NMap class
class NMapScan:
    def __init__(self, server, port):
        self.server = server
        self.port = port

    # Function: NMap scanner
    def scanner(self):
        # Initialize variables
        self.server = remote_server
        self.port = ports

        # Print "scan is running"
        print("\nRunning NMap scan on desired host and ports...".format(self.server, self.port))

        # Retrieve IP from hostname
        remote_ip = socket.gethostbyname(self.server)
        # Initialize nmap
        query = nmap.PortScanner()
        # Scan remote_ip with ports_open based on first port scan
        query.scan(remote_ip, self.port)

        # Print result to .csv format
        with open('nmap_{}.csv'.format(self.server), 'w') as file:
            file.write(query.csv())

        # Print 'scan is complete'
        print("NMap scan has completed!\n")

    # Function: Get HTML headers
    def retrieve_headers(self):
        # Initialize variables
        self.server = remote_server

        # Print 'scan is starting'
        print("Retrieving HTML header information...")

        try:
            # Retrieve header information
            with request.urlopen("http://%s" % self.server) as url:
                # HTML response code check
                '''
                if f.getcode() == 200:
                    print("URL ok")
                elif f.getcode() == 404:
                    print("URL was not found!\nPlease re-enter URL")
                '''
                # Print header info
                with open('headers_{}.txt'.format(self.server), 'w') as file:
                    file.write(str(url.info()))
        except request.URLError:
            print("Connection refused! Please re-enter your URL!")
            sys.exit()

        # Headers retrieved
        print("Headers retrieved!\n")

        # Print 'scan is complete'
        print("Fingerprint scan has completed!")


if __name__ == "__main__":
    # Check if root/admin
    # if os.getuid() is not 0:
    #     print("Must run as root/administrator!")
    #     sys.exit()

    # Clear shell window
    subprocess.call('clear', shell=True)

    # Input for server and ports
    remote_server = input("Enter remote host (URL/IP address): ")
    ports = input("Enter port range (Ex: 21-445): ")

    # Start SocketScan class
    # socket_scan = SocketScan(remote_server, ports)
    # socket_scan.scanner()

    # Start NMapScan class
    nmap_scan = NMapScan(remote_server, ports)
    nmap_scan.scanner()
    nmap_scan.retrieve_headers()
