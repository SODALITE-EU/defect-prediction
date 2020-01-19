from ansiblelint import AnsibleLintRule


class DuplicateEntity(AnsibleLintRule):
    id = 'ANSIBLE0015'
    descreiption = 'unexpected results can happen from same names from different handelers'
    severity = 'medium'
    tags = {'complex'}
    version_added = 'v1.0.0'
    shortdesc = 'use unique name for handelers'

    def match(self, file, line):
        if "name:" in line:
            return (line.split("name:")[1])
        return False
