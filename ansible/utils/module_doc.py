import pickle

from utils.ident_ans_mods import identify_ansible_modules
from utils.module_parameters import get_module_parameters, map_module_used_parameters


def match_tasks_doc(tasks):
    # 'tasks_from_repos.pkl'
    # with open(pkl_file_tasks, 'rb') as input_file:
    #     tasks = pickle.load(input_file)
    descriptions = tasks[['task_name', 'method_description']]
    with open('data\\modules.pkl', 'rb') as input_file:
        mda = pickle.load(input_file)
    df_desc_mod = descriptions.copy()
    df_desc_mod = df_desc_mod.reset_index()
    df_desc_mod = df_desc_mod.rename(columns={'index': 'repo_count'})
    inst = identify_ansible_modules(df_desc_mod, mda)
    df = inst.create_text_cols()
    df = df[df['mod_keys_found'].apply(len).gt(0)]
    tasks_ast_raw = df.reset_index(drop=True)

    with open('data\\top10_list.pkl', 'rb') as input_file:
        top10_module_list = pickle.load(input_file)

    tasks_ast_raw = tasks_ast_raw[
        tasks_ast_raw['mod_keys_found'].apply(lambda v: len(set(v) & set(top10_module_list)) > 0)]

    tasks_10 = tasks_ast_raw.copy()
    two_keys_set = tasks_10[tasks_10['mod_keys_found'].apply(lambda x: len(x) > 1)]
    one_key_set = tasks_10[tasks_10['mod_keys_found'].apply(lambda x: len(x) < 2)]
    one_key_set['mod_keys_found_string'] = one_key_set['mod_keys_found'].apply(lambda x: ''.join(x))
    params_dict = get_module_parameters(top10_module_list)
    # one_key_set = one_key_set.drop(columns=['found_used_parameters'])
    one_key_set['found_used_parameters'] = one_key_set['method_description'].apply(
        lambda x: map_module_used_parameters(x, params_dict))
    return one_key_set
