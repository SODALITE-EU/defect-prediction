from ansiblelint import AnsibleLintRule


class HardCodePassword(AnsibleLintRule):
    id = 'ANSIBLE0006'
    descreiption = 'check if password is fixed'
    severity = 'HIGH'
    tags = {'incomplete'}
    version_added = 'v1.0.0'
    _modules = ['zabbix_group']
    shortdesc ='check if password is fixed'

    def matchtask(self, file, task):
        #print(task)
        #print(str(task['action'].get('ansible_become_pass')))
        #print(type(task["action"]["__ansible_module__"]))
        if task["action"]["__ansible_module__"] in self._modules:
            pass_word = task['action'].get('login_password')
            pass_word = str(pass_word)
            #print(pass_word)
            print(len(pass_word))
            #print("default('')" in pass_word)
            if len(pass_word) == 0 :
                return True
            return False
        return False