import nltk

from utils.ansible_ast import build_ast
from utils.module_doc import match_tasks_doc
from utils.mutation import process_tasks, finalize_tokenization
from utils.w2c_cnn import predict

nltk.download('punkt')

tasks_df = process_tasks("C:\\Postdoc\\projects\\sodalite-eu"
                         "\\defect-prediction\\ansible\\testResources\\ansible-smell\\httpwithouttls.yml")
tasks_mapped_module_parameters = match_tasks_doc(tasks_df)
m10 = build_ast(tasks_mapped_module_parameters)
tokenized_df = finalize_tokenization(m10)
print(tokenized_df)
print(tokenized_df.columns)
# with open('data\\mutated.pkl', 'rb') as input_file:
#     mutated = pickle.load(input_file)

# with open('data\\mutated_valid.pkl', 'rb') as input_file:
#     testdata = pickle.load(input_file)
#
# # mutated_selected = mutated[['task_name', 'task_complete', 'mod_keys_found_string', 'consistent']]
# # print(mutated_selected.columns)
# # print(mutated_selected)
# # print(train(mutated_selected))
#
# # testdata = testdata[testdata['mod_keys_found_string'] == 'shell']
# testdata = testdata[['task_name', 'task_complete', 'mod_keys_found_string']]
# train_set, val_set, test_set = np.split(testdata.sample(frac=1), [int(.6 * len(testdata)), int(.8 * len(testdata))])
#
# dfa = test_set.copy()
# test_set2 = dfa[['task_name']]
#
# arr = _predict(test_set, 'shell')
# y_classes = arr.argmax(axis=-1)
#
# test_set2['consistent'] = y_classes.tolist()
# # print(test_set2)
# test_set2['consistent'] = test_set2['consistent'].apply(lambda x: True if x==1 else False)
# print(df.columns)
# print(test_set2)
# print(test_set2.to_json(orient='records'))
# print(predict(test_set))
tokenized_df = tokenized_df[['task_name', 'task_complete', 'mod_keys_found_string']]
print(predict(tokenized_df))
