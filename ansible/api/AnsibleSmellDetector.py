import flask
from api import Linter
app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/bugs/ansible/json', methods=['GET'])
def home():
    matches = Linter.main(["-r","../ansiblelints/test","-R","../testResources/ansible-smell/adminbydefault.yml"])
    for match in matches:
        print(match)
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction " \
           "novels.</p> "

app.run()