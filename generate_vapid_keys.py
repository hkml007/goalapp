from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import base64

# Generate private key
private_key = ec.generate_private_key(ec.SECP256R1())
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Get public key
public_key = private_key.public_key()
public_numbers = public_key.public_numbers()
x = public_numbers.x.to_bytes(32, 'big')
y = public_numbers.y.to_bytes(32, 'big')
public_key_bytes = b'\x04' + x + y
public_key_b64 = base64.urlsafe_b64encode(public_key_bytes).rstrip(b'=').decode('utf-8')

# Get private key
private_numbers = private_key.private_numbers()
private_key_bytes = private_numbers.private_value.to_bytes(32, 'big')
private_key_b64 = base64.urlsafe_b64encode(private_key_bytes).rstrip(b'=').decode('utf-8')

print("PUBLIC_KEY =", public_key_b64)
print("PRIVATE_KEY =", private_key_b64)
