#!/usr/bin/env python

#David Lichtenberg
#dmlicht
#david.m.lichtenberg@gmail.com

#
# toy client for playing with networking in python
#
# To run - pass server IP and Port as arguments. 
# Client will establish connection with corresponding server and say hello
#

import socket
from sys import argv

http_get_msg = "GET /index.html HTTP/1.1"

#check if correct number of args supplied
if len(argv) != 4:
    print 'incorrect input'
    print 'Usage: ./client server_ip server_port_num "message"'
    exit(0)

#pull out arguments
server_ip = argv[1]
server_port = int(argv[2])
message = argv[3]

#create client socket
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, e:
    print 'error while creating socket:', e
    exit(1)

#connect to server
try:
    sock.connect((server_ip, server_port))
except socket.gaierror, e:
    print 'address lookup error: ', e
    exit(1)
except socket.error, e:
    print "connection error: ", e
    exit(1)

#send message to server
try:
    sock.sendall(message)
except socket.error, e:
    print "error sending message: ", e
    exit(1)

#shutdown server to ensure send has happened correctly
try:    
    sock.shutdown(1)
except socket.error, e:
    print "error during shutdown: ", e

#recieve message
print sock.recv(2048)

#close socket
try:
    sock.close()
except socket.error, e:
    print "error while closing socket: ", e