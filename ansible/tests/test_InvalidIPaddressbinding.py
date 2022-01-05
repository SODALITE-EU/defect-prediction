from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner

from ansiblelints.rules.InvalidIPaddressbinding import InvalidIPaddressbinding


class TestInvalidIPaddressbinding:

    def test_file(self):
        collection = RulesCollection()
        collection.register(InvalidIPaddressbinding())
        file_name = 'testResources/ansible-smell/invalidIPaddressbinding.yml'
        good_runner = Runner(playbook=file_name, rules=collection)
        result = good_runner.run()
        print(result)
        print(type(result))
        print(len(result))
        assert 0 == len(good_runner.run())
