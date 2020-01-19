import unittest
from ansiblelint import RulesCollection, Runner
from ansiblelints.stage.DuplicateEntity import DuplicateEntity
import collections

class TestDuplicateEntity(unittest.TestCase):
    collection = RulesCollection()

    def setUp(self):
        self.collection.register(DuplicateEntity())

    def test_file(self):
        file_name = 'testResources/ansible-smell/hardcodepassword5.yml'
        good_runner = Runner(self.collection, file_name, [], [], [])

        name_list=[]
        for item in good_runner.run():
            name_list.append(str(item).split('matched')[0])

        if len(name_list) != 0:
            print([item for item,count in collections.Counter(name_list).items() if count >1])


