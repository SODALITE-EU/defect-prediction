import unittest
from ansiblelint import RulesCollection, Runner

class TestIncompleteConstructs(unittest.TestCase):
    collection = RulesCollection()

    def setUp(self):
        self.collection.register(IncompleteConstructs())

    #def test_file_positive(self):
    #   success = 'tests/Incomplete-Constructs-success.yml'
    #   good_runner = Runner(self.collection, success, [],[],[])
    #   self.assertEqual([],good_runner.run())

    def test_file_negative(self):
        failure = 'tests/Incomplete-Constructs-failure.yml'
        bad_runner = Runner(self.collection, failure, [],[],[])
        errs = bad_runner.run()
        self.assertEqual(1, len(errs))