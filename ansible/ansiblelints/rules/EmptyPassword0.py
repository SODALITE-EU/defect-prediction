from ansiblelint import AnsibleLintRule


class EmptyPassword(AnsibleLintRule):
    id = 'ANSIBLE0004'
    descreiption = 'check if password is empty'
    severity = 'HIGH'
    tags = {'incomplete'}
    version_added = 'v1.0.0'
    _modules = ['add_host']
    shortdesc ='check if password is empty'

    def matchtask(self, file, task):
        #print(task)
        #print(str(task['action'].get('ansible_become_pass')))
        #print(type(task["action"]["__ansible_module__"]))
        if task["action"]["__ansible_module__"] in self._modules:
            pass_word = task['action'].get('ansible_become_pass')
            pass_word = str(pass_word)
            #print(pass_word)
            #print(len(pass_word))
            #print("default('')" in pass_word)
            return "default('')" in pass_word
