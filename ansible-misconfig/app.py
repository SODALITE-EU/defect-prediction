import os
from pathlib import Path

from flask import Flask, json, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["DEBUG"] = True
import nltk

nltk.download('punkt')
nltk.download('en_core_web_md')

@app.route('/bugs/ansible/misconfig/file', methods=['POST'])
def detect_linguistic_bugs():
    home = str(Path.home())
    soda_home = os.path.join(home, ".sodalite")
    if not os.path.exists(soda_home):
        os.makedirs(soda_home)

    if 'file' not in request.files:
        return json.dumps({'message': 'No file part in the request'}, sort_keys=False, indent=4), 400

    file = request.files['file']

    if file.filename == '':
        return json.dumps({'message': 'No file selected for uploading'}, sort_keys=False, indent=4), 400
    else:
        filename = secure_filename(file.filename)
        file_path = os.path.join(soda_home, filename)
        file.save(file_path)
        res = json.dumps({'message': 'the api is not complete yet'}, sort_keys=False, indent=4), 400
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print("The file does not exist to be removed")
        return res


app.run(host='0.0.0.0', port=5000)
