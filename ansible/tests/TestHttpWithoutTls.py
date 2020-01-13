import unittest
from ansiblelint import RulesCollection, Runner
from ansiblelints.rules.HttpWithoutTls import HttpWithoutTls

class TestHttpWithoutTls(unittest.TestCase):
    collection = RulesCollection()

    def setUp(self):
        self.collection.register(HttpWithoutTls())

    def test_file(self):
        success = 'testResources/ansible-smell/httpwithouttls2.yml'
        good_runner = Runner(self.collection, success, [], [], [])
        print(good_runner.run())
        #print(type(good_runner.run()))
        #print(len(good_runner.run()))
        #self.assertGreaterEqual(1, len(good_runner.run()))
