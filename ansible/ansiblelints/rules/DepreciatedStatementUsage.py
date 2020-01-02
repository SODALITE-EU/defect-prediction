from ansiblelint import AnsibleLintRule


class DepreciatedStatementUsage(AnsibleLintRule):
    id = 'ANSIBLE0021'
    descreiption = 'Prevent using depreciated syntax in Ansible playbook'
    severity = 'High'
    tags = {'clarity'}
    version_added = 'v1.0.0'
    shortdesc ='Prevent using depreciated syntax in Ansible playbook'

    def matchlines(self, file, text):
        for (prev_line_no, line) in enumerate(text.split("\n")):
            if prev_line_no != 0:
                if len(line) != 0 :
                    if 'when:' in line:
                        if "{{" in line:
                            return(prev_line_no,line)
                        elif "{ {" in line:
                            return (prev_line_no, line)
                        elif "{#" in line:
                            return (prev_line_no, line)
                        elif "{%" in line:
                            return (prev_line_no, line)
