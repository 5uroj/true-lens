import os
import json
from Cryptography.hash import hash_image_pixels
from Cryptography.signature import sign_image_hash
from Cryptography.add_metadata import add_metadata_jpg, add_metadata_png, add_metadata_jpeg
from Cryptography.extract_metadata import extract_metadata 
from Cryptography.verify_signature import verify_image_signature 
from Cryptography.generate_key import generate_key, public_key
from BlockChain.get_key import get_model_public_key
from BlockChain.add_device import add_model_to_blockchain

def register_model(model_number):
    if not os.path.exists("keys"):
        os.makedirs("keys")

    private_path = f"keys/{model_number}.pem"
    public_path = f"keys/{model_number}_public.pem"
    
    generate_key(private_path)
    public_key(private_path)
    
    if add_model_to_blockchain(public_path):
        return True


def sign_image(image_path, model_number, private_key_path):
    if not os.path.exists(image_path):
        return "Error: File not found"

    pixel_hash = hash_image_pixels(image_path)
    if not pixel_hash:
        return "Error: Hashing failed"

    signature = sign_image_hash(private_key_path, image_path)
    if not signature:
        return "Error: Signing failed"

    metadata_payload = {
        "model": model_number,
        "hash": pixel_hash,
        "signature": signature
    }

    ext = os.path.splitext(image_path)[1].lower()
    image_dir = os.path.dirname(image_path)
    image_name = os.path.basename(image_path)
    output_name = os.path.join(image_dir, f"signed_{image_name}")

    if ext == ".png":
        add_metadata_png(image_path, metadata_payload, output_name)
    elif ext in [".jpg", ".jpeg"]:
        add_metadata_jpg(image_path, metadata_payload, output_name)
    else:
        return f"Error: Unsupported format: {ext}"

    return True

def verify_image(image_path):
    if not os.path.exists(image_path):
        return "Error: File not found"

    data = extract_metadata(image_path)
    if not data or "error" in data:
        return f"Error: Could not extract metadata: {data.get('error')}"

    model_number = data.get("model")
    extracted_hash = data.get("hash")
    extracted_sig = data.get("signature")

    live_hash = hash_image_pixels(image_path)
    
    if live_hash != extracted_hash:
        return "Failure: Image content has been modified"

    public_key_hex = get_model_public_key(model_number)
    
    if not public_key_hex:
        return f"Error: No public key found for model {model_number}"


    is_valid = verify_image_signature(public_key_hex, extracted_sig, extracted_hash)
    if is_valid:
        return extracted_hash,model_number
    else:
        return False,False


if __name__ == "__main__":
    
    # result = sign_image("image.png", "Canon-X1000_public", "keys/Canon-X1000.pem")
    result = verify_image("signed_image.png")
    print(result)