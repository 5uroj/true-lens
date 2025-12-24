from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization


def generate_key(file_name):
    private_key = ed25519.Ed25519PrivateKey.generate()
    with open(file_name, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )


def public_key(private_key_file):
    with open(private_key_file, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    pub_key = private_key.public_key()

    output_file = private_key_file.replace(".pem", "_public.pem")

    with open(output_file, "wb") as f:
        f.write(
            pub_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )
