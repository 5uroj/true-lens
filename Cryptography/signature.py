import os
import hashlib
from PIL import Image
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

def compute_pixel_hash(image_path):
    """
    Extracts raw pixel data and returns a SHA256 binary digest.
    This ensures we sign the 'essence' of the image, ignoring metadata.
    """
    img = Image.open(image_path)
    ext = os.path.splitext(image_path)[1].lower()

    # Standardize color layers based on file type
    if ext == ".png":
        img = img.convert("RGBA")
    elif ext in [".jpg", ".jpeg"]:
        img = img.convert("RGB")
    else:
        raise ValueError(f"Format {ext} not supported.")

    # Build the hash using pixels, dimensions, and mode
    hasher = hashlib.sha256()
    hasher.update(img.tobytes())
    hasher.update(str(img.size).encode())
    hasher.update(img.mode.encode())
    
    return hasher.digest()  # Returns the 32-byte hash

def sign_image_hash(private_key_path, image_path):
    """Signs the pre-computed hash of an image using Ed25519."""
    if not os.path.exists(image_path):
        print(f"File missing: {image_path}")
        return None

    # 1. Generate the hash first
    try:
        digest = compute_pixel_hash(image_path)
    except Exception as e:
        print(f"Error hashing {image_path}: {e}")
        return None

    # 2. Load the private key from the PEM file
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(), 
            password=None
        )
    
    # 3. Sign the hash (the digest), not the raw image file
    signature = private_key.sign(digest)
    
    return signature.hex()

if __name__ == "__main__":
    # Settings
    PRIVATE_KEY_FILE = "iphone-13.pem"
    target_images = ["image.jpg", "image.jpeg", "image.png"]

    print("--- Generating Signatures for Image Hashes ---")
    for file_name in target_images:
        if os.path.exists(file_name):
            sig_hex = sign_image_hash(PRIVATE_KEY_FILE, file_name)
            print(f"Target: {file_name}")
            print(f"Hash Signature: {sig_hex}\n")
        else:
            print(f"File {file_name} not found, skipping...")