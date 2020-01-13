import unittest
from ansiblelint import RulesCollection, Runner
from ansiblelints.rules.IncompleteConditional import IncompleteConditional


class TestIncompleteConditional(unittest.TestCase):
    collection = RulesCollection()

    def setUp(self):
        self.collection.register(IncompleteConditional())

    def test_file(self):
        file_name = 'testResources/ansible-smell/hardcodepassword5.yml'
        good_runner = Runner(self.collection, file_name, [], [], [])

        print(good_runner.run())
