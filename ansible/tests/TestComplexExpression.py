import unittest
from ansiblelint import RulesCollection, Runner
from ansiblelints.rules.ComplexExpression import ComplexExpression

class TestComplexExpression(unittest.TestCase):
    collection = RulesCollection()

    def setUp(self):
        self.collection.register(ComplexExpression())

    def test_file(self):

        file_name = 'testResources/ansible-smell/complexexpression.yml'
        good_runner = Runner(self.collection, file_name, [], [], [])
        print(good_runner.run())
