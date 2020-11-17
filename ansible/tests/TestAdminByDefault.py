import unittest

from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner

from ansiblelints.rules.AdminByDefault import AdminByDefault


class TestAdminByDefault(unittest.TestCase):
    collection = RulesCollection()

    def setUp(self):
        self.collection.register(AdminByDefault())

    def test_file(self):
        success = 'testResources/ansible-smell/adminbydefault.yml'
        good_runner = Runner(self.collection, success, [], [], [])
        # print(good_runner.run())
        self.assertEqual(3, len(good_runner.run()))
