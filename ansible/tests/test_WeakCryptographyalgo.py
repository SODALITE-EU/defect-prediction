from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner
import unittest
from ansiblelints.rules.WeakCryptographyalgo import WeakCryptographyalgo


class TestWeakCryptographyalgo(unittest.TestCase):

    def test_file(self):
        collection = RulesCollection()
        collection.register(WeakCryptographyalgo())
        file_name = str('testResources/ansible-smell/weakcryptographyalgo.yml')
        good_runner = Runner(playbook=file_name, rules=collection)
        print(good_runner.run())
