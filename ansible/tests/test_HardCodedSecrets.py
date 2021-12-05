from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner

from ansiblelints.rules.HardCodedSecrets import HardCodedSecrets


class TestAdminByDefault:

    def test_file(self):
        collection = RulesCollection()
        collection.register(HardCodedSecrets())
        file_name = 'testResources/ansible-smell/create.yml'
        good_runner = Runner(file_name, rules=collection)
        # print(good_runner.run())
        assert 1 == len(good_runner.run())
