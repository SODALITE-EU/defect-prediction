from ansiblelint import AnsibleLintRule


class UnNamedConstructs(AnsibleLintRule):
    id = 'ANSIBLE0013'
    descreiption = 'the name of the role or task has not been specified'
    severity = 'medium'
    tags = {'clarity'}
    version_added = 'v1.0.0'
    _modules = ['hosts']
    shortdesc ='meaningful names for role or tasks should exist'

    def match(self, file, line):
        if "- "in line:
            if 'name' not in line.split(":")[0]:
                return(line)




    #def matchtasks(self, file, task):
    #    if task["action"]["__ansible_module__"] in self._modules:
    #        name_value = task['action'].get('name')
    #        if len(name_value) == 0:
    #            return(name_value)

