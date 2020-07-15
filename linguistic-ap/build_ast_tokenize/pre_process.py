import pandas as pd
import numpy as np

remove_list = [',', '``','"',"''",'==','{','}','(',"'",'[',']',"'==",')','>','=','-','|','/','+','$','.+',':','!','--','\\','?','@',';','&','#','^','<','*','%','.','=~']

def remove_symbols(sequence):
    
    for obj in sequence:
        for element in obj:
            if element in remove_list:
                obj.remove(element)
            elif "'" in element:
                obj.remove(element)                

    return sequence

def flatten_list(sequence):

    flat_list = [item for sublist in sequence for item in sublist]

    return flat_list

def remove_symbols_simple(sequence):

    for item in sequence:
        if item in remove_list:
            sequence.remove(item)

    return sequence