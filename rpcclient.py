import xmlrpc.client
import socket

def main ():
    try:
        c = xmlrpc.client.ServerProxy ("http://127.0.0.1:10000")
        c.printBla ("Hallo from Client!")
        c.printBla ("Bye from Client!")
    except socket.error as e:
        print ("Connection error : '%s'" % str (e))
    except xmlrpc.client.Fault as e:
        print ("rpc-client error : '%s'" % str (e))

if __name__ == '__main__':
    main ()
