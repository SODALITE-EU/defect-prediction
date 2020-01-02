from ansiblelint import AnsibleLintRule
import ruamel.yaml


class ComplexExpression(AnsibleLintRule):
    id = 'ANSIBLE0012'
    descreiption = 'code script contains a difficult to understand complex expression like having several if, and, or'
    severity = 'medium'
    tags = {'complex'}
    version_added = 'v1.0.0'
    shortdesc ='difficult to understand complex expression in code'
    #_modules = ['fortiosconfig']


    def match(self, file, line):
        if ' when:' in line:
            if sum(line.count(word) for word in [' if ', ' and ', ' or ', '|', ' | ']) > 2:
                return(line)







        #print(task['action'])
        #if task["action"]["__ansible_module__"] in self._modules:
            #print("HELLO")
        #data = task["action"]["__ansible_module__"]
        #print(data)
        #if task["action"]["__ansible_module__"] == 'fortiosconfig' :
        #    complex_expre = task['action'].getfull('username')
         #   complex_expre = str(complex_expre)
         #   print(complex_expre)
         #   return(complex_expre)


        #with open(file['path']) as fp:
       #     data = ruamel.yaml.round_trip_load(fp)

        #print(type(data))

        #word_list = [' if ', ' and ', ' or ', '|', ' | ']
        #word_count = []

        #for line in ruamel.yaml.round_trip_dump(data).splitlines(False):
         #   print((line))

         #   for word in word_list:
          #      if word in line:
          #          word_count.append(word)

         #   if len(word_count) > 2:
          #      return line
