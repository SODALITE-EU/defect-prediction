from ansiblelint import AnsibleLintRule


class AdminByDefault(AnsibleLintRule):
    id = 'ANSIBLE0003'
    descreiption = 'Set admin as default-admin when it is empty'
    severity = 'HIGH'
    tags = {'incomplete'}
    version_added = 'v1.0.0'
    _modules = ['add_host','fortiosconfig']
    shortdesc ='some'

    def matchtask(self, file, task):

        if task["action"]["__ansible_module__"] in self._modules:
            usr = task['action'].get('ansible_become_user')
            usr = str(usr)
            return usr in ['root', 'admin']
        return False
