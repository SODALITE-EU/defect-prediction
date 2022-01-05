from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner
import unittest
from ansiblelints.rules.SuspiciousComment import SuspiciousComment


class TestSuspiciousComment(unittest.TestCase):

    def test_file(self):
        collection = RulesCollection()
        collection.register(SuspiciousComment())
        file_name = str('testResources/ansible-smell/suspiciouscomment.yml')
        good_runner = Runner(playbook=file_name, rules=collection)
        print(good_runner.run())
