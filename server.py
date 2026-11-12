import os
import requests
from flask import Flask, request, jsonify, send_from_directory

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

app = Flask(__name__, static_folder="static")

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/send", methods=["POST"])
def send():
    photo = request.files.get("photo")
    if not photo:
        return jsonify(ok=False, error="no photo"), 400
    r = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
        data={"chat_id": CHAT_ID, "caption": "Фото"},
        files={"photo": (photo.filename or "photo.jpg", photo.stream, photo.mimetype)},
        timeout=30,
    )
    return jsonify(ok=r.ok), (200 if r.ok else 502)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)