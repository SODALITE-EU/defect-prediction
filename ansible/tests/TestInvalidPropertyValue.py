import unittest

from ansiblelint import RulesCollection, Runner

from ansiblelints.stage.InvalidPropertyValue import InvalidPropertyValue


class TestInvalidPropertyValue(unittest.TestCase):
    collection = RulesCollection()

    def setUp(self):
        self.collection.register(InvalidPropertyValue())

    def test_file(self):
        file_name = 'testResources/ansible-smell/httpwithouttls3.yml'
        good_runner = Runner(self.collection, file_name, [], [], [])

        print(good_runner.run())
