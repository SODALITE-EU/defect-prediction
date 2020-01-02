from ansiblelint import AnsibleLintRule


class ImproperAlignment(AnsibleLintRule):
    id = 'ANSIBLE0016'
    descreiption = 'double spaces are used for indentation instead of tabulation'
    severity = 'medium'
    tags = {'complex'}
    version_added = 'v1.0.0'
    shortdesc ='consistency of indentation and alignmnet'


    def matchlines(self, file, text):

        for (prev_line_no, line) in enumerate(text.split("\n")):
            if prev_line_no != 0:
                if len(line) != 0 :
                    if "- "in line:
                        indent_length = len(line.split("- ")[0]) + 2
                    else:
                        if line[-1] == ":" :
                            indent_length = indent_length + 2
                        else:

                            if (len(line) - len(line.strip(" "))) > indent_length:
                                print(indent_length)
                                print(len(line) - len(line.strip(" ")))
                                return(prev_line_no, line)

                            else:
                                return('no line found')



