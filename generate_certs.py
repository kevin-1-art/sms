#!/usr/bin/env python
"""Generate self-signed SSL certificate for HTTPS testing"""

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta
import os

# Create certs directory if it doesn't exist
os.makedirs('certs', exist_ok=True)

print("🔐 Generating Self-Signed SSL Certificate...")

# Generate private key
print("  → Generating private key...")
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Generate certificate
print("  → Generating certificate...")
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"State"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"City"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"School Management"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
])

cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    private_key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.utcnow()
).not_valid_after(
    datetime.utcnow() + timedelta(days=365)
).add_extension(
    x509.SubjectAlternativeName([
        x509.DNSName(u"localhost"),
        x509.DNSName(u"127.0.0.1"),
    ]),
    critical=False,
).sign(private_key, hashes.SHA256(), default_backend())

# Write certificate to file
print("  → Saving certificate to certs/cert.pem...")
with open("certs/cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

# Write private key to file
print("  → Saving private key to certs/key.pem...")
with open("certs/key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

print("\n✅ SSL Certificate Generated Successfully!")
print("   📁 Certificate: certs/cert.pem")
print("   📁 Private Key: certs/key.pem")
print("   ⏰ Valid for: 365 days")
print("\n🔒 Your certificates are ready for HTTPS!")
