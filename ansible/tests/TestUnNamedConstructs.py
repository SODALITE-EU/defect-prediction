import unittest

from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner

from ansiblelints.stage.UnNamedConstructs import UnNamedConstructs


class TestUnNamedConstruct(unittest.TestCase):
    collection = RulesCollection()

    def setUp(self):
        self.collection.register(UnNamedConstructs())

    def test_file(self):
        file_name = 'testResources/ansible-smell/unnamedconstructs.yml'
        good_runner = Runner(playbook=file_name, rules=self.collection)
        print(good_runner.run())
