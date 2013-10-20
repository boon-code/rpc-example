import sys
import socket
import ssl

def server_app ():
    sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    ctx = ssl.SSLContext (ssl.PROTOCOL_SSLv23)
    ctx.load_verify_locations (capath="./ca/ca_certs1")
    ctx.verify_mode = ssl.CERT_REQUIRED
    ctx.load_cert_chain("./ca/cert1.pem", "./ca/key1.pem")

    sock = ctx.wrap_socket (sock, server_side=True)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind (("", 12347))
    sock.listen (1)

    while (1):
        try:
            con, addr = sock.accept ()
            break
        except ssl.SSLError:
            pass
    try:
        msg = con.recv ()
        print (msg)
    except KeyboardInterrupt:
        pass

def client_app ():
    sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    sock = ssl.wrap_socket (sock, server_side=False,
                            certfile="./ca/cert3.pem",
                            keyfile="./ca/key3.pem",
                            cert_reqs=ssl.CERT_REQUIRED,
                            ca_certs="./ca/cert1.pem",
                            ssl_version=ssl.PROTOCOL_SSLv23)
    sock.connect (("", 12347))
    sock.send (b"Bla bla bla")

def main (args):
    if (len (args) == 1):
        if args [0] in ('s', 'server'):
            server_app ()
        elif args [0] in ('c', 'client'):
            client_app ()
        else:
            print ("error")

if __name__ == '__main__':
    main (sys.argv [1:])
