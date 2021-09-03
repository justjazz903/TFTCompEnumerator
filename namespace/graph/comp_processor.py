import numpy as np

def get_comp_cost(comp_id, champion_matrix):
    return champion_matrix[comp_id][:,-1]

def get_comp_matrix(comp_id, champion_matrix, trait_matrix):
    cost = get_comp_cost(comp_id, champion_matrix)
    comp_trait = np.sum(champion_matrix[comp_id], axis=0)[:-1]
    # 8: draconic
    # comp_trait[8] = 0
    # --------------------------
    comp_trait = comp_trait * trait_matrix.T
    trait = np.zeros((trait_matrix.shape[0]), dtype=np.int8)
    for trait_num in range(comp_trait.shape[0]):
        if trait_num == 0:
            continue
        trait += np.where(comp_trait[trait_num] >= trait_num, 1, 0)
    return trait, cost
