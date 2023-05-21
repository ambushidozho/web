
def app(environ, start_response):
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']
    get_params = environ['QUERY_STRING']
    post_params = environ['wsgi.input'].read().decode()
    print(f"Method: {method}")
    print(f"Path: {path}")
    print(f"GET params: {get_params}")
    print(f"POST params: {post_params}")
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, headers)
    return [b"Success!"]