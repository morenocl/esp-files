from machine import Pin
import ujson
import usocket as socket


OK = b"""\
HTTP/1.0 200 OK

"""

CONTENT = b"""\
Hello #%d from MicroPython!
"""

STATUS_LED = b"""\
Status led: #%d
"""

NOT_METHOD = b"""\
Method not valid. Use GET and POST
"""

NO_PATH = b"""\
Path not valid. Use a valid path.
"""

def parse_header(header):
    d = {}
    header = header.split('\r\n')
    for line in header:
        if ':' in line:
            key, value = line.split(':',1)
            d[key] = value
    return d

def get_request(client_stream):
    req = client_stream.recv(1024)
    req = req.decode('ascii')
    return req

def get(path, header):
    if path == '/':
        return OK + CONTENT
    elif path == '/led':
        led = Pin(2, Pin.OUT)
        return OK + STATUS_LED % led.value()
    else:
        return OK + NO_PATH

def post(path, header, client_stream):
    if header['Content-Length'] and int(header['Content-Length']):
        body = ujson.loads(client_stream.recv(1024))
        print(body)
    return OK + CONTENT

def main(micropython_optimize=False):
    s = socket.socket()

    ai = socket.getaddrinfo("0.0.0.0", 8080)
    print("Bind address info:", ai)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8080/")

    while True:
        client_stream, client_addr = s.accept()
        print("Client address:", client_addr)
        print("Client socket:", client_stream)

        print("Request:")
        # get the firsth line and header of the request
        request = get_request(client_stream)
        initial_line, header = request.split('\r\n', 1)
        method, path, http_version = initial_line.split(' ')
        print(method, path, http_version)

        header = parse_header(header)
        print(header)
        # Select the method to exec
        if method == 'GET':
            print('Used GET method')
            msj = get(path, header)
        elif method == 'POST':
            print('Used POST method')
            msj = post(path, header, client_stream)
        else:
            print('Used another method: %s' % method)
            msj = OK + NOT_METHOD

        # Send the response and close the socket.
        client_stream.write(msj)
        client_stream.close()


main()