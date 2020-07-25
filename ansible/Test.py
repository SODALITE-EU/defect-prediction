import pickle

import numpy as np

# tasks_df = process_tasks("C:\\Postdoc\\projects\\learing\\restdefect\\testResources\\adminbydefault.yml")
from utils.w2c_cnn import _predict

# with open('data\\mutated.pkl', 'rb') as input_file:
#     mutated = pickle.load(input_file)

with open('data\\mutated_valid.pkl', 'rb') as input_file:
    testdata = pickle.load(input_file)

# mutated_selected = mutated[['task_name', 'task_complete', 'mod_keys_found_string', 'consistent']]
# print(mutated_selected.columns)
# print(mutated_selected)
# print(train(mutated_selected))

testdata = testdata[testdata['mod_keys_found_string'] == 'shell']
testdata = testdata[['task_name', 'task_complete', 'mod_keys_found_string', 'consistent']]
train_set, val_set, test_set = np.split(testdata.sample(frac=1), [int(.6 * len(testdata)), int(.8 * len(testdata))])

dfa = test_set.copy()
test_set2 = dfa[['task_name']]

arr = _predict(test_set, 'shell')
y_classes = arr.argmax(axis=-1)

test_set2['consistent'] = y_classes.tolist()
# print(test_set2)
test_set2['consistent'] = test_set2['consistent'].apply(lambda x: True if x==1 else False)
# print(df.columns)
# print(test_set2)
print(test_set2.to_json(orient='records'))

