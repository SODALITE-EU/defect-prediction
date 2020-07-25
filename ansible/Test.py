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
df = _predict(test_set, 'shell')
# print(df.columns)
print(df)
