from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner

from ansiblelints.rules.HardCodePassword import HardCodePassword


class TestHardCodePassword:

    def test_file(self):
        collection = RulesCollection()
        collection.register(HardCodePassword())
        success = 'testResources/ansible-smell/hardcodepassword.yml'
        good_runner = Runner(collection, success, [], [], [])
        print(good_runner.run())
        print(type(good_runner.run()))
        print(len(good_runner.run()))
        assert 0 == len(good_runner.run())
