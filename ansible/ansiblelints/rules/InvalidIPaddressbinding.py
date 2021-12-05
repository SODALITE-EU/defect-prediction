from ansiblelint.rules import AnsibleLintRule


class InvalidIPaddressbinding(AnsibleLintRule):
    id = 'ANSIBLE0007'
    description = 'check if the IP address has the 0.0.0.0 format'
    severity = 'HIGH'
    tags = ['validity']
    version_added = 'v1.0.0'
    shortdesc = 'InvalidIPAddressBinding'

    def match(self, file, line):
        if "0.0.0.0" in line:
            return True
        return False
