from ansiblelint import AnsibleLintRule
import ruamel.yaml


class ComplexExpression(AnsibleLintRule):
    id = 'ANSIBLE0012'
    descreiption = 'code script contains a difficult to understand complex expression like having several if, and, or'
    severity = 'medium'
    tags = {'complex'}
    version_added = 'v1.0.0'
    shortdesc = 'difficult to understand complex expression in code'

    # _modules = ['fortiosconfig']

    def match(self, file, line):
        if ' when:' in line:
            if sum(line.count(word) for word in [' if ', ' and ', ' or ', '|', ' | ']) > 2:
                return True
            return False
        return False
