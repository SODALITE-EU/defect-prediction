import unittest

from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner

from ansiblelints.stage.IncompleteConditional import IncompleteConditional


class TestIncompleteConditional(unittest.TestCase):
    collection = RulesCollection()

    def setUp(self):
        self.collection.register(IncompleteConditional())

    def test_file(self):
        file_name = 'testResources/ansible-smell/hardcodepassword5.yml'
        good_runner = Runner(file_name, rules=self.collection)

        print(good_runner.run())
