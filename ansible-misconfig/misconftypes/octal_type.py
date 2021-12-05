import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")

from ansible_module_documentation import scrap_module_info, list_top_modules

module_documentation = scrap_module_info(list_top_modules)
df_module_documentation = module_documentation[0]
all_available_modules = module_documentation[1]

df_module_documentation['Module_Name'].nunique()

synopsis = df_module_documentation.explode('Synopsis')[
    ['Collection_Name', 'Module_Name', 'Module_Link', 'Synopsis']].drop_duplicates().dropna()
synopsis.columns = ['Collection_Name', 'Module_Name', 'Module_Link', 'Text']
synopsis['section'] = 'synopsis'
notes = df_module_documentation.explode('Notes')[
    ['Collection_Name', 'Module_Name', 'Module_Link', 'Notes']].drop_duplicates().dropna()
notes.columns = ['Collection_Name', 'Module_Name', 'Module_Link', 'Text']
notes['section'] = 'notes'
df_module_level_texts = pd.concat([synopsis, notes])

df_module_level_texts.to_excel(
    'files/module_level.xlsx')
# df_parameter_level_texts.to_excel('files/parameter_level.xlsx')

df_module_level_texts = pd.read_excel(
    'files/module_level.xlsx')
df_parameter_level_texts = pd.read_excel(
    'files/parameter_level.xlsx')

df_parameter_level_texts = df_parameter_level_texts.dropna(how='all')
df_module_level_texts = df_module_level_texts.dropna(how='all')


def check_access_keys(yaml_code, tag):
    shortdesc = 'Playbook May Contain Credentials'
    description = 'Credentials should not be included in variables, especially if they are stored publically'
    line = yaml_code
    line = line[line.find('var:'):]
    if tag + ':' in line.split(' '):
        return shortdesc
    if tag + ':' in line.split(' '):
        return shortdesc
    return 'No Misconfiguration'


yaml_code = """- hosts: all
tasks:
   - name: AWS Creds
     var:
      aws_secret_access_key: AKIAJL123456789qazw"""

check_access_keys(yaml_code, tag='aws_secret_access_key')


def check_similarity(module_documentation, ref_text):
    doc1 = nlp(module_documentation)
    doc2 = nlp(ref_text)
    similarity_score = doc1.similarity(doc2)
    if (similarity_score > 0.95):
        print(module_documentation)


df_parameter_level_texts['Description'].apply(check_similarity,
                                              ref_text="""You must either add a leading zero so that Ansible's YAML parser knows it is an octal number or quote it so Ansible receives a string and can do its own conversion from string into number.""")
