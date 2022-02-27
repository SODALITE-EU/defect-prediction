import unittest

from ansiblelint.rules import RulesCollection

from ansible_module_documentation import scrap_module_info


class TestLongStatement(unittest.TestCase):
    collection = RulesCollection()

    # def setUp(self):
    #     self.collection.register(LongStatement())

    def test_file(self):
        top_module_df, list_all_modules = scrap_module_info(modules_list=['copy'])
        assert top_module_df is not None
        assert list_all_modules is not None

        # file_name = 'testResources/ansible-smell/many.yaml'
        # good_runner = Runner(file_name, rules=self.collection)
        #
        # print(good_runner.run())
