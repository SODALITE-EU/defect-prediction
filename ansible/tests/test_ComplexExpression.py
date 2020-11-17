import pytest

from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner

from ansiblelints.rules.ComplexExpression import ComplexExpression


class TestComplexExpression:

    def test_file(self):
        collection = RulesCollection()
        collection.register(ComplexExpression())
        file_name = 'testResources/ansible-smell/complexexpression.yml'
        good_runner = Runner(collection, file_name, [], [], [])
        print(good_runner.run())
