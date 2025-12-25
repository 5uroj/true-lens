import os
import json
import shutil
from PIL import Image, PngImagePlugin
import piexif


def add_metadata_jpg(image_path, user_content, output_path=None):
    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")
        return

    if output_path is None:
        output_path = image_path
    else:
        # Copy original image to output path before editing metadata
        shutil.copyfile(image_path, output_path)

    exif_dict = piexif.load(output_path)
    exif_dict["Exif"][piexif.ExifIFD.UserComment] = json.dumps(user_content).encode()
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, output_path)
    print(f"UserComment added losslessly to: {output_path}")

# ------------------ PNG metadata ------------------ #
def add_metadata_png(image_path, user_content, output_path=None):
    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")
        return

    if output_path is None:
        output_path = image_path

    img = Image.open(image_path)
    meta = PngImagePlugin.PngInfo()
    meta.add_text("Comment", json.dumps(user_content))
    img.save(output_path, pnginfo=meta)
    print(f"UserComment added to PNG: {output_path}")

# ------------------ JPEG lossless metadata ------------------ #
def add_metadata_jpeg(input_path, user_content, output_path):
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        return

    try:
        exif_dict = piexif.load(input_path)
    except Exception:
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "Interop": {}, "thumbnail": None}

    exif_dict['Exif'][piexif.ExifIFD.UserComment] = json.dumps(user_content).encode('utf-8')
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, input_path, output_path)
    print(f"UserComment added losslessly to: {output_path}")

# ------------------ Main ------------------ #
if __name__ == "__main__":
    # JPG
    add_usercomment_lossless("image.jpg", {"verification": "true"}, "image_with_comment.jpg")
    # PNG
    add_usercomment_png("image.png", {"verification": "true"}, "image_with_comment.png")
    # JPEG
    add_usercomment_jpeg_lossless("image.jpeg", {"verification": "true"}, "image_with_comment.jpeg")

    print("UserComments added losslessly. Pixels unchanged.")
