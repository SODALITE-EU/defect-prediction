import os
from pathlib import Path

from flask import Flask, json, request, Response
from werkzeug.utils import secure_filename

import Linter
from ansible_lint_rule_generator import generate_linter_rules

app = Flask(__name__)
app.config["DEBUG"] = True
import nltk

import en_core_web_sm

nlp = en_core_web_sm.load()

nltk.download('punkt')
nltk.download('en_core_web_md')


@app.route('/ansible/misconfig/rules', methods=['POST'])
def re_generate_rules():
    module_names = request.get_json()["modules"]
    # TODO
    # TODO Parse the documentation for the give modules and generate rules
    generate_linter_rules()
    js = json.dumps({'message': 'Rule were generated for ' + module_names}, sort_keys=False, indent=4)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route('/ansible/misconfig/file', methods=['POST'])
def detect_misconfigurations():
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
    matches = Linter.main(["-r", "rules", "-R", file])
    data = []
    bugs = {"action_id": action_id, "deployment_id": deployment_id, "bugs": data}
    for match in matches:
        bugrecord = {"bug_name": str(match.rule),
                     "bug_info": {"uri": str(match.linenumber) + " , " + str(match.line),
                                  "description": str(match.message)}}
        data.append(bugrecord)
    js = json.dumps(bugs, sort_keys=False, indent=4)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


app.run(host='0.0.0.0', port=5000)
