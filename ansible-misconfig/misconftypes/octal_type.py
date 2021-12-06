import spacy

nlp = spacy.load("en_core_web_sm")


def check_similarity(par_descr, ref_text):
    doc1 = nlp(par_descr)
    doc2 = nlp(ref_text)
    similarity_score = doc1.similarity(doc2)
    if "octal" in par_descr and similarity_score > 0.64:
        return True
    return False


def gen_rule(df_parameter_level_texts, env):
    df_parameter_level_texts['conf_index'] = df_parameter_level_texts['Description'].apply(check_similarity,
                                                                                           ref_text="""You must either add a leading zero so that Ansible's YAML parser knows it is an octal number or quote it so Ansible receives a string and can do its own conversion from string into number.""")

    # print(df_parameter_level_texts[df_parameter_level_texts['conf_index'] == True]['Module_Name'].unique())
    sel_mod_parameters = df_parameter_level_texts[df_parameter_level_texts['conf_index'] == True][
        ['Module_Name', 'Parameter_Name', 'Module_Link']].drop_duplicates().values

    for each_val in sel_mod_parameters:
        rule_name = 'OctalPermissionsRule'
        tm = env.get_template('octal_template.txt')
        python_render_file = tm.render(rule_name=rule_name,
                                       rule_id='risky-octal',
                                       rule_desc_short='Octal file permissions must contain leading zero or be a string',
                                       rule_desc='Numeric file permissions without leading zero can behave in unexpected ways. See ' +
                                                 each_val[2] + ' for more details',
                                       modules_sel=each_val[0],
                                       parameter_name=each_val[1],
                                       misconfiguration_type='Formatting')
        # to save the results
        with open("rules/" + each_val[0] + "_" + each_val[1] + "octal_file.py", "w") as fh:
            fh.write(python_render_file)
        fh.close()
