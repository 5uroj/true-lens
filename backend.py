from flask import Flask, request, jsonify, send_from_directory,send_file
from flask_cors import CORS
import os
from app import *

import json


app = Flask(__name__)
CORS(app)

MEDIA_FOLDER = "media"
os.makedirs(MEDIA_FOLDER, exist_ok=True)

ALLOWED_MEDIA_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webm"]

import json

def get_dict_from_file(filename: str) -> dict:
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def add_key_value_to_json(filename: str, key, value) -> None:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    data[key] = value

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



def allowed_media(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_MEDIA_EXTENSIONS


@app.route("/register", methods=["POST"])
def register_device():
    device_name = request.form.get("device_name")
    hardware_id = request.form.get("hardware_id")

    if not device_name or not hardware_id:
        return jsonify({"error": "device_name and hardware_id required"}), 400
    if hardware_id in get_dict_from_file('./registry.json').keys():
        return jsonify({"success": True}), 200
    if register_model(device_name):
        add_key_value_to_json("./registry.json", hardware_id, device_name)
        return jsonify({"success": True}), 200

@app.route("/uploadmedia", methods=["POST"])
def upload_media():
    if "media" not in request.files:
        return jsonify({"error": "media not given"}), 400

    media = request.files["media"]
    device_id = request.form.get("device-id")

    if media.filename == "":
        return jsonify({"error": "empty filename"}), 400

    if not allowed_media(media.filename):
        return jsonify({"error": "unsupported media type"}), 400

    if not device_id:
        return jsonify({"error": "device-id missing"}), 400

    original_path = os.path.join(MEDIA_FOLDER, media.filename)
    media.save(original_path)

    device_name = get_dict_from_file('./registry.json').get(device_id)
    if not device_name:
        return jsonify({"error": "Please register your camera"}), 404

    signed_filename = "signed_" + media.filename
    signed_path = os.path.join(MEDIA_FOLDER, signed_filename)
    
    sign_image(original_path, device_name, f'./keys/{device_name}.pem')

    try:
        return send_file(
            signed_path,
            as_attachment=True,
            download_name=signed_filename,
            mimetype='image/png'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/verifymedia", methods=["POST"])
def verify_media():
    if "media" not in request.files:
        return jsonify({"error": "media not given"}), 400

    media = request.files["media"]

    if media.filename == "":
        return jsonify({"error": "empty filename"}), 400

    if not allowed_media(media.filename):
        return jsonify({"error": "unsupported media type"}), 400

    path = os.path.join(MEDIA_FOLDER, media.filename)
    media.save(path)
    verify_hash,model = verify_image(path)
    if verify_hash and model:
        return jsonify({"success": True, "source_device": model, "hash": verify_hash}), 200
    else:
        return jsonify({"sucess":False})


@app.route("/media/<filename>")
def get_media(filename):
    return send_from_directory(MEDIA_FOLDER, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
