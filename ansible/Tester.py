import Linter

matches = Linter.main(["-v", "-r", "../ansiblelints/rules", "-R", "../testResources/ansible-smell/create.yml"])
for match in matches:
    print(match.__dict__)
