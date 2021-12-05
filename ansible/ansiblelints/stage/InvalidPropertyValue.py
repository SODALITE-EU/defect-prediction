from ansiblelint.rules import AnsibleLintRule


class InvalidPropertyValue(AnsibleLintRule):
    id = 'ANSIBLE0022'
    descreiption = 'Prevent error by using the valid syntax'
    severity = 'High'
    tags = {'correctness'}
    version_added = 'v1.0.0'
    shortdesc = 'Prevent error by using the valid syntax'

    def matchlines(self, file, text):
        for (prev_line_no, line) in enumerate(text.split("\n")):
            if prev_line_no != 0:
                if len(line) != 0:

                    if '==' in line:
                        if line.split("==")[1].split(' ')[1] == 'True':
                            return (prev_line_no, line)
                        elif line.split("==")[1].split(' ')[1] == 'False':
                            return (prev_line_no, line)
                        elif line.split("==")[1].split(' ')[1] == "''":
                            return (prev_line_no, line)
                        else:
                            return ('OK')

                    if '!=' in line:
                        if line.split("!=")[1].split(' ')[1] == 'True':
                            return (prev_line_no, line)
                        elif line.split("!=")[1].split(' ')[1] == 'False':
                            return (prev_line_no, line)
                        elif line.split("!=")[1].split(' ')[1] == "''":
                            return (prev_line_no, line)
                        else:
                            return ('OK')

        return []
