from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner

from ansiblelints.rules.ComplexExpression import ComplexExpression
import unittest

class TestComplexExpression(unittest.TestCase):

    def test_file(self):
        collection = RulesCollection()
        collection.register(ComplexExpression())
        file_name = 'testResources/ansible-smell/complexexpression.yml'
        good_runner = Runner(playbook=file_name, rules=collection)
        print(good_runner.run())
