from ansiblelint.rules import AnsibleLintRule #NOSONAR


class DeprecatedVariableRule(AnsibleLintRule):
    id = 'ANSIBLE0001'
    shortdesc = 'DeprecatedVariables'
    description = 'Check for lines that have old style ${var} ' + \
                  'declarations'
    tags = {'deprecated'}

    def match(self, file, line):
        return '${' in line
