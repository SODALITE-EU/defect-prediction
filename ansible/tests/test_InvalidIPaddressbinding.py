from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner

from ansiblelints.rules.InvalidIPaddressbinding import InvalidIPaddressbinding


class TestInvalidIPaddressbinding:

    def test_file(self):
        collection = RulesCollection()
        collection.register(InvalidIPaddressbinding())
        success = 'testResources/ansible-smell/invalidIPaddressbinding.yml'
        good_runner = Runner(collection, success, [], [], [])
        result = good_runner.run()
        print(result)
        print(type(result))
        print(len(result))
        assert 1 == len(good_runner.run())
