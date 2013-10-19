import xmlrpc.server

def printBla (s):
    print ("BLA: '%s'" % s)
    return 0

def main ():
    srv = xmlrpc.server.SimpleXMLRPCServer (("", 10000))
    srv.register_function (printBla)
    srv.serve_forever ()

if __name__ == '__main__':
    main ()
