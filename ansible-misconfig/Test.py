from ansible_module_documentation import scrap_module_info

top_module_df, list_all_modules = scrap_module_info(modules_list=['copy'])
print(top_module_df)
print(list_all_modules)
