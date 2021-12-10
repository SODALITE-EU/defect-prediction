from jinja2 import Environment, FileSystemLoader

from ansible_module_documentation import load_module_parameter_docs
from misconftypes.ip_type import gen_rule_ip_type
from misconftypes.octal_type import gen_rule_octal_type


def generate_linter_rules():
    env = Environment(loader=FileSystemLoader('templates'))
    df_module_level_texts, df_parameter_level_texts = load_module_parameter_docs()
    gen_rule_octal_type(df_parameter_level_texts.copy(), env)
    gen_rule_ip_type(df_parameter_level_texts.copy(), env)
