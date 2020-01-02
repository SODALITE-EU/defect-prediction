import unittest
from ansiblelint import RulesCollection, Runner
from ansiblelintsoda.rules.SuspiciousComment import SuspiciousComment

class TestSuspiciousComment(unittest.TestCase):
    collection = RulesCollection()

    def setUp(self):
        self.collection.register(SuspiciousComment())


    def test_file(self):

        file_name = str('/home/nima/PycharmProjects/sodalite/tests/ansible-smell/suspiciouscomment.yml')
        good_runner = Runner(self.collection, file_name, [], [], [])
        for item in good_runner.run():
            print(item)
