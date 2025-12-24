import hashlib
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519


def sha256_hash(file_name):
    h = hashlib.sha256()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()


def signature(private_key_file, data_hash):
    with open(private_key_file, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    if isinstance(data_hash, str):
        data_hash = bytes.fromhex(data_hash)

    return private_key.sign(data_hash)
