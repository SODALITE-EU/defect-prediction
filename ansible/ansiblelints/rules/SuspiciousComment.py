from ansiblelint import AnsibleLintRule, Match


def issuspicious(line):
    if "#" in line:
        if 'todo' in line.lower():
            return True
        if 'bug' in line.lower():
            return True
        if 'fixme' in line.lower():
            return True


class SuspiciousComment(AnsibleLintRule):
    id = 'ANSIBLE0009'
    description = 'check if there are wrong words in comments'
    severity = 'HIGH'
    tags = ['validity']
    version_added = 'v1.0.0'
    shortdesc = "SuspiciousComments"

    def matchlines(self, file, text):
        matches = []
        # arrays are 0-based, line numbers are 1-based
        # so use prev_line_no as the counter
        for (prev_line_no, line) in enumerate(text.split("\n")):
            if issuspicious(line):
                matches.append(Match(prev_line_no + 1, line,
                                     file['path'], self, self.shortdesc))
        return matches
