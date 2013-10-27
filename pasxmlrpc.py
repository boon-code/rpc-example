"""
Privacy Authentication over Secure Socket Layer XML RPC package
===============================================================

This module contains an xml Server and Server proxy. Both use
SSL for encrypted communication and certificates to authenticate.
"""

import ssl
from xmlrpc.server import SimpleXMLRPCServer
from http.client import HTTPSConnection
from xmlrpc.client import ServerProxy, Transport, Fault


class RPCServer (SimpleXMLRPCServer):
    """RPC Server that uses SSL for privacy and authentication"""

    def __init__ (self, address, port, certfile, keyfile, ca_files):
        """
        :param address:  Address of the server to listen on.
        :param port:     Port number to listen on.
        :param certfile: Certificate of the server.
        :param keyfile:  Private key file (matching the certificate).
        :param ca_files: List of client certificates that will be
                         accepted by this server.
        """
        SimpleXMLRPCServer.__init__ (self, (address, port))
        self.__ctx = ssl.SSLContext (ssl.PROTOCOL_SSLv23)
        for ca_f in ca_files:
            self.__ctx.load_verify_locations (cafile=ca_f)
        self.__ctx.verify_mode = ssl.CERT_REQUIRED
        self.__ctx.load_cert_chain (certfile, keyfile)
        self.socket = self.__ctx.wrap_socket (self.socket,
                                              server_side=True)

class CATransport (Transport):
    """Transport class for client authentication via certificate."""

    def __init__ (self, certfile, keyfile, server_certfile):
        """
        :param certfile:        Certificate which will be used to
                                authenticate on the server-side.
        :param keyfile:         Private key of the certificate (Used
                                to sign the certificate?).
        :param server_certfile: Server-side certificate of the server to
                                trust.
        """
        self._cafile = certfile
        self._keyfile = keyfile
        self._server_cafile = server_certfile

    def make_connection (self, host):
        if self._connection and host == self._connection[0]:
            return self._connection[1]
        chost, self._extra_headers, x509 = self.get_host_info (host)
        #
        print ("X509: %s" % str (x509))
        print ("Chost", chost)
        print (str (self._extra_headers))
        #
        context = ssl.SSLContext (ssl.PROTOCOL_SSLv23)
        context.load_verify_locations (cafile=self._server_cafile)
        context.verify_mode = ssl.CERT_REQUIRED
        con = HTTPSConnection (chost, cert_file=self._cafile,
                               key_file=self._keyfile, context=context,
                               check_hostname=False)
        self._connection = host, con
        #
        print (str (dir (self._connection[1])))
        #
        return con

class RPCProxy (ServerProxy):
    """RPC Proxy Server to connect to an RPC Server."""

    def __init__ (self, url, certfile, keyfile, server_certfile):
        """
        :param url:             Server URL to connect to (including
                                port address).
        :param certfile:        Certificate which will be used to
                                authenticate on the server-side.
        :param keyfile:         Private key of the certificate (Used
                                to sign the certificate?).
        :param server_certfile: Server-side certificate of the server to
                                trust.
        """
        transport = CATransport (certfile, keyfile, server_certfile)
        xmlrpc.client.ServerProxy.__init__ (self, url, transport)
