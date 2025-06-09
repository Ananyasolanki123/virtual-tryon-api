from flask import Flask, request, jsonify
import requests
from PIL import Image
from io import BytesIO
import os
import uuid

app = Flask(__name__)

@app.route('/')
def home():
    return "Virtual Try-On API is running!"

@app.route('/tryon', methods=['POST'])
def tryon():
    data = request.json
    user_img_url = data['user_image_url']
    dress_img_url = data['dress_image_url']

    try:
        user_response = requests.get(user_img_url)
        dress_response = requests.get(dress_img_url)

        user_img = Image.open(BytesIO(user_response.content)).convert("RGBA")
        dress_img = Image.open(BytesIO(dress_response.content)).convert("RGBA")

        dress_img = dress_img.resize((user_img.width, int(user_img.height * 0.4)))
        user_img.paste(dress_img, (0, int(user_img.height * 0.25)), dress_img)

        filename = f"{uuid.uuid4()}.png"
        os.makedirs("static", exist_ok=True)
        output_path = f"static/{filename}"
        user_img.save(output_path)

        return jsonify({"result_url": f"http://localhost:3000/static/{filename}"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

