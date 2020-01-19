from flask import Flask, json, request
import os
from api import Linter
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["DEBUG"] = True
UPLOAD_FOLDER = '/home/indika/tmp/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/bugs/ansible/json', methods=['POST'])
def detectBugsJson():
    input = request.get_json()
    res = runDetector(input["ansible_definition"], input["action_id"], input["deployment_id"])
    return res, 200

@app.route('/bugs/ansible/file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return json.dumps({'message': 'No file part in the request'}, sort_keys=False, indent=4), 400

    file = request.files['file']

    if file.filename == '':
        return json.dumps({'message': 'No file selected for uploading'}, sort_keys=False, indent=4), 400
    else:
        folder = os.path.join(app.config['UPLOAD_FOLDER'])
        print(file.filename)
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_path = str(folder) + str(file.filename);
        res = runDetector(file_path,"default","default")
        os.remove(file_path)
        return res, 200


def runDetector(file, action_id, deployment_id):
    matches = Linter.main(["-r", "../ansiblelints/rules", "-R", file])
    data = []
    bugs = {"action_id": action_id, "deployment_id": deployment_id, "bugs": data}
    for match in matches:
        bugrecord = {"bug_name": str(match.rule),
                     "bug_info": {"location": str(match.linenumber) + " , " + str(match.line),
                                  "description": str(match.message)}}
        data.append(bugrecord)
    return json.dumps(bugs, sort_keys=False, indent=4)


app.run()
