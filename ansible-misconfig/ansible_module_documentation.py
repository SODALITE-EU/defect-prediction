import pandas as pd
import requests
import spacy
from bs4 import BeautifulSoup

nlp = spacy.load("en_core_web_sm")

# Reference - https://mike42.me/blog/2019-01-the-top-100-ansible-modules
list_top_modules = ['file', 'include', 'template', 'command', 'service', 'shell',
                    'set_fact', 'apt', 'lineinfile', 'copy', 'yum', 'assert',
                    'include_tasks', 'stat', 'package', 'get_url', 'debug',
                    'import_tasks', 'include_vars', 'apt_repository', 'user', 'fail',
                    'unarchive', 'apt_key', 'pip', 'systemd', 'action', 'git', 'uri',
                    'group', 'sysctl', 'raw', 'mysql_user', 'meta', 'replace',
                    'ini_file', 'find', 'local_action', 'mysql_db', 'cron', 'wait_for',
                    'rpm_key', 'include_role', 'yum_repository', 'mount',
                    'blockinfile', 'firewalld', 'ufw', 'authorized_key',
                    'docker_container', 'dnf', 'seboolean', 'homebrew', 'fetch', 'npm',
                    'osx_defaults', 'postgresql_user', 'pkgng', 'pause', 'script',
                    'setup', 'postgresql_db', 'mysql_replication', 'win_regedit',
                    'pacman', 'debconf', 'slurp', 'gem', 'iptables', 'apache2_module',
                    'synchronize', 'docker', 'alternatives', 'selinux', 'oc_obj',
                    'make', 'win_shell', 'modprobe', 'hostname', 'zypper', 'xml',
                    'supervisorctl', 'win_file', 'homebrew_cask', 'add_host',
                    'rabbitmq_user', 'pamd', 'win_command', 'assemble', 'htpasswd',
                    'apk', 'openbsd_pkg', 'win_get_url', 'win_chocolatey',
                    'docker_image', 'tempfile', 'locale_gen', 'easy_install',
                    'django_manage', 'composer']


def scrap_module_info(modules_list):
    list_all_modules = []
    path_module_documentation = 'https://docs.ansible.com/ansible/latest/collections/'
    req = requests.get(path_module_documentation)
    soup = BeautifulSoup(req.content, 'html.parser')
    all_collection_list = soup.find_all("ul", class_="simple")
    top_module_dataframe = []
    for each_list in all_collection_list:
        for each_reference_link in each_list.find_all('li'):
            link_to_collection = 'https://docs.ansible.com/ansible/latest/collections/' + each_reference_link.find(
                'a').get('href')
            name_collection = each_reference_link.find('a').text
            req_collection = requests.get(link_to_collection)
            soup_collection = BeautifulSoup(req_collection.content, 'html.parser')
            soup_coll_modules = soup_collection.find("div", {"id": "modules"})
            if (soup_coll_modules):
                ul_module = soup_coll_modules.find_all('ul', class_='simple')
                for each_ul in ul_module:
                    for each_link_li in each_ul.find_all('li'):
                        name_module = each_link_li.find('a').text
                        list_all_modules.append(name_module)
                        if (name_module in modules_list):
                            # print(name_module)
                            link_to_module = (link_to_collection.split('#')[0].replace('index.html', '') + (
                                each_link_li.find('a').get('href').split('#')[0]))
                            # print(link_to_module)
                            req_module = requests.get(link_to_module)
                            soup_each_module = BeautifulSoup(req_module.content, 'html.parser')
                            synopsis_list = soup_each_module.find("div", {"id": "synopsis"})
                            if (synopsis_list != None):
                                synopsis_list = synopsis_list.find_all('li')
                                synopsis_text = []
                                for each_syn in synopsis_list:
                                    synopsis_text.append(each_syn.text)
                            else:
                                synopsis_text = None
                            notes_list = soup_each_module.find("div", {"id": "notes"})
                            if (notes_list != None):
                                notes_list = notes_list.find_all('li')
                                notes_text = []
                                for each_note in notes_list:
                                    notes_text.append(each_note.text)
                            else:
                                notes_text = None
                            parameters = soup_each_module.find("div", {"id": "parameters"})
                            if (parameters):
                                rows = parameters.findAll('tr')
                                for tr in rows:
                                    each_parameter_detail = []
                                    x = 0
                                    cols = tr.findAll('td')
                                    for td in cols:
                                        x = x + 1
                                        list_str = td.text.strip().split('\n')
                                        list_str = filter(None, list_str)
                                        list_str = list(list_str)
                                        each_parameter_detail.append(list_str)
                                    if (len(each_parameter_detail) > 0):
                                        if (len(each_parameter_detail[0]) > 0):
                                            name_param = each_parameter_detail[0][0]
                                            datatype_param = each_parameter_detail[0][1]
                                            choices_default = each_parameter_detail[1]
                                            choices = None
                                            default = None
                                            choices_clean = []
                                            if (len(choices_default) > 0):
                                                if (choices_default[0] == 'Choices:'):
                                                    choices = choices_default[1:]
                                                    for each_choice in choices:
                                                        choices_clean.append(each_choice.split('\xa0←')[0])
                                                        if (each_choice[-1] == '←'):
                                                            default = each_choice.split('\xa0←')[0]
                                                else:
                                                    default = choices_default[0].split(':')[1]
                                            desc_param = each_parameter_detail[2]
                                            top_module_dataframe.append(
                                                [name_param, datatype_param, choices_clean, default, desc_param,
                                                 name_module, link_to_module, name_collection, synopsis_text,
                                                 notes_text])
                            # top_module_dataframe.append([name_module,link_to_module,name_collection,synopsis_text,notes_text,parameter_list])
    top_module_df = pd.DataFrame(top_module_dataframe)
    top_module_df.columns = ['Parameter_Name', 'Datatype_Param', 'Choices', 'Default', 'Description', 'Module_Name',
                             'Module_Link', 'Collection_Name', 'Synopsis', 'Notes']
    return ([top_module_df, list_all_modules])
