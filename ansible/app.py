import os
from pathlib import Path

from flask import Flask, json, request, Response
from werkzeug.utils import secure_filename

import Linter

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/bugs/ansible/json', methods=['POST'])
def detect_bugs_json():
    input = request.get_json()
    res = run_detector(input["ansible_definition"], input["action_id"], input["deployment_id"])
    return res


@app.route('/bugs/ansible/file', methods=['POST'])
def detect_bugs_file():
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
        res = run_detector(file_path, "default", "default")
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print("The file does not exist to be removed")
        return res


def run_detector(file, action_id, deployment_id):
    matches = Linter.main(["-r", "ansiblelints/rules", "-R", file])
    data = []
    bugs = {"action_id": action_id, "deployment_id": deployment_id, "bugs": data}
    for match in matches:
        bugrecord = {"bug_name": str(match.rule),
                     "bug_info": {"uri": str(match.linenumber) + " , " + str(match.line),
                                  "description": str(match.message)}}
        data.append(bugrecord)
    js = json.dumps(bugs, sort_keys=False, indent=4)

    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST'
    resp.headers['Access-Control-Max-Age'] = '1000'
    return resp


app.run(host='0.0.0.0', port=5000)
