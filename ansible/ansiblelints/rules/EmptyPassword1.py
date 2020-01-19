from ansiblelint import AnsibleLintRule


class EmptyPassword1(AnsibleLintRule):
    id = 'ANSIBLE0005'
    descreiption = 'check if password is empty'
    severity = 'HIGH'
    tags = {'incomplete'}
    version_added = 'v1.0.0'
    _modules = ['add_host']
    shortdesc = 'check if password is empty'

    def matchtask(self, file, task):
        if task["action"]["__ansible_module__"] in self._modules:
            pass_word = task['action'].get('ansible_ssh_pass')
            pass_word = str(pass_word)
            # print(pass_word)
            return "default('')" in pass_word

        return False
