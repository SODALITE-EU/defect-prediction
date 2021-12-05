import unittest

from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner

from ansiblelints.stage.InvalidPropertyValue import InvalidPropertyValue


class TestInvalidPropertyValue(unittest.TestCase):
    collection = RulesCollection()

    def setUp(self):
        self.collection.register(InvalidPropertyValue())

    def test_file(self):
        file_name = 'testResources/ansible-smell/httpwithouttls3.yml'
        good_runner = Runner(file_name, rules=self.collection)

        print(good_runner.run())
