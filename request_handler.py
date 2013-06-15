#!/usr/bin/env python

import HTTPserver
from HTTPserver import Response

def main():
    handlers = {
        "GET": get_get,
        "HEAD": get_head,
        "OPTIONS": get_options
    }
    HTTPserver.Server(handlers)

def parse_route(route):
    """take in web route and returns appropriate route to resource"""
    if route == '/':
        route = '/index.html'
    while '../' in route:
        route = route.replace('../', '')
    return '.' + route


def get_get(route):
    """handles get request - returns appropriate data and response code"""
    resource_path = parse_route(route)
    try:
        f = open(resource_path)
        response_body = f.read()
    except Exception as e:
        print e
        return 404
    return Response(response_body, 200)


def get_head(route):
    """returns response code"""
    resource_path = parse_route(route)
    try:
        open(resource_path)
    except IOError:
        return 404
    return Response(resource_path, 200)


def get_options():
    pass


if __name__ == '__main__':
    main()
