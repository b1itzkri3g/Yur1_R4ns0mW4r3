from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Generate a new RSA private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Serialize and save the private key to a file
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)


# Extract the public key from the private key
public_key = private_key.public_key()

# Serialize and save the public key to a file
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)



# Hardcoded public key (replace with the actual public key)
with open("publickey.pem","rb") as f:
    hardcoded_public_key = f.read()

# Encrypt the private key with the hardcoded public key
encrypted_private_key = hardcoded_public_key.encrypt(
    private_pem,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Save the encrypted private key to a file
with open("encrypted_private_key.bin", "wb") as encrypted_key_file:
    encrypted_key_file.write(encrypted_private_key)
