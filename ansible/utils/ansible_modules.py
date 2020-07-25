from collections import Counter
from itertools import chain

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_ansible_modules(url):
    """ This function returns a dictionary which each key is the name of an ansible module and the value is its description """

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    span_list = soup.find_all('span', class_='std std-ref')
    module_dict = {}
    for span in span_list:
        span_text = span.text
        split_text = span_text.split(' – ', 1)
        key = split_text[0]
        value = split_text[1]
        module_dict[key] = value

    return module_dict


def top10_modules_used(tasks_raw):
    a = pd.Series(np.concatenate(tasks_raw['mod_keys_found']))
    df = a.value_counts().sort_index().rename_axis('x').reset_index(name='frequency')
    df = pd.Series(Counter(chain(*tasks_raw['mod_keys_found']))).sort_index().rename_axis(
        'ansible_modules').reset_index(name='frequency')
    df = df.sort_values(by=['frequency'], ascending=False)
    top10_module_list = df['ansible_modules'].head(10).to_list()

    return top10_module_list, df
