import pytest
from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner

from ansiblelints.stage.DepreciatedStatementUsage import DepreciatedStatementUsage


class TestDepreciatedStatementUsage:

    def test_file(self):
        collection = RulesCollection()
        self.collection.register(DepreciatedStatementUsage())

        file_name = 'testResources/ansible-smell/adminbydefault.yml'
        good_runner = Runner(self.collection, file_name, [], [], [])

        print(good_runner.run())
