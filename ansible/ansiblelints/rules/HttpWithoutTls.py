from ansiblelint import AnsibleLintRule


class HttpWithoutTls(AnsibleLintRule):
    id = 'ANSIBLE0008'
    description = 'check if url addresses has http instead of https'
    severity = 'HIGH'
    tags = {'incomplete'}
    version_added = 'v1.0.0'
    _modules = ['uri']
    shortdesc = 'HttpWithoutTLS'
    _modules = ['uri']

    def matchtask(self, file, task):

        if task["action"]["__ansible_module__"] in self._modules:
            url = task['action'].get('url')
            url = str(url)
            return "http://" in url
        return False
