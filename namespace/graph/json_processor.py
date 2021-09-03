import json
import numpy as np

from constant import CONSTANT

def get_data_matrix():
    with open(CONSTANT['FILE']['JSON'], 'r') as f:
        data = json.load(f)
    champion_matrix = np.zeros((len(data['champions']), len(data['traits']) + 1), dtype=np.uint8)
    trait_matrix = np.zeros((len(data['traits']), max([max(trait['level']) for trait in data['traits']]) + 1), dtype=np.uint8)
    trait_number_matrix = np.zeros((len(data['traits']), max([len(trait['level']) for trait in data['traits']]) + 1))
    for trait_id, trait in enumerate(data['traits']):
        for n in trait['level']:
            trait_matrix[trait_id][n] = 1
    for champ_id, champ in enumerate(data['champions']):
        champion_matrix[champ_id][-1] = champ['cost']
        for trait_name in champ['traits']:
            for trait_id, trait in enumerate(data['traits']):
                if trait['name'] == trait_name:
                    champion_matrix[champ_id][trait_id] = 1
                    break
    for i, trait in enumerate(data['traits']):
        for j, level in enumerate(trait['level']):
            trait_number_matrix[i][j + 1] = level
    return champion_matrix, trait_matrix, trait_number_matrix
