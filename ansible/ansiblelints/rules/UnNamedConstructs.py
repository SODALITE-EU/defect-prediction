from ansiblelint import AnsibleLintRule


class UnNamedConstructs(AnsibleLintRule):
    id = 'ANSIBLE0013'
    descreiption = 'the name of the role or task has not been specified'
    severity = 'medium'
    tags = {'clarity'}
    version_added = 'v1.0.0'
    _modules = ['hosts']
    shortdesc = 'meaningful names for role or tasks should exist'

    def match(self, file, line):
        if "- " in line:
            if 'name' not in line.split(":")[0]:
                return line

        return False
