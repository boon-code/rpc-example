RPC Example
===========

This shall become a basic example for using a secure XML RPC connection.

Currently, it's just a basic connection without encryption and authentication.

Create Certificate (Old)
------------------------

1. Create a private key::

    openssl genrsa -des3 -out private-key.pem 4096

2. Create certificate::

    openssl req -new -x509 -key private-key.pem -out certitificate.ca

3. Combine private key and certificate in one file::

    cat private-key.pem certificate.ca > combi_key_cert.ca

Create Certificate (New)
------------------------

To create a new self-signed certificate, issue following commands::

  openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365

Status
------

* Connection is encrypted using ssl
* Verified that checking of hostname against certificate (client side) is disabled
* Client and server authentication via certificates works

To do
-----

* Clean up code
* Build simple modules to allow fast application development
