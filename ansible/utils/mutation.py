import logging  # Setting up the loggings to monitor gensim
import os
import os.path
from copy import deepcopy

import pandas as pd
import yaml

from utils.trainutil import mutate_descriptions2, remove_symbols_simple

logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt='%H:%M:%S', level=logging.INFO)


def split_task_name_body(task_dict):
    """This function splits the name from the body for a task"""
    task_name = {}
    task_body = {}

    task_name.update(name=task_dict['name'])
    for key, value in task_dict.items():
        if key != 'name':
            task_body.update([(key, value)])

    return task_name, task_body


def get_tasks(file):
    """Heuristic method to find tasks within a yml/yaml file"""
    value_object_list = []
    name_found_list = []
    for element in file:
        if isinstance(element, dict):
            if 'name' in element:
                if 'tasks' in element:
                    tasks_list = element['tasks']
                    flag = False
                    if tasks_list:
                        for el in tasks_list:
                            if 'name' in el:
                                flag = True
                                name_found_list.append(el)
                    if not flag:
                        name_found_list.append(element)
                else:
                    name_found_list.append(element)
            else:
                for key, value in element.items():
                    if isinstance(value, list):
                        if value:
                            for val in value:
                                if isinstance(val, dict):
                                    if 'name' in val:
                                        name_found_list.append(val)

    return name_found_list


def create_name_body_df_file(task_list, df_tasks):
    """This function creates the dataframe which contains the name and the body for each task"""
    for task in task_list:
        body_list = []
        name, body = split_task_name_body(task)
        body_list.append(body)
        df_tasks = pd.concat(
            [df_tasks, pd.DataFrame({'task_name': name['name'], 'method_description': body_list}, index=[0])],
            ignore_index=True)

    return df_tasks


def process_tasks(file):
    tasks_df = pd.DataFrame(columns=['task_name', 'method_description'])

    content = check_file(file)

    # avoid error throwing for empty files
    if content:  # type(content) is list:
        found_tasks = get_tasks(content)
        if found_tasks:
            tasks_df = create_name_body_df_file(found_tasks, tasks_df)

    return tasks_df


def check_file(file):
    """This method reads the yml/yaml file"""
    if os.stat(file).st_size != 0:
        try:
            with open(file) as f:
                docs = yaml.load_all(f, Loader=yaml.FullLoader)
                for doc in docs:
                    content = doc
                    return content
        except:
            print('Except: ', file)
            return []
    else:
        a = []
        return a


def one_string(col):
    a = ' '.join(col)
    return a


def correct_first_token_name(seq):
    seq[0] = 'TaskDescription'
    return seq


def correct_first_token_name2(seq):
    seq.insert(0, 'AnsibleTask')
    return seq


def mutate(mapped10_ast_token):
    m10 = deepcopy(mapped10_ast_token)
    m20 = deepcopy(m10)
    m20 = m20.reset_index(drop=True)
    m20['consistent'] = False
    m20['mutated_third_tokens'] = m20['third_tokens'].apply(lambda x: mutate_descriptions2(x, m20))
    m20 = m20.drop(columns=['third_tokens'])
    m20 = m20.rename(columns={'mutated_third_tokens': 'third_tokens'})
    m10['consistent'] = True
    merged = pd.concat([m10, m20], ignore_index=True)
    merged['token_task_names'] = merged['token_task_names'].apply(lambda x: remove_symbols_simple(x))
    merged['third_tokens'] = merged['third_tokens'].apply(lambda x: remove_symbols_simple(x))
    merged.head()
    m = deepcopy(merged)
    m['token_task_names'] = m['token_task_names'].apply(lambda x: ['TaskName'] + x)
    mm = deepcopy(m)
    mm['third_tokens'] = mm['third_tokens'].apply(lambda x: correct_first_token_name(x))
    merged2 = deepcopy(mm)
    merged2['task_com'] = merged2['token_task_names'] + merged2['third_tokens']
    merged2['task_complete'] = merged2['task_com'].apply(lambda x: correct_first_token_name2(x))
    return merged2
