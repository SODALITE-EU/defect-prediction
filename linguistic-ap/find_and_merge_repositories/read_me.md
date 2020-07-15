# Ansible Repositories Search

Files:

  - A python file check_repository.py
  - 3 jupyter notebooks
  - 7 pickle files
 
Elaboration:
  - check_repository.py contains the code that can check if repository satisfies the criteria.
  - git.ipynb is the notebook in which we construct three initial lists which contain ansible repositories. Using Github API we use 2 methods to identify Ansible repositories. The results lists are saved into 3 pickle files namely: yml_repos.pkl, yaml_repos.pkl, ansible_repos.pkl
  - test_class.ipynb is the notebook in which we check every repository list created in git.ipynb in order to explore how many repositories satisfy the criteria, The result lists are saved in three pickle files namely: passed_repos_yaml.pkl, passed_respos_yml.pkl, passed_repos_ansible.pkl
  - In merge final repos.ipynb we merge the result lists from test_class.ipynb. In addition we make sure each element in the final list is unique. The final repository list is saved in the final_merged_repos.pkl pickle file.
