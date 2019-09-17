# HTTPS

## Creating a Certificate

`pyluxa4` is mainly meant to be used on a local network, so these instructions are from that perspective. In many cases,
using a simple self signed certificate is more than sufficient.

To create a certificate, we will assume you have [OpenSSL][openssl] installed. If you are on Windows
using Git Bash, it will likely be available in your Bash terminal.

We will generate a x509v3 certificate. You can create a simple configuration template like the one shown below. Replace
The IP with the one from your machine. We will call this file `cert.conf`.

```ini
[ req ]
default_bits               = 4096
distinguished_name         = req_distinguished_name
[ req_distinguished_name ]
countryName                = Country Name (2 letter code)
stateOrProvinceName        = State or Province Name (full name)
localityName               = Locality Name (eg, city)
organizationName           = Organization Name (eg, company)
organizationalUnitName     = Organizational Unit Name (eg, section)
commonName                 = Common Name (e.g. server FQDN or YOUR name)
emailAddress               = Email Address
[ v3_req  ]
subjectAltName             = @alt_names
[alt_names]
DNS.1                      = localhost
IP.1                       = 127.0.0.1
IP.2                       = 192.168.1.2
```

Afterwards, run the following command. Then run the following command and enter the information that you'd like:

```
openssl req -x509 -out pyluxa4.cer -newkey rsa:4096 -nodes -keyout private.key -extensions v3_req -days 3650 -config cert.conf
```

You should now have a certificate `pyluxa4.cer` and a private key file `private.key`.

## Using HTTPS

When you start your server, simply feed in both `pyluxa4.cer` and `private.key` and optionally a token if desired:

```
pyluxa4 serve --ssl-cert pyluxa4.cer --ssl-key private.key --token secret
```

Now you can issue commands to your device using https.

```
pyluxa4 color red --secure pyluxa4.cer --token secret
```

Optionally you can send commands via the client without verifying the certificate:

```
pyluxa4 color red --secure 0 --token secret
```

--8<--
refs.txt
--8<--
