from nltk import word_tokenize

from utils.build_sequence_tokens import return_tokens, \
    rem_nested_lists, convert_int_bool_to_str, tokenize_task, is_empty
from utils.pre_process import remove_symbols, flatten_list


def build_ast(tasks_mapped_module_parameters):
    mapped10 = tasks_mapped_module_parameters.copy()
    mapped10['has_params'] = mapped10['found_used_parameters'].apply(lambda x: is_empty(x['intersected_params']))
    mapped10['initial_ast'] = mapped10['method_description'].apply(lambda x: return_tokens(x))
    mapped10['second_ast'] = mapped10['initial_ast'].apply(lambda x: convert_int_bool_to_str(x))
    mapped10['third_ast'] = mapped10['second_ast'].apply(lambda x: rem_nested_lists(x))
    task_name_tokens = [word_tokenize(token) for token in mapped10['task_name']]
    mapped10['first_tokens'] = mapped10['third_ast'].apply(lambda x: tokenize_task(x))
    mapped10 = mapped10.reset_index(drop=True)
    m10 = mapped10.copy()

    m10['second_tokens'] = m10['first_tokens'].apply(lambda x: remove_symbols(x))
    m10['third_tokens'] = m10['second_tokens'].apply(lambda x: flatten_list(x))
    m10['token_task_names'] = task_name_tokens
    m10 = m10.drop(columns=['initial_ast', 'second_ast', 'first_tokens', 'second_tokens'])
    m10['descr_one_string'] = m10['third_tokens'].apply(lambda x: ' '.join(x))
    return m10
