import ruamel.yaml
from ansiblelint import AnsibleLintRule


class WeakCryptographyalgo(AnsibleLintRule):
    id = 'ANSIBLE0010'
    description = 'check if weak algorithms such as MD5 are used or not '
    severity = 'HIGH'
    tags = {'weak algo'}
    version_added = 'v1.0.0'
    shortdesc = 'WeakCryptographyalgo'
    # _commands = ['shell']
    _modules = ['add_host']

    def matchtask(self, file, task):

        with open(file['path']) as fp:
            data = ruamel.yaml.round_trip_load(fp)

        for line in ruamel.yaml.round_trip_dump(data, indent=2, block_seq_indent=3).splitlines(True):
            if "MD5" or 'md5' in line:
                return True
        return False
