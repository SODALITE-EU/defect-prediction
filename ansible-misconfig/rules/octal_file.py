from ansiblelint import AnsibleLintRule
import re

class ModuleOctalPermissions(AnsibleLintRule):
    id = 'E401'
    shortdesc = 'Octal file permissions must contain leading zero'
    description = 'Numeric file permissions without leading zero can behave' + \
        'in unexpected ways. See ' + \
        'http://docs.ansible.com/ansible/file_module.html'
    tags = ['module']
    _modules = ['file']
    mode_regex = re.compile(r'^\s*[0-9]+\s*$')
    valid_mode_regex = re.compile(r'^\s*0[0-7]{3,4}\s*$')
    def matchtask(self, file, task):
        if task["action"]["__ansible_module__"] in self._modules:
            mode = task['action'].get('mode', None)
            if isinstance(mode, str) and self.mode_regex.match(mode):
                return not self.valid_mode_regex.match(mode)
            if isinstance(mode, int):
                result = (mode % 8 and mode % 8 < 4 or
                          (mode >> 3) % 8 and (mode >> 3) % 8 < 4 or
                          (mode >> 6) % 8 and (mode >> 6) % 8 < 4 or
                          mode & 8 < (mode << 3) & 8 or
                          mode & 8 < (mode << 6) & 8 or
                          (mode << 3) & 8 < (mode << 6) & 8)
                return result