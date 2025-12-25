from PIL import Image
import hashlib
import os


def hash_image_pixels(image_path):
    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")
        return None

    ext = os.path.splitext(image_path)[1].lower()

    # Convert mode based on image type
    if ext == ".png":
        img = Image.open(image_path).convert("RGBA")
    elif ext in [".jpg", ".jpeg"]:
        img = Image.open(image_path).convert("RGB")
    else:
        print(f"Unsupported image format: {ext}")
        return None

    # Compute SHA256 hash of pixels + size + mode
    h = hashlib.sha256()
    h.update(img.tobytes())
    h.update(str(img.size).encode())
    h.update(img.mode.encode())
    return h.hexdigest()


if __name__ == "__main__":
    # List of files to hash
    image_files = ["image.jpg", "image.jpeg", "image.png"]

    for image_path in image_files:
        hash_value = hash_image_pixels(image_path)
        if hash_value:
            print(f"{image_path} pixel hash:", hash_value)
