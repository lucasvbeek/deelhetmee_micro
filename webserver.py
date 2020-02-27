from flask import Flask, jsonify, request
from flask_cors import CORS
import config
import audio_helper
import os
import str_helper
import requests

app = Flask(__name__)

CORS(app)

# API routes
@app.route("/create/<prefix>", methods=["POST"])
def api_create(prefix):
    not_new = True
    while not_new:
        file_name = str_helper.random_string()
        temp_path = f"./temp_sounds/{file_name}.wav"
        if not os.path.exists(f"{config.MAIN_SITE}/static/sounds/{file_name}.mp3"):
            not_new = False
    f = open(temp_path, "wb")
    f.write(request.data)
    f.close()
    sound = audio_helper.create_sound(temp_path, prefix=f"./sounds/{prefix}.wav")
    file_name_no_path = f"{file_name}.mp3"
    export_path = f"./final_sounds/{file_name_no_path}"
    sound.export(export_path, format="mp3")
    os.remove(temp_path)
    export_file = open(export_path, "rb")
    files = {"sound": export_file}
    params = {"name": file_name, "token": config.TOKEN}
    requests.post(f"{config.MAIN_SITE}/savesound", files=files, params=params)
    export_file.close()
    os.remove(export_path)
    return file_name

@app.route("/prefixes")
def api_prefixes():
    path = "./sounds/"
    all_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    all_files = [f.split(".")[0] for f in all_files]
    return jsonify(all_files)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG)
