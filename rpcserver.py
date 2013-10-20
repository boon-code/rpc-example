import xmlrpc.server
import socket
import ssl
import os

class SecureRpcServer (xmlrpc.server.SimpleXMLRPCServer):

    def __init__ (self, address, port, certfile, keyfile, ca_files):
        xmlrpc.server.SimpleXMLRPCServer.__init__ (self,
                                                   (address, port))
        self.__ctx = ssl.SSLContext (ssl.PROTOCOL_SSLv23)
        for ca_f in ca_files:
            self.__ctx.load_verify_locations (cafile=ca_f)
        self.__ctx.verify_mode = ssl.CERT_REQUIRED
        self.__ctx.load_cert_chain(certfile, keyfile)

        self.socket = self.__ctx.wrap_socket (self.socket,
                                              server_side=True)

def printBla (s):
    print ("BLA: '%s'" % s)
    return 0

def pathlist (dir):
    for i in os.listdir (dir):
        yield os.path.join (dir, i)

def main ():
    ca_files = list (pathlist ("./ca/ca_certs1/"))
    srv = SecureRpcServer ("", 10000, "./ca/cert5.pem",
                           "./ca/key5.pem", ca_files)
    srv.register_function (printBla)
    srv.serve_forever ()

if __name__ == '__main__':
    main ()
