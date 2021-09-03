import pickle

from namespace.graph.coder import bit_code_to_comp_id
from namespace.graph.comp_processor import get_comp_cost

def default_extracter(filepath, score, level, champion_matrix, trait_matrix):
    used_champions = [False for _ in range(champion_matrix.shape[0])]
    res = list()
    with open(filepath, 'rb') as f:
        data = pickle.load(f)
    if not score in data.keys():
        return res, used_champions
    for bit_code in data[score]:
        comp_id = bit_code_to_comp_id(bit_code, champion_matrix.shape[0])
        cost = get_comp_cost(comp_id, champion_matrix)
        ############### cost check with level ###############
        if (level == 5 or level == 6) and (4 in cost or 5 in cost):
            for i in range(len(comp_id)):
                if cost[i] == 4 or cost[i] == 5:
                    used_champions[comp_id[i]] = True
            continue
        if (level == 7) and (5 in cost):
            for i in range(len(comp_id)):
                if cost[i] == 5:
                    used_champions[comp_id[i]] = True
            continue
        #####################################################
        res.append(bit_code)
        for champ_id in comp_id:
            used_champions[champ_id] = True
    return res, used_champions
