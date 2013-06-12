#!/usr/bin/env python

import server

def main():
    handlers = {
        "GET": get_get,
        "HEAD": get_head,
        "OPTIONS": get_options
    }
    server.HTTPServer(handlers)

def get_get(resource):
    """handles get request - returns appropriate data and response code"""
    response_status_code = 200
    response_body = ""
    resource = '.' + resource
    if resource == './':
        resource = './index.html'
    try:
        f = open(resource)
        response_body = f.read()
    except Exception as e:
        print e
        response_status_code = 404
    return response_status_code, response_body


def get_head(resource):
    pass

def get_options():
    pass


if __name__ == '__main__':
    main()