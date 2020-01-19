from ansiblelint import AnsibleLintRule


class InvalidIPaddressbinding(AnsibleLintRule):
    id = 'ANSIBLE0007'
    descreiption = 'check if the IP address has the 0.0.0.0 format'
    severity = 'HIGH'
    tags = ['validity']
    version_added = 'v1.0.0'
    shortdesc = 'check if password is fixed'

    def match(self, file, line):
        if "0.0.0.0" in line:
            return True
        return False
