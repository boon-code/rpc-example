import xmlrpc.client
import http.client
import ssl
import socket

class MyHTTPS (http.client.HTTPSConnection):

    def getresponse (self, *args, **kargs):
        print ("Arguments: ", *args, **kargs)
        ret = super (MyHTTPS, self).getresponse (*args, **kargs)
        print ("Returns: ", dir (ret))
        print (ret.headers)
        print (ret.reason)
        print (dir(self))
        print (self.sock)
        return ret

    def request (self, *args, **kargs):
        print ("Request...")
        ret = super (MyHTTPS, self).request (*args, **kargs)
        print ("Socket:", self.sock)
        return ret

    def connect (self):
        ret = super (MyHTTPS, self).connect ()
        print ("connect: ", ret)
        print ("sock: ", self.sock)
        print ("sock-certf:", self.sock.getpeercert ())
        return ret


class MyTransport(xmlrpc.client.Transport):
    """Handles an HTTPS transaction with digest authentication."""

    def make_connection (self, host):
        if self._connection and host == self._connection[0]:
            return self._connection[1]

        if not hasattr(http.client, "HTTPSConnection"):
            raise NotImplementedError(
            "your version of http.client doesn't support HTTPS")
        # create a HTTPS connection object from a host descriptor
        # host may be a string, or a (host, x509-dict) tuple
        chost, self._extra_headers, x509 = self.get_host_info(host)
        print ("X509: %s" % str (x509))
        print ("Chost", chost)
        print (str (self._extra_headers))
        context = ssl.SSLContext (ssl.PROTOCOL_SSLv23)
        context.load_verify_locations (cafile="./ca/ca_certs2/cert5.pem")
        context.verify_mode = ssl.CERT_REQUIRED
        self._connection = host, http.client.HTTPSConnection (chost,
            cert_file="./ca/cert2.pem",
            key_file="./ca/key2.pem",
            context=context,
            check_hostname=False)
        print (str (dir (self._connection[1])))
        return self._connection[1]

def main ():
    try:
        transport = MyTransport ()
        c = xmlrpc.client.ServerProxy ("https://127.0.0.1:10000",
                                       transport)
        print ("now call...")
        c.printBla ("Hallo from Client!")
        c.printBla ("Bye from Client!")
    except socket.error as e:
        print ("Connection error : '%s'" % str (e))
    except xmlrpc.client.Fault as e:
        print ("rpc-client error : '%s'" % str (e))

if __name__ == '__main__':
    main ()
