from flask import Flask, json
from api import Linter

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/bugs/ansible/json', methods=['GET'])
def home():
    matches = Linter.main(["-r", "../ansiblelints/rules", "-R", "../testResources/ansible-smell/adminbydefault.yml"])
    data = []
    for match in matches:
        data.append({"bug_name": str(match.rule)})
    return json.dumps(data, sort_keys=False, indent=4), 200


app.run()
