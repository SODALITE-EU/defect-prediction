from ansiblelint import AnsibleLintRule


class InconsistentNaming(AnsibleLintRule):
    id = 'ANSIBLE0014'
    descreiption = 'Human meaningful name of the role or task to communicate the purpose'
    severity = 'medium'
    tags = {'clarity'}
    version_added = 'v1.0.0'
    #_modules = ['hosts']
    shortdesc ='meaningful and less confusing names for role or tasks should exist'

    def match(self, file, line):
        if "name:"in line:
            if len(line.split("name:")[1]) < 7:
                return(line)