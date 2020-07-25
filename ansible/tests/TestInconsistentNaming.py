import unittest

from ansiblelint import RulesCollection, Runner

from ansiblelints.stage.InconsistentNaming import InconsistentNaming


class TestInconsistentNaming(unittest.TestCase):
    collection = RulesCollection()

    def setUp(self):
        self.collection.register(InconsistentNaming())

    def test_file(self):
        file_name = 'testResources/ansible-smell/unnamedconstructs.yml'
        good_runner = Runner(self.collection, file_name, [], [], [])
        print(good_runner.run())
