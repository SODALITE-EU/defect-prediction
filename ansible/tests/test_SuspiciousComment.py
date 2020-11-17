import unittest

from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner

from ansiblelints.rules.SuspiciousComment import SuspiciousComment


class TestSuspiciousComment(unittest.TestCase):

    def test_file(self):
        collection = RulesCollection()
        collection.register(SuspiciousComment())
        file_name = str('testResources/ansible-smell/suspiciouscomment.yml')
        good_runner = Runner(collection, file_name, [], [], [])
        for item in good_runner.run():
            print(item)
