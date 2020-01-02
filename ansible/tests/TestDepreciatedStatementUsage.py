import unittest
from ansiblelint import RulesCollection, Runner
from ansiblelintsoda.rules.DepreciatedStatementUsage import DepreciatedStatementUsage


class TestDepreciatedStatementUsage(unittest.TestCase):
    collection = RulesCollection()

    def setUp(self):
        self.collection.register(DepreciatedStatementUsage())

    def test_file(self):
        file_name = 'ansible-smell/adminbydefault.yml'
        good_runner = Runner(self.collection, file_name, [], [], [])

        print(good_runner.run())