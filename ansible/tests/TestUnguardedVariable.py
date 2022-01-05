import unittest

from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner

from ansiblelints.stage.UnguardedVariable import UnguardedVariable


class TestUnguardedVariable(unittest.TestCase):
    collection = RulesCollection()

    def setUp(self):
        self.collection.register(UnguardedVariable())

    def test_file(self):
        file_name = 'testResources/ansible-smell/hardcodepassword5.yml'
        good_runner = Runner(playbook=file_name, rules=self.collection)

        print(good_runner.run())
