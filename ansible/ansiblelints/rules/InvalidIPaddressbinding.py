from ansiblelint import AnsibleLintRule


class InvalidIPaddressbinding(AnsibleLintRule):
    id = 'ANSIBLE0007'
    descreiption = 'check if the IP address has the 0.0.0.0 format'
    severity = 'HIGH'
    tags = ['validity']
    version_added = 'v1.0.0'
    shortdesc ='check if password is fixed'

    def match(self, file, line):

        if "0.0.0.0" in line:
            return line



        #print(line.)
        #line_elements =(line.split())
        #print(line_elements)

        #print(type(line_elements))

        #for index_number, element in enumerate(line_elements):
            #if "tinyproxy_port" in element:
                #print(index_number)
                #print(line_elements[index_number-3])
        #print(str(task['action'].get('ansible_become_pass')))
        #print(type(task["action"]["__ansible_module__"]))
        #if task["action"]["__ansible_module__"] in self._modules:
            #pass_word = task['action'].get('login_password')
            #pass_word = str(pass_word)
            #print(pass_word)
            #print(len(pass_word))
            #print("default('')" in pass_word)
            #if len(pass_word) == 0 :
                #return pass_word