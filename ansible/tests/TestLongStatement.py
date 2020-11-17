import unittest

from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner

from ansiblelints.stage.LongStatement import LongStatement


class TestLongStatement(unittest.TestCase):
    collection = RulesCollection()

    def setUp(self):
        self.collection.register(LongStatement())

    def test_file(self):
        file_name = 'testResources/ansible-smell/many.yaml'
        good_runner = Runner(self.collection, file_name, [], [], [])

        print(good_runner.run())
