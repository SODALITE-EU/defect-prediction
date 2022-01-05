from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner
import unittest
from ansiblelints.rules.HttpWithoutTls import HttpWithoutTls


class TestHttpWithoutTls(unittest.TestCase):

    def test_file(self):
        collection = RulesCollection()
        collection.register(HttpWithoutTls())
        file_name = 'testResources/ansible-smell/httpwithouttls2.yml'
        good_runner = Runner(playbook=file_name, rules=collection)
        print(good_runner.run())
