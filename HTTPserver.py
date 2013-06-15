#!/usr/bin/env python
""" Toy server for playing with networking in python """

#David Lichtenberg
#dmlicht
#david.m.lichtenberg@gmail.com



import socket
import server_constants

class Response(object):
    http_ver = 'HTTP/0.9'
    default_bodies = {
        404 : "<html>File not found</html>",
        501 : "<html>That method's not implemented</html>"}

    @classmethod
    def convenience(cls, response):
        if isinstance(response, int):
            return cls(None, response)
        elif not isinstance(response, cls):
            r = cls(response, 200)
            return r
        else:
            return response

    def _get_body(self):
        if self._body is None and self.status_code in self.default_bodies:
            return self.default_bodies[self.status_code]
        else:
            return self._body
    def _set_body(self, body):
        self._body = body
    body = property(_get_body, _set_body)

    def __init__(self, body=None, status_code=200, **headers):
        self.status_code = status_code
        self.body = body
        self.headers = headers

    def __str__(self):
        return '{http_ver} {status_code!s} {status_code_text}\r\n{headers_plus_RN}\r\n{body_plus_2RN}'.format(
                    http_ver=self.http_ver,
                    status_code=self.status_code,
                    status_code_text=server_constants.REASON_PHRASES[self.status_code],
                    headers_plus_RN="%s\r\n" % ('\r\n'.join("%s: %s" % (k, v) for k, v in self.headers.items()) if self.headers else ""),
                    body_plus_2RN=("%s\r\n\r\n" % self.body) if self.body else "")

    def __repr__(self):
        return "<Response: %s>" % repr(str(self))

class Request(object):
    @classmethod
    def from_data(cls, msg):
        head, body = msg.split('\r\n\r\n', 1)
        if not body:
            body = None
        tokens = head.split()
        method, resource, version = tokens[:3]
        #TODO: fix header parsing, not up to spec
        headers = {key: value for key, value in
                    [line.split(': ', 1) for line in head.split('\r\n')[1:] if line.strip()]}
        r = cls(resource, method=method, body=body, version=version, **headers)
        return r
    def __init__(self, resource, method="GET", body=None, version="HTTP/1.1", **headers):
        self.method = method
        self.resource = resource
        self.version = version
        self.body = body
        self.headers = headers
    def __str__(self):
        return '{method} {resource} {version}\r\n{headers_plus_RN}\r\n{body_plus_2RN}'.format(
                method=self.method,
                resource=self.resource,
                version=self.version,
                headers_plus_RN="%s\r\n" % ('\r\n'.join("%s: %s" % (k, v) for k, v in self.headers.items()) if self.headers else ""),
                body_plus_2RN="%s\r\n\r\n" % (self.body if self.body else ""))
    def __repr__(self):
        return "<Request: %r>" % self.orig_msg

class Server(object):
    def __init__(self, handlers):
        self.handlers = handlers
        self.run()

    def handle_msg(self, msg):
        """returns a Response object for given request"""
        request = Request.from_data(msg)
        if request.method in self.handlers:
            handler = self.handlers[request.method]
            if handler.func_code.co_argcount == 1:
                response = Response.convenience(handler(request.resource))
            elif handler.func_code.co_argcount == 2:
                response = Response.convenience(handler(request.resource, request))
        elif request.method in server_constants.METHODS:
            response = Response(status_code=501) #Is okay request but not implemented
        else:
            response = Response(status_code=400) #Not a supported method return response
        return response

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
            if not msg:
                continue

            #TODO: spin off new thread
            response = self.handle_msg(msg)

            try:
                #client_socket.send(msg)
                client_socket.send(str(response))
            except socket.error, e:
                print "error sending out file: ", e
            clients_served += 1
            print 'clients served:', clients_served
            client_socket.close()
