import unittest

from ansiblelint import RulesCollection, Runner

from ansiblelints.rules.HardCodedSecrets import HardCodedSecrets


class TestAdminByDefault(unittest.TestCase):
    collection = RulesCollection()

    def setUp(self):
        self.collection.register(HardCodedSecrets())

    def test_file(self):
        success = 'testResources/ansible-smell/create.yml'
        good_runner = Runner(self.collection, success, [], [], [])
        # print(good_runner.run())
        self.assertEqual(1, len(good_runner.run()))
