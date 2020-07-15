import pandas as pd
import numpy as np
import pickle

def pick_random_method(task_df):
    
    task = task_df.sample(n=1)
    task_descr = ' '.join(task.loc[task.index[0],'third_tokens'])
    task_tuple = (task.index[0],task_descr)
    
    return task_tuple

def drop_same(similars,id):
    for elem in similars:
        if elem[0] == id:
            similars.remove(elem)
    
    return similars        

def get_tasks_from_simlist(similar_list,tasks_df):
    
    name_list = []
    for elem in similar_list:
        row_id = elem[0]
        task_name = ' '.join(tasks_df.loc[row_id,'token_task_names'])
        name_list.append(task_name)
        
    return name_list

def find_task_names_by_id(similar_list,tagged_names):
    
    name_list = []
    for elem in similar_list:
        row_id = elem[0]
        task_name = tagged_names[row_id].words
        name_list.append((task_name,row_id))
        
    return name_list    

def find_similar_names(similar_task_names,model_names):
    
    similar_of_similars = []
    for elem,row_id in similar_task_names:
        elem_similars = model_names.docvecs.most_similar(positive=[model_names.infer_vector(elem)],topn=11)
        elem_sims = drop_same(elem_similars,row_id)
        similar_of_similars.append((elem_sims,row_id))
    
    return similar_of_similars    

def check_random_found(rand_id,similar_names):
    
    found = ''
    for tup in similar_names:
        # found = False
        lst = tup[0]
        index = similar_names.index(tup)
        for tup2 in lst:
            found = False
            if tup2[0] == rand_id:
                found = True
                acc = tup2[1]
                print('The randomly selected element was found at the '+str(index)+ ' position with accuracy' + str(round(acc,2)))

remove_list = [',', '``','"',"''",'==','{','}','(',"'",'[',']',"'==",')','>','=','-','|','/','+','$','.+',':','!',
               '--','\\','?','@',';','&','#','^','<','*','%','.','=~','{{','}}',]

def remove_symbols_simple(sequence):

    for item in sequence:
        if item in remove_list:
            sequence.remove(item)

    return sequence

def mutate_descriptions_old(method, tasks_df):
    
    """ This method mutates the methods descriptions column. It replaces the implementation of the ansible module by randomly selecting another """
    
    module_used = method[1]
    filtered_df = tasks_df[tasks_df['mod_keys_found_string'] != module_used]
    random_method = filtered_df.sample(n=1)['third_tokens'].tolist()[0][1:]
    new_method = method[:1]
    new_method +=  random_method    
    
    return new_method    

def mutate_descriptions2(method, tasks_df):
    
    """ This method mutates the methods descriptions column. It replaces the implementation of the ansible module by randomly selecting another """
    
    module_list = list(tasks_df['mod_keys_found_string'].unique())
    module_used = list(set(module_list) & set(method))[0]
    # print(module_used)
    filtered_df = tasks_df[tasks_df['mod_keys_found_string'] == module_used]
    random_method = filtered_df.sample(n=1)['third_tokens'].tolist()[0][1:]
    new_method = method[:1]
    new_method +=  random_method    
    
    return new_method    

     