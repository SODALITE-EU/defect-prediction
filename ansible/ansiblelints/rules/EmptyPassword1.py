from ansiblelint.rules import AnsibleLintRule


class EmptyPassword1(AnsibleLintRule):
    id = 'ANSIBLE0005'
    description = 'check if password is empty'
    severity = 'HIGH'
    tags = {'incomplete'}
    version_added = 'v1.0.0'
    _modules = ['add_host']
    shortdesc = 'EmptyPassword'

    def matchtask(self, file, task):
        if task["action"]["__ansible_module__"] in self._modules:
            pass_word = task['action'].get('ansible_ssh_pass')
            pass_word = str(pass_word)
            return "default('')" in pass_word

        return False
