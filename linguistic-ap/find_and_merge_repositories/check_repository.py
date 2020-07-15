from github import Github
import pandas as pd
from pydriller import RepositoryMining

class check_repo:

	""" This class contains methods to examine whether a repository fulfils the criteria for selection """
    
    def __init__(self,token,repo_name,iac):
        
        self.g = Github(token)
        self.iac = iac
        self.rep = repo_name
        self.repo = Github(token).get_repo(self.rep)
        self.repo_content = self.repo.get_contents("")
        
    def get_all_files(self,repo_content, repo):
    
        files = []
        while self.repo_content:

            element = self.repo_content.pop(0)
            if element.type == 'dir':            
                self.repo_content.extend(self.repo.get_contents(element.path))
            else:
                files.append(element.path)

        return files
    
    def get_all_file_types(self, files):
    
        file_types = []
        for file in files:
            if '.' in file:
                file_types.append(file[file.find('.'):])
        return file_types
    
    def count_file_types(self,list_file_types,files):
    
        file_dict = {}
        for file_type in list_file_types:

            file_dict.update({file_type : list_file_types.count(file_type)/len(files)})


        return file_dict
    
    def get_percentage(self,file_type, counted_repo_repo_files):
    
        per = 0
        for key in counted_repo_repo_files:
            if key in file_type:
                per = counted_repo_repo_files[key]
        return per
    
    def check_file_percentage(self):
	
		""" This function checks the iac percentage in a repository, if it is higher than 11% returns True """
        
        flag = False

        files = self.get_all_files(self.repo_content,self.repo)

        list_file_types = self.get_all_file_types(files)

        counted_perc_file_types = self.count_file_types(list_file_types,files)

        iac_percentage = self.get_percentage(self.iac, counted_perc_file_types)
        
        if iac_percentage > 0.11:
            flag = True

        return flag
    
    def check_num_contributors(self):
	
		""" This function checks checks the number of contributors in a repository, returns True if there are more than 10 """
    
        flag = False
        contributors = self.repo.get_contributors()
        if contributors.totalCount > 10:
            flag = True

        return flag
    
    def check_commits(self):
	
		""" Checks the number of commits per month, return true if  there are more than 2 commits for every month """
    
        path = 'https://github.com/'+ self.rep
        commits = {}
        flag = False
        for commit in RepositoryMining(path).traverse_commits():
            commits.update({commit.hash:commit.committer_date.strftime('%Y-%m-%d %H:%M:%S')})
        commits_df = pd.DataFrame.from_dict(commits,orient='index')
        commits_df = commits_df.reset_index()
        commits_df = commits_df.rename(columns={'index':'sha',0:'date'})
        commits_df['date'] = pd.to_datetime(commits_df['date'],format='%Y-%m-%d %H:%M:%S')
        commits_df = commits_df.set_index('date')
        new_df = commits_df.groupby(pd.Grouper(freq="M")).agg('count')
        flag = (new_df['sha']>2).any()

        return flag