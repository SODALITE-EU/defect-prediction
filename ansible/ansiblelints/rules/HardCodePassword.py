from ansiblelint import AnsibleLintRule


class HardCodePassword(AnsibleLintRule):
    id = 'ANSIBLE0006'
    description = 'check if password is fixed'
    severity = 'HIGH'
    tags = {'incomplete'}
    version_added = 'v1.0.0'
    _modules = ['zabbix_group']
    shortdesc = 'HardCodePassword'

    def matchtask(self, file, task):
        if task["action"]["__ansible_module__"] in self._modules:
            pass_word = task['action'].get('login_password')
            pass_word = str(pass_word)
            print(len(pass_word))
            if len(pass_word) == 0:
                return True
            return False
        return False
