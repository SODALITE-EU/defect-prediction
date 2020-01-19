from ansiblelint import AnsibleLintRule


class IncompleteConditional(AnsibleLintRule):
    id = 'ANSIBLE0018'
    descreiption = 'Always state the conditional'
    severity = 'High'
    tags = {'clarity'}
    version_added = 'v1.0.0'
    shortdesc ='always state the conditional'


    def matchlines(self, file, text):

        for (prev_line_no, line) in enumerate(text.split("\n")):
            if prev_line_no != 0:
                if len(line) != 0 :
                    if "when:" in line:
                        if len(line.split("when:")[1]) == 0:
                            return(prev_line_no,line)
                        else:
                            return('None found')
        return []