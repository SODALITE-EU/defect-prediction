from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('octal_template.txt')
output_from_parsed_template = template.render(module_name='file', parameter_name='mode')
print(output_from_parsed_template)

# to save the results
with open("rules/octal_file.py", "w") as fh:
    fh.write(output_from_parsed_template)