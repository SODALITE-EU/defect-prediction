import unittest
from ansiblelint import RulesCollection, Runner
from ansiblelintsoda.rules.EmptyPassword0 import EmptyPassword0

class TestEmptyPassword(unittest.TestCase):
    collection = RulesCollection()

    def setUp(self):
        self.collection.register(EmptyPassword0())

    def test_file(self):
        success = 'ansible-smell/adminbydefault.yml'
        good_runner = Runner(self.collection, success, [], [], [])
        print(good_runner.run())
        print(len(good_runner.run()))
        self.assertEqual(0, len(good_runner.run()))



