import json
import numpy as np

from namespace.graph.coder import bit_code_to_comp_id
from constant import CONSTANT

def get_comp_matrix(comp_id, champion_matrix, trait_matrix):
    cost = champion_matrix[comp_id][:,-1]
    comp_trait = np.sum(champion_matrix[comp_id], axis=0)[:-1]
    comp_trait = comp_trait * trait_matrix.T
    trait = np.zeros((trait_matrix.shape[0]), dtype=np.int8)
    for trait_num in range(comp_trait.shape[0]):
        if trait_num == 0:
            continue
        trait += np.where(comp_trait[trait_num] >= trait_num, 1, 0)
    return trait, cost

def print_comp(bit_code, champion_matrix, trait_matrix):
    with open(CONSTANT['FILE']['JSON'], 'r') as f:
        json_file = json.load(f)
    comp_id = bit_code_to_comp_id(bit_code, len(json_file['champions']))
    trait, cost = get_comp_matrix(comp_id, champion_matrix, trait_matrix)
    champ_names = list()
    for champ_id in comp_id:
        champ_names.append(json_file['champions'][champ_id]['name'])
    trait_names = list()
    for trait_id in range(len(trait)):
        if trait[trait_id] != 0:
            trait_names.append(json_file['traits'][trait_id]['name'] + ': ' + str(json_file['traits'][trait_id]['level'][trait[trait_id] - 1]))
    return champ_names, trait_names, round(np.mean(cost), 2)
