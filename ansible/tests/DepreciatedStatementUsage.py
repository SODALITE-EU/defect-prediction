from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner

from ansiblelints.stage.DepreciatedStatementUsage import DepreciatedStatementUsage


class TestDepreciatedStatementUsage:

    def test_file(self):
        collection = RulesCollection()
        collection.register(DepreciatedStatementUsage())

        file_name = 'testResources/ansible-smell/adminbydefault.yml'
        good_runner = Runner(file_name, rules=collection)

        print(good_runner.run())
