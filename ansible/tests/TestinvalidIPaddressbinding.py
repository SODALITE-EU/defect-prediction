import unittest

from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner

from ansiblelints.rules.InvalidIPaddressbinding import InvalidIPaddressbinding


class TestInvalidIPaddressbinding(unittest.TestCase):
    collection = RulesCollection()

    def setUp(self):
        self.collection.register(InvalidIPaddressbinding())

    def test_file(self):
        success = 'testResources/ansible-smell/invalidIPaddressbinding.yml'
        good_runner = Runner(self.collection, success, [], [], [])
        result = good_runner.run()
        print(result)
        print(type(result))
        print(len(result))
        self.assertGreaterEqual(1, len(good_runner.run()))
