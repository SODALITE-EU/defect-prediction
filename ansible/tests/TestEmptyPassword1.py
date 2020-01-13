import unittest
from ansiblelint import RulesCollection, Runner
from ansiblelints.rules.EmptyPassword0 import EmptyPassword

class TestEmptyPassword(unittest.TestCase):
    collection = RulesCollection()

    def setUp(self):
        self.collection.register(EmptyPassword())

    def test_file(self):
        success = 'testResources/ansible-smell/adminbydefault.yml'
        good_runner = Runner(self.collection, success, [], [], [])
        print(good_runner.run())
        print(len(good_runner.run()))
        self.assertEqual(0, len(good_runner.run()))

