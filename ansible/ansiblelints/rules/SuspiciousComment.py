from ansiblelint import AnsibleLintRule
import ruamel.yaml

class SuspiciousComment(AnsibleLintRule):
    id = 'ANSIBLE0009'
    descreiption = 'check if there are wrong words in comments'
    severity = 'HIGH'
    tags = ['validity']
    version_added = 'v1.0.0'
    shortdesc = "check if there are wrong words in comments"

    def matchtasks(self, file, task):

        with open(file['path']) as fp:
            data = ruamel.yaml.round_trip_load(fp)

        res = []
        for line in ruamel.yaml.round_trip_dump(data, indent=2, block_seq_indent=3).splitlines(True):
            if "#" in line:
                if 'TODO' in line:
                    res.append(line)
        return res
