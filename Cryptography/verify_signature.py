import os
from cryptography.hazmat.primitives.asymmetric import ed25519


def verify_image_signature(public_key_hex, signature_hex, hash_hex):
    try:
        # Ensure inputs are strings and remove '0x' prefix
        def clean_hex(h):
            if isinstance(h, int):
                h = hex(h)
            return h.replace("0x", "")

        pub_bytes = bytes.fromhex(clean_hex(public_key_hex))
        sig_bytes = bytes.fromhex(clean_hex(signature_hex))
        hash_bytes = bytes.fromhex(clean_hex(hash_hex))

        # Load the public key object from the 32-byte raw public key
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(pub_bytes)

        # Ed25519 verification
        public_key.verify(sig_bytes, hash_bytes)
        return True

    except Exception as e:
        print(f"Verification error: {e}")
        return False


if __name__ == "__main__":

    public_key_hex = "ab51779e0368a354daf8a13c88324f2c168941a7bc6826b40a2cb846a7f2652d"

    input_signature = "fedc30a6aa26c4014ec8ee706db96c60f6acd4234235a4c0b1c343352872c2d2de5d1782ee4dcdc029d697fe5f3e671dcc9b0a2977630dbe6125b2e07e049305"

    input_hash = "90042363b79f14861ee6f83eb7989ff34fb0d65a2ba6baf8c8a9d8d7c136b996"

    # Process verification
    result = verify_image_signature(public_key_hex, input_signature, input_hash)

    if result:
        print("Signature is valid.")
    else:
        print("Signature is invalid.")
