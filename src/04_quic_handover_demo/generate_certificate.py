"""
generate_certificate.py

Purpose
-------
QUIC requires TLS encryption for every connection, even for a purely
local experiment. This script creates a self-signed certificate
(cert.pem) and its matching private key (key.pem) so the QUIC hospital
server has something to present during the TLS handshake.

Run this ONCE, from inside this folder, before running
hospital_server_quic.py for the first time:

    py generate_certificate.py

It creates cert.pem and key.pem in the current folder. The QUIC client
in this project is configured to accept self-signed certificates
(config.verify_mode = ssl.CERT_NONE), which is fine for a local
prototype but would NOT be appropriate for a real production deployment.
"""
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import datetime

# Generate a private key for the certificate.
key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# Build a minimal self-signed certificate for "localhost".
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
])

cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.utcnow())
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
    .sign(key, hashes.SHA256())
)

# Save the private key to key.pem.
with open("key.pem", "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ))

# Save the certificate to cert.pem.
with open("cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("Done! Created cert.pem and key.pem in this folder.")
