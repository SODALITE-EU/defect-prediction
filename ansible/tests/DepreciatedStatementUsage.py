import unittest

from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner

from ansiblelints.stage.DepreciatedStatementUsage import DepreciatedStatementUsage


class TestDepreciatedStatementUsage(unittest.TestCase):

    def test_file(self):
        collection = RulesCollection()
        collection.register(DepreciatedStatementUsage())

        file_name = 'testResources/ansible-smell/adminbydefault.yml'
        good_runner = Runner(playbook=file_name, rules=collection)

        print(good_runner.run())
