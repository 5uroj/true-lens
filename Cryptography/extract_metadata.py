import os
import json
from PIL import Image
import piexif


def extract_metadata(image_path):
    if not os.path.exists(image_path):
        return {"error": f"File not found: {image_path}"}

    ext = os.path.splitext(image_path)[1].lower()

    try:
        if ext in (".jpg", ".jpeg"):
            exif_data = piexif.load(image_path)
            raw_comment = exif_data.get("Exif", {}).get(piexif.ExifIFD.UserComment)

            if raw_comment:
                text = raw_comment.decode("utf-8", errors="ignore")
                if "{" in text and "}" in text:
                    text = text[text.find("{") : text.rfind("}") + 1]
                return json.loads(text)

        if ext == ".png":
            img = Image.open(image_path)
            text = img.info.get("Comment")
            if text:
                return json.loads(text)

        return {"status": "No metadata found"}

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    test_files = [
        "image_with_comment.jpg",
        "image_with_comment.jpeg",
        "image_with_comment.png",
    ]

    for path in test_files:
        if os.path.exists(path):
            result = extract_metadata(path)
            print(f"{path} → {result} ({type(result)})")
        else:
            print(f"{path} → file not found")
