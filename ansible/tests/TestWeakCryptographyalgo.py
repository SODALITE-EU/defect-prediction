import unittest
from ansiblelint import RulesCollection, Runner
from ansiblelints.rules.WeakCryptographyalgo import WeakCryptographyalgo

class TestWeakCryptographyalgo(unittest.TestCase):
    collection = RulesCollection()

    def setUp(self):
        self.collection.register(WeakCryptographyalgo())

    def test_file(self):

        file_name = str('testResources/ansible-smell/weakcryptographyalgo.yml')
        good_runner = Runner(self.collection, file_name, [], [], [])
        for item in good_runner.run():
            print(item)
