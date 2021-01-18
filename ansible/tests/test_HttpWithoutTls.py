from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner

from ansiblelints.rules.HttpWithoutTls import HttpWithoutTls


class TestHttpWithoutTls:

    def test_file(self):
        collection = RulesCollection()
        collection.register(HttpWithoutTls())
        success = 'testResources/ansible-smell/httpwithouttls2.yml'
        good_runner = Runner(collection, success, [], [], [])
        print(good_runner.run())