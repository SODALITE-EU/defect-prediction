from api import Linter

matches = Linter.main(["-r","../ansiblelints/rules","-R","../testResources/ansible-smell/adminbydefault.yml"])
for match in matches:
    print(str(match.rule))