import pytest

from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner
from ansiblelints.rules.AdminByDefault import AdminByDefault


class TestAdminByDefault:

    def test_file(self):
        collection = RulesCollection()
        collection.register(AdminByDefault())
        success = 'testResources/ansible-smell/adminbydefault.yml'
        good_runner = Runner(collection, success, [], [], [])
        # print(good_runner.run())
        assert 3 == len(good_runner.run())
