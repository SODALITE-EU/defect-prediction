from ansiblelint import AnsibleLintRule


def ishardcoded(usr):
    print("******" +str(usr))
    if usr:
        if "{" in str(usr):
            return False
        return True
    return False


class HardCodedSecrets(AnsibleLintRule):
    id = 'ANSIBLE000311'
    description = 'The password or username is hardcoded.'
    severity = 'HIGH'
    tags = {'incomplete'}
    version_added = 'v1.0.0'
    _modules = ['add_host', 'fortiosconfig']
    shortdesc = 'HardCodedSecrets'

    def matchtask(self, file, task):
        if task["action"]["__ansible_module__"] in self._modules:
            if ishardcoded(task['action'].get('ansible_become_user')) or ishardcoded(
                    task['action'].get('ansible_user')):
                return True

        return False
