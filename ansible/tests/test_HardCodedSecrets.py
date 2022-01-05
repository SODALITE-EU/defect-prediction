from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner
import unittest
from ansiblelints.rules.HardCodedSecrets import HardCodedSecrets


class TestAdminByDefault(unittest.TestCase):

    def test_file(self):
        collection = RulesCollection()
        collection.register(HardCodedSecrets())
        file_name = 'testResources/ansible-smell/create.yml'
        good_runner = Runner(rules=collection, playbook=file_name)
        # print(good_runner.run())
        assert 1 == len(good_runner.run())
