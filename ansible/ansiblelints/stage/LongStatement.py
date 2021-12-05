from ansiblelint.rules import AnsibleLintRule


class LongStatement(AnsibleLintRule):
    id = 'ANSIBLE0020'
    descreiption = 'Keeping line in YAML file below 160 characters'
    severity = 'medium'
    tags = {'clarity'}
    version_added = 'v1.0.0'
    shortdesc = 'Keeping line in YAML file below 160 characters'

    def matchlines(self, file, text):

        for (prev_line_no, line) in enumerate(text.split("\n")):
            if prev_line_no != 0:
                if len(line) > 160:
                    return (prev_line_no, len(line), line)
        return []
