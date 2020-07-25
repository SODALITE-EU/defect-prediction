import os
import os.path

import pandas as pd
import yaml


class find_tasks:
    """This class contains the methods for finding tasks and separating task declaration from implementation"""

    def __init__(self, root_directory, base_directory):

        self.root = root_directory
        self.base = base_directory

    def get_iacfiles(self, reponame):
        """This function returns a list of all .yml and .yaml found in the repository"""
        files_list = []
        for dirpath, dirnames, filenames in os.walk(reponame):
            for filename in [f for f in filenames if f.endswith(tuple(['.yml', '.yaml']))]:
                fullpath = os.path.join(dirpath, filename)
                fullpath = fullpath.replace('\\', '/')
                fullpath = fullpath.replace('.', '', 1)
                files_list.append(fullpath)

        return files_list

    def get_repo_name(self, base_path, full_path):
        """This functions returns the name of the repository"""
        temp = full_path.replace(base_path, '')
        repo_title = temp.split('/')[0]

        return repo_title

    def get_file_name(self, base_path, full_path):
        """This functions returns the name of the file"""
        temp = full_path.replace(base_path, '')
        file_title = temp.rsplit('/', 1)[1]

        return file_title

    def is_in_roles(self, path):
        """This function checks whether the file is under tasks or roles directory"""
        flag = False
        path_keys = ['/roles/', '/tasks/']
        if any(key in path for key in path_keys):
            flag = True

        return flag

    def split_task_name_body(self, task_dict):
        """This function splits the name from the body for a task"""
        task_name = {}
        task_body = {}

        task_name.update(name=task_dict['name'])
        for key, value in task_dict.items():
            if key != 'name':
                task_body.update([(key, value)])

        return task_name, task_body

    def get_tasks(self, file):
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

    def create_name_body_df(self, task_list, name_file, name_repo, isroles, df_tasks):
        """This function creates the dataframe which contains the name and the body for each task"""
        for task in task_list:
            body_list = []
            name, body = self.split_task_name_body(task)
            body_list.append(body)
            df_tasks = pd.concat([df_tasks, pd.DataFrame({'task_name': name['name'], 'method_description': body_list,
                                                          'file_name': name_file, 'repo_name': name_repo,
                                                          'is_roles': isroles}, index=[0])],
                                 ignore_index=True)

        return df_tasks

    def check_file(self, file):
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

    def search_tasks(self, path_base, iac_path):
        """This method searches for tasks in a yml/yaml file"""
        file_name = self.get_file_name(path_base, iac_path)
        repo_name = self.get_repo_name(path_base, iac_path)
        is_roles = self.is_in_roles(iac_path)

        tasks_df = pd.DataFrame(columns=['task_name', 'method_description', 'file_name', 'repo_name', 'is_roles'])

        content = self.check_file(iac_path)

        # avoid error throwing for empty files
        if content:  # type(content) is list:
            found_tasks = self.get_tasks(content)
            if found_tasks:
                tasks_df = self.create_name_body_df(found_tasks, file_name, repo_name, is_roles, tasks_df)

        return tasks_df

    def tasks_per_repo(self, list_of_files):
        """This method constructs the table which contains the based on the list of files in the repository"""
        tasks_from_files = pd.DataFrame()
        for example in list_of_files:
            file_tasks = self.search_tasks(self.base, self.root + example)
            tasks_from_files = tasks_from_files.append(file_tasks, ignore_index=True, sort=False)

        return tasks_from_files

    def process_repos_for_tasks(self, repo_list):
        """The method to be called to provide the final result table with the found tasks """
        all_tasks = pd.DataFrame()
        sum_of_files = 0
        for repo in repo_list:
            pathforfiles = ('./repos/' + repo)
            iac_files = self.get_iacfiles(pathforfiles)
            sum_of_files += len(iac_files)
            tasks_df = self.tasks_per_repo(iac_files)
            all_tasks = pd.concat([all_tasks, tasks_df])

        return all_tasks, sum_of_files
