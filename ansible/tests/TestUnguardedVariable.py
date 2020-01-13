import unittest
from ansiblelint import RulesCollection, Runner
from ansiblelints.rules.UnguardedVariable import UnguardedVariable


class TestUnguardedVariable(unittest.TestCase):
    collection = RulesCollection()

    def setUp(self):
        self.collection.register(UnguardedVariable())

    def test_file(self):
        file_name = 'tests/ansible-smell/hardcodepassword5.yml'
        good_runner = Runner(self.collection, file_name, [], [], [])

        print(good_runner.run())
