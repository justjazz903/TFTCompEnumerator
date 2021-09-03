import numpy as np

def comp_id_to_bit_code(comp_id):
    bit_code = 0
    for current_id in comp_id:
        setter = 1 << current_id
        bit_code |= setter
    return bit_code

def bit_code_to_comp_id(bit_code, champ_num):
    comp_id = list()
    for i in range(champ_num):
        probe = 1 << i
        if probe & bit_code == probe:
            comp_id.append(i)
    return comp_id

def comp_id_to_comp_vec(comp_id, champ_num):
    comp_vec = np.zeros(champ_num, dtype=np.int8)
    for champ_id in comp_id:
        comp_vec[champ_id] = 1
    return comp_vec

def bit_code_to_comp_vec(bit_code, champ_num):
    return comp_id_to_comp_vec(bit_code_to_comp_id(bit_code, champ_num), champ_num)
