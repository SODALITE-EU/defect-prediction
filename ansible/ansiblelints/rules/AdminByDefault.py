from ansiblelint import AnsibleLintRule


def isadmin(usr):
    usr = str(usr)
    return usr in ['root', 'admin']


class AdminByDefault(AnsibleLintRule):
    id = 'ANSIBLE0003'
    description = 'The user is admin by default'
    severity = 'HIGH'
    tags = {'incomplete'}
    version_added = 'v1.0.0'
    _modules = ['add_host', 'fortiosconfig']
    shortdesc = 'AdminByDefault'

    def matchtask(self, file, task):
        if task["action"]["__ansible_module__"] in self._modules:
            if isadmin(task['action'].get('ansible_become_user')) or isadmin(task['action'].get('ansible_user')):
                return True

        return False
