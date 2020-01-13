import unittest
from ansiblelint import RulesCollection, Runner
from ansiblelints.rules.LongStatement import LongStatement


class TestLongStatement(unittest.TestCase):
    collection = RulesCollection()

    def setUp(self):
        self.collection.register(LongStatement())

    def test_file(self):
        file_name = 'tests/ansible-smell/many.yaml'
        good_runner = Runner(self.collection, file_name, [], [], [])

        print(good_runner.run())
