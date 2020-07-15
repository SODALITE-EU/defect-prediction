from github import Github
from pydriller import RepositoryMining
import pandas as pd

def create_commits_table(repo,keywords):
        
        """This functions creates the commits table given the repository and a set of keywords"""
    
        commits_table = pd.DataFrame()
        path = 'https://github.com/'+ repo
        for commit in RepositoryMining(path).traverse_commits():
            
            commit_words = set(commit.msg.split())            
            if commit_words.intersection(keywords) != set([]):
                result = pd.DataFrame({'{}'.format('Repo name') : repo,
                                       '{}'.format('Commit hash') : commit.hash, 
                                       '{}'.format('Commit msg') : commit.msg,
                                       '{}'.format('keywords') : commit_words.intersection(keywords)
                                      },index=[0])
                                     
                commits_table = commits_table.append(result)
        
        commits_table.index = range(len(commits_table))
        return commits_table