import pandas as pd
import numpy as np


class identify_ansible_modules:

    """ This class is responsible for providing the context of actions for a set of ansible tasks based on the documentation"""
    
    def __init__(self,df,modules):
        
        self.df = df
        self.modules = modules
        self.mod_keys = list(modules.keys())

    def check_keys_in_modules(self,keys,modules_keys):
    
        """ This functions checks where the keys of method descriptions are part of the ansible official documentation """

        keys_in_mods = []
        for key in keys:
            if key in modules_keys:
                keys_in_mods.append(key)

        return keys_in_mods

    def check_values_in_modules(self,values,modules_keys):
    
        """ This function checks whether values contain keys that are part of official ansible documentation """

        keys_in_mods = []
        for value in values:
            if isinstance(value, dict):
                value_keys = list(value.keys())
                for key in value_keys:
                    if key in modules_keys:
                        keys_in_mods.append(key)

        return keys_in_mods

    def replace_empty_lists(self,values):
    
        """ This functions replaces empty lists found in values for the text found in key 'name' within the value, if it is found """

        names_in_mods = []
        for value in values:
            if isinstance(value, dict):
                value_keys = list(value.keys())
                for key in value_keys:
                    if key == 'name':
                        names_in_mods.append(value[key])

        return names_in_mods

    def search_ansible_modules(self,df,modules):
    
        """ This function checks for each task the keys of the method description and saves in another column the keys that are found to be part of ansible official documentation.
              In addition it checks the values in the same fashion. 
        """
        
        for idx, content in self.df['method_description'].iteritems():

            keys = list(content.keys())
            values = [*content.values()]
            found_modules_keys = self.check_keys_in_modules(keys,self.mod_keys)
            found_modules_values = self.check_values_in_modules(values,self.mod_keys)

            self.df.at[idx,'mod_keys_found'] = found_modules_keys
            self.df.at[idx,'mod_values_found'] = found_modules_values

            if self.df.at[idx,'mod_values_found'] == []:
                self.df.at[idx,'mod_values_found'] = self.replace_empty_lists(values)

        return df

    def create_key_module_column(self,df,modules):
    
        """ This function returns for every key found that is part of ansible documentation the respective description of it """

        for idx, content in self.df['mod_keys_found'].iteritems():
            for key in content:
                text = self.modules[key]
                if self.df.at[idx,'key_module_text'] == '':
                    self.df.at[idx,'key_module_text'] = text
                else:
                    self.df.at[idx,'key_module_text'] += '__' +text
        return df

    def create_value_module_column(self,df,modules):
    
        """ This function checks if for each value keys are part of ansible documentation and if so return the description. If value keys are not part of ansible documentation but contain 
        the key 'name' return its description. It was found that even in values of nested dictionaries of a given parent value there might a list of keys. In that case we check once again if
        those keys are part of ansible documentation and return descriptions respectively. Finally, if the value is a string we return the string"""

        for idx, content in self.df['mod_values_found'].iteritems():
            if content:
                for key in content:
                    if key in list(self.modules.keys()):
                        text = self.modules[key]
                        if self.df.at[idx,'value_module_text'] == '':
                            self.df.at[idx,'value_module_text'] = text
                        else:
                            self.df.at[idx,'value_module_text'] += ' ' +text
                    else:
                        if isinstance(key, str):
                            ind = content.index(key)
                            text = content[ind]
                            # if ('{{' in text) and ('}}' in text):
                                # first_bracket = text.index('{')
                                # last_bracket = text.rfind('}')
                                # sub_text = text[first_bracket:last_bracket+1]
                                # sub_text1 = sub_text.replace('{','')
                                # sub_text2 = sub_text1.replace('}','')
                                # sub_text3 = sub_text2.replace(' ','')
                                # text = 'variable ' + sub_text3
                            self.df.at[idx,'value_module_text'] += text
                        elif isinstance(key, list):
                            for k in key:
                                if k in list(self.modules.keys()):
                                    text = self.modules[k]
                                    if self.df.at[idx,'value_module_text'] == '':
                                        self.df.at[idx,'value_module_text'] = text
                                    else:
                                        self.df.at[idx,'value_module_text'] += ' ' +text
                                else:
                                    text = ' '.join(key)
                                    self.df.at[idx,'value_module_text'] += text
            else:
                self.df.at[idx,'value_module_text'] = ''
                
        return df
    def create_text_cols(self):
    
        """ This is the function to be called in order to create the new columns """
    
        self.df['mod_keys_found'] = ''
        self.df['mod_values_found'] = ''
        self.df['key_module_text'] = ''
        self.df['value_module_text'] = ''

        df = self.search_ansible_modules(self.df,self.modules)
        df = self.create_key_module_column(self.df,self.modules)
        df = self.create_value_module_column(self.df,self.modules)

        return df