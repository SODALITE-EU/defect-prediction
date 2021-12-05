from ansiblelint.rules import AnsibleLintRule


class UnguardedVariable(AnsibleLintRule):
    id = 'ANSIBLE0019'
    descreiption = 'respect the syntax/braces of Jinja2 in script like {{}} or {##}'
    severity = 'High'
    tags = {'correctness'}
    version_added = 'v1.0.0'
    shortdesc = 'respect the syntax/braces of Jinja2 in script'

    def matchlines(self, file, text):

        for (prev_line_no, line) in enumerate(text.split("\n")):
            if prev_line_no != 0:
                if len(line) != 0:
                    if "{{" in line:
                        if "}}" not in line:
                            return (prev_line_no, line)
                    elif "{ {" in line:
                        if "} }" not in line:
                            return (prev_line_no, line)
                    elif "{#" in line:
                        if "#}" not in line:
                            return (prev_line_no, line)
                    elif "{%" in line:
                        if "%}" not in line:
                            return (prev_line_no, line)
                    else:
                        return 'None found'
        return []
