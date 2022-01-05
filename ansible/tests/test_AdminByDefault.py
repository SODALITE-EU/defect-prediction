from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner

from ansiblelints.rules.AdminByDefault import AdminByDefault
import unittest

class TestAdminByDefault(unittest.TestCase):

    def test_file(self):
        collection = RulesCollection()
        collection.register(AdminByDefault())
        file_name = 'testResources/ansible-smell/adminbydefault.yml'
        good_runner = Runner(playbook=file_name, rules=collection)
        # print(good_runner.run())
        assert 3 == len(good_runner.run())
