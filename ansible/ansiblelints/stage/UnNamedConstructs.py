from ansiblelint import AnsibleLintRule


class UnNamedConstructs(AnsibleLintRule):
    id = 'ANSIBLE0013'
    description = 'the name of the role or task has not been specified'
    severity = 'medium'
    tags = {'clarity'}
    version_added = 'v1.0.0'
    _modules = ['hosts']
    shortdesc = 'UnNamedConstructs'

    def match(self, file, line):
        if "- " in line:
            if 'name' not in line.split(":")[0]:
                return True

        return False
