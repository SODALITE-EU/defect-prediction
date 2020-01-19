from api import Linter

matches = Linter.main(["-v", "-r", "../ansiblelints/rules", "-R", "../testResources/ansible-smell/adminbydefault.yml"])
for match in matches:
    print(match.__dict__)
