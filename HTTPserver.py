#!/usr/bin/env python
""" Toy server for playing with networking in python """

#David Lichtenberg
#dmlicht
#david.m.lichtenberg@gmail.com



import socket
import server_constants

class ResponseHeader(object):
    def __init__(self, http_ver, status_code):
        self.http_ver = http_ver
        self.status_code = status_code
    def __str__(self):
        return self.http_ver + ' ' + str(self.status_code) + ' ' + server_constants.REASON_PHRASES[self.status_code]
    def __repr__(self):
        return "<ResponseHeader: %s>" % self

class Request(object):
    def __init__(self, msg):
        self.orig_msg = msg
        tokens = msg.split()
        self.method, self.resource, self.version = tokens[:3]

        #TODO: fix header parsing, not up to spec
        self.headers = {}
        for key, value in [line.split(': ', 1) for line in msg.split('\r\n')[1:] if line.strip()]:
            self.headers[key] = value
    def __str__(self):
        return self.orig_msg
    def __repr__(self):
        return "<Request: %r>" % self.orig_msg

class Server(object):
    def __init__(self, handlers):
        self.handlers = handlers
        self.run()

    def handle_msg(self, msg):
        """returns header and body (if applicable) for given request"""
        http_msg = Request(msg)
        response_body = ""
        if http_msg.method in self.handlers:
            status_code, response_body = self.handlers[http_msg.method](http_msg.resource)
        elif http_msg.method in server_constants.METHODS:
            status_code = 501 #Is okay request but not implemented
        else:
            status_code = 400 #Not a supported method
        response_header = ResponseHeader(http_msg.version, status_code)
        return str(response_header), str(response_body)

    def run(self):
        host = '' #accept requests from all interfaces

        port = 9000 #use port 80 as binding port

        #Initialize IPv4 (AF_INET) socket using TCP (SOCK_STREAM)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #set port to be reusable - this allows port to be freed when socket is closed
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        clients_served = 0

        try:
            sock.bind((host, port))
        except socket.error, msg:
            print 'bind error, code: ', msg
            exit(0)

        #begin listening allowing for one connection at a time

        try:
            sock.listen(1)
        except socket.error:
            exit(0)

        while 1:
            client_socket, client_addr = sock.accept()
            msg = client_socket.recv(2048)

            #TODO: spin off new thread
            outgoing_header, outgoing_body = self.handle_msg(msg)

            try:
                #client_socket.send(msg)
                client_socket.send(outgoing_body)
            except socket.error, e:
                print "error sending out file: ", e
            clients_served += 1
            print 'clients served:', clients_served
            client_socket.close()
