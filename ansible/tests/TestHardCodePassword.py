import unittest

from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner

from ansiblelints.rules.HardCodePassword import HardCodePassword


class TestHardCodePassword(unittest.TestCase):
    collection = RulesCollection()

    def setUp(self):
        self.collection.register(HardCodePassword())

    def test_file(self):
        success = 'testResources/ansible-smell/hardcodepassword.yml'
        good_runner = Runner(self.collection, success, [], [], [])
        print(good_runner.run())
        print(type(good_runner.run()))
        print(len(good_runner.run()))
        self.assertEqual(0, len(good_runner.run()))
