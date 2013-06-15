from HTTPserver import Server, Response

entries = []

def html(msg):
    r = "<HTML>%s</HTML>" % msg.replace('\n', '<br>')
    print 'formating html to:', r
    return r

def get_get(route):
    print 'running get on ',repr(route)
    if route == '/entries':
        return html("Entries:\n"+"\n".join(entries))
    elif route in ['/', '']:
        print 'index'
        return html("Try /entries or /post")
    elif route == '/post':
        print 'returning post'
        return html(
            '<form action="entries" method="post">'
            'Your Entry: <input type="text" name="entry">'
            '<input type="submit" value="Submit">'
            '</form>')
    else:
        return 404

def get_post(route, request):
    print 'running post on ',repr(route)
    if route == '/entries':
        entries.append(request.body)
        r = Response(status_code=303)
        r.headers['Location'] = '/entries'
        r.headers['Method'] = 'GET'
        return r
    else:
        return 404

def get_head(route):
    r = Response.convenience(get_get(route))
    r.body = None
    return r


def main():
    Server({k[4:].upper(): v for k, v in globals().items() if k.startswith('get_')})

if __name__ == "__main__":
    main()
