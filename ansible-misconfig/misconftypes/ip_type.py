def contain_ip(par_descr):
    case_insensitive_descr = par_descr.casefold()
    if "hostname/ip" in par_descr or "ip address" in case_insensitive_descr:
        return True
    return False


def gen_rule_ip_type(df_parameter_level_texts, env):
    df_parameter_level_texts['conf_index'] = df_parameter_level_texts['Description'].apply(contain_ip)

    sel_mod_parameters = df_parameter_level_texts[df_parameter_level_texts['conf_index'] == True][
        ['Module_Name', 'Parameter_Name', 'Module_Link']].drop_duplicates().values

    for each_val in sel_mod_parameters:
        rule_name = 'IPTypeRule'
        tm = env.get_template('ip_type_template.txt')
        python_render_file = tm.render(rule_name=rule_name,
                                       rule_id='risky-octal',
                                       rule_desc_short='IP address must be in valid format',
                                       rule_desc='IP address must be in valid format. See ' +
                                                 each_val[2] + ' for more details',
                                       modules_sel=each_val[0],
                                       parameter_name=each_val[1],
                                       misconfiguration_type='Formatting')
        # to save the results
        with open("rules/" + each_val[0] + "_" + each_val[1] + "_ip_type.py", "w") as fh:
            fh.write(python_render_file)
        fh.close()
