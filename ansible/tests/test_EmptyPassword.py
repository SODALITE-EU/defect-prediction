from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner

from ansiblelints.rules.EmptyPassword0 import EmptyPassword0


class TestEmptyPassword:

    def test_file(self):
        collection = RulesCollection()
        collection.register(EmptyPassword0())
        success = 'testResources/ansible-smell/adminbydefault.yml'
        good_runner = Runner(collection, success, [], [], [])
        print(good_runner.run())
        print(len(good_runner.run()))
        assert 0 == len(good_runner.run())
