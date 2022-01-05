import unittest

from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner

from ansiblelints.rules.EmptyPassword0 import EmptyPassword0


class TestEmptyPassword(unittest.TestCase):

    def test_file(self):
        collection = RulesCollection()
        collection.register(EmptyPassword0())
        file_name = 'testResources/ansible-smell/adminbydefault.yml'
        good_runner = Runner(playbook=file_name, rules=collection)
        print(good_runner.run())
        print(len(good_runner.run()))
        assert 0 == len(good_runner.run())
