import sys
import os
import socket
import pasxmlrpc
from optparse import OptionParser

def printBla (s):
    print ("BLA: '%s'" % s)
    return 0

def reply (s):
    return "Reply to '%s'" % s

def pathlist (dir):
    for i in os.listdir (dir):
        yield os.path.join (dir, i)

def server_main ():
    ca_files = list (pathlist ("./ca/ca_certs1/"))
    srv = pasxmlrpc.RPCServer ("", 10000, "./ca/cert5.pem",
                               "./ca/key5.pem", ca_files)
    srv.register_function (printBla)
    srv.register_function (reply)
    srv.serve_forever ()

def client_main (host=None):
    if host is None:
        host = '127.0.0.1'
    try:
        c = pasxmlrpc.RPCProxy (
            "https://%s:10000" % host,
            "./ca/cert2.pem",
            "./ca/key2.pem",
            "./ca/ca_certs2/cert5.pem"
        )
        print ("now call...")
        c.printBla ("Hallo from Client!")
        c.printBla ("Bye from Client!")
        print ("Response: %s" % c.reply ("Bla bla bla"))
    except socket.error as e:
        print ("Connection error : '%s'" % str (e))
    except pasxmlrpc.Fault as e:
        print ("rpc-client error : '%s'" % str (e))

def main (args):
    if len (args) <= 0:
        return -1
    if args[0] == 'server':
        return server_main ()
    elif args[0] == 'client':
        host = None
        if len (args) >= 2:
            host = args[1]
        return client_main (host)
    else:
        return -2

if __name__ == '__main__':
    sys.exit (main (sys.argv[1:]))
