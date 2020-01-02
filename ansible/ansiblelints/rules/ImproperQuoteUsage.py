from ansiblelint import AnsibleLintRule


class ImproperQuoteUsage(AnsibleLintRule):
    id = 'ANSIBLE0017'
    descreiption = 'only single or double quotes should be used in scripts'
    severity = 'medium'
    tags = {'clarity'}
    version_added = 'v1.0.0'
    shortdesc ='consistency of single or duoble quoting'


    def matchlines(self, file, text):

        for (prev_line_no, line) in enumerate(text.split("\n")):
            if prev_line_no != 0:
                if len(line) != 0 :

                    if "{{" in line:
                        if line.startswith("'") and line.endswith("'"):
                            return(prev_line_no,line)

                    elif ": " in line:

                        if line.split(": ")[1].startswith("'") and line.split(": ")[1].endswith("'"):
                            return(prev_line_no,line)
                        elif line.split(": ")[1].startswith('"') and line.split(": ")[1].endswith('"'):
                            return(prev_line_no,line)