from ansiblelint import AnsibleLintRule


class HttpWithoutTls(AnsibleLintRule):
    id = 'ANSIBLE0008'
    descreiption = 'check if url addresses has http instead of https'
    severity = 'HIGH'
    tags = {'incomplete'}
    version_added = 'v1.0.0'
    _modules = ['uri']
    shortdesc ='check if url addresses has http instead of https'

    def matchtasks(self, file, task):
        #print(task)
        #print(str(task['action'].get('url')))
        code_script  = task
        #print(code_script)
        with_out_tls_count = code_script.count('http:')
        if with_out_tls_count >= 1 :
            return with_out_tls_count*['http:']

        return False

        #print(type(task["action"]["__ansible_module__"]))
        #if task["action"]["__ansible_module__"] in self._modules:
         #   pass_word = task['action'].get('url')
         #   pass_word = str(pass_word)
          #  print(pass_word)
            #print(len(pass_word))
            #print("default('')" in pass_word)
            #if len(pass_word) == 0 :
                #return pass_word