from ansiblelint import AnsibleLintRule

class IncompleteConstructs(AnsibleLintRule):
    id = 'ANSIBLE0002'
    descreiption = 'Incomplete tasks in programming indicate with comments like #TODO'
    severity = 'LOW'
    tags = {'incomplete'}
    version_added = 'v1.0.0'

    comments_word_list = ['TODO', 'TO DO', 'FIXME', 'FIX ME']

    def matchtask(self, file,task):
        for comments_word in comment_word_list:
            return comments_word in task.get('name')