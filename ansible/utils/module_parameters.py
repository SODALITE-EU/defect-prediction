import re

import requests
from bs4 import BeautifulSoup


def remove_tags(text):
    """ This function is used to remove html tags from python string """

    TAG_RE = re.compile(r'<[^>]+>')
    t = TAG_RE.sub('', text)
    return t.replace('\n', '')


def get_parameters(url):
    """ This function returns the parameters given a ansible module url """

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find_all('table', class_='documentation-table')[0]
    params = {}
    # params_text = {}
    for row in table.find_all('tr'):
        td_tags = row.find_all('td', colspan=1)
        for tag in td_tags:
            required = ''
            param_name = tag.find('b').getText()
            param_type = tag.find('span', attrs={'style': 'color: purple'}).getText()
            if tag.find('span', attrs={'style': 'color: red'}):
                required = tag.find('span', attrs={'style': 'color: red'}).getText()
            if required:
                # param_required = param_name+'_'+required
                params[param_name + '_required'] = True
            else:
                params[param_name + '_required'] = False

            params[param_name] = param_type

            # add parameter descriptions
            td3_tags = row.find_all('td')
            for td3 in td3_tags:
                param_texts = td3.find('div', attrs={'style': None, 'class': None, 'id': None})
                if param_texts:
                    par_text = param_name + '_text'
                    for text in param_texts.find_parents('td'):
                        pure = remove_tags(str(text))
                        params[par_text] = pure

    return params


def get_module_parameters(parameters):
    """ This functions scrapes the information from the ansible documentation website in order to retrieve information from the corresponding parameter list"""

    param_dict = {}
    key2 = ''
    for key in parameters:
        key_url = 'https://docs.ansible.com/ansible/latest/modules/' + key + '_module.html#'

        if '_' in key:
            key2 = key.replace('_', '-')
        key_url += key2 + '-module'

        params = get_parameters(key_url)

        param_dict[key] = params

    return param_dict


def intersection_lists(lst1, lst2):
    """ Return the intersection between two lists """
    return list(set(lst1) & set(lst2))


def add_when(task):
    text = ''
    if 'when' in list(task.keys()):
        when = task['when']
        if isinstance(when, list):
            for key in when:
                text += key + ' '
        else:
            text = when
    else:
        text = ''

    return text


def map_module_used_parameters(task, all_params):
    """ This function retrieves information about module parameters used in a  task given a dictionary of reference """

    keys_task = set(task.keys())
    keys_all_params = set(all_params.keys())
    key_intersection = keys_task & keys_all_params

    intersect_dict = {}

    for key in list(key_intersection):

        value_dict_task = task[key]
        intersect_dict['module_used'] = key

        if isinstance(value_dict_task, dict):

            value_dict_all_params = all_params[key]

            value_dict_task_keys = value_dict_task.keys()
            value_dict_all_params_keys = value_dict_all_params.keys()

            value_keys_interesection = value_dict_task_keys & value_dict_all_params_keys
            intersect_dict['intersected_params'] = list(value_keys_interesection)
            if list(value_keys_interesection):
                for vki in list(value_keys_interesection):
                    required = vki + '_required'
                    text = vki + '_text'
                    intersect_dict[vki] = value_dict_all_params[vki]
                    intersect_dict[required] = value_dict_all_params[required]
                    intersect_dict[text] = value_dict_all_params[text]
            else:

                if isinstance(value_dict_task, dict):
                    for k in list(value_dict_task.keys()):
                        new_key = key + '_' + k
                        intersect_dict[new_key] = value_dict_task[k]
                else:
                    intersect_dict[key] = value_dict_task

        else:
            no_param_value = 'no_param_value'
            intersect_dict['intersected_params'] = []
            intersect_dict[no_param_value] = task

    return intersect_dict
