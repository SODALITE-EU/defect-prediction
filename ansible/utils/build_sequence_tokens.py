from anytree import PreOrderIter
from nltk import word_tokenize
from treelib import Node


def is_empty(params):
    flag = False
    if params:
        flag = True
    return flag


def build_ast(parent, task):
    root = Node(parent)

    for key in list(task.keys()):
        node_key = Node(key, parent=root)
        value_element = task[key]
        Node(value_element, parent=node_key)

    return root


def check_for_nested(node_list):
    for node in node_list:
        if isinstance(node, dict):
            index = node_list.index(node)
            index_parent = index - 1
            parent = node_list[index_parent]
            nested = build_ast(parent, node)
            nested_list = [node.name for node in PreOrderIter(nested)]
            nested_list.pop(0)
            node_list[index] = nested_list

    return node_list


def return_tokens(task):
    r = 'AnsibleTask'
    root = build_ast(r, task)
    all_nodes = [node.name for node in PreOrderIter(root)]
    nodes = check_for_nested(all_nodes)

    return nodes


def convert_int_bool_to_str(node_list):
    for node in node_list:
        if (isinstance(node, int)) or (isinstance(node, bool)) or (node == None):
            index = node_list.index(node)
            new_str = str(node)
            node_list[index] = new_str

    return node_list


def rem_nested_lists(node_list):
    for node in node_list:
        if isinstance(node, list):
            index = node_list.index(node)

            joined_string = ",".join(map(str, node))
            node_list[index] = joined_string

    return node_list


def tokenize_task(node_list):
    for node in node_list:
        index = node_list.index(node)
        new_node = word_tokenize(node)
        node_list[index] = new_node

    return node_list


def tokenize_name(task_name):
    seq = [word_tokenize(token) for token in task_name]

    return seq
